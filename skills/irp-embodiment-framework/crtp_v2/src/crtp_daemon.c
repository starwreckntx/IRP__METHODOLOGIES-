/*
 * CRTP Provenance Daemon v2.0
 *
 * Listens on CRTP_PORT (UDP 6666) for CRTP-framed packets.
 * Validates:
 *   - Layer 0 biometric binding (voiceprint hash)
 *   - Cumulative chain hash across all traversed layers
 *   - Recursion depth limits (Guardian Codex Article 5)
 *   - CRC32 header integrity
 *
 * On validation failure:
 *   - Packets are silently dropped (no ACK to attacker)
 *   - Incident logged to /var/log/irp/incidents.log
 *   - Guardian kill switch activated for hash mismatches
 *
 * Part of the IRP Embodiment Framework (Lower Layer)
 * Build: see Makefile
 *
 * Reference: Kimi K2.5 design session 2026-02-08
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <time.h>
#include <syslog.h>
#include <signal.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include "irp_chain.h"

/* ── Paths ──────────────────────────────────────────── */
#define INCIDENT_LOG    "/var/log/irp/incidents.log"
#define CHAIN_LOG       "/var/log/irp/chain_audit.log"
#define ENROLLED_KEYS   "/etc/irp/enrolled.biometric"
#define GUARDIAN_BAN     "/etc/irp/guardian.ban"

/*
 * Bind address: set via IRP_BIND_ADDR environment variable.
 * Defaults to 0.0.0.0 if not set.
 * In production, set to the Tailscale mesh IP of this node:
 *   export IRP_BIND_ADDR=<TAILSCALE_NODE_IP>
 */
#define DEFAULT_BIND_ADDR   "0.0.0.0"

static volatile int keep_running = 1;

static void signal_handler(int sig) {
    (void)sig;
    keep_running = 0;
}

/* ── CRC32 (zlib-compatible) ────────────────────────── */
static uint32_t crc_table[256];
static int crc_initialized = 0;

static void init_crc32(void) {
    if (crc_initialized) return;
    for (int i = 0; i < 256; i++) {
        uint32_t c = (uint32_t)i;
        for (int j = 0; j < 8; j++) {
            c = (c & 1) ? (0xEDB88320 ^ (c >> 1)) : (c >> 1);
        }
        crc_table[i] = c;
    }
    crc_initialized = 1;
}

uint32_t crc32_compute(const void *data, size_t len) {
    if (!crc_initialized) init_crc32();
    const uint8_t *buf = data;
    uint32_t c = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        c = crc_table[(c ^ buf[i]) & 0xFF] ^ (c >> 8);
    }
    return c ^ 0xFFFFFFFF;
}

/* ── Chain Hash Computation ─────────────────────────── */
int compute_chain_hash(chain_link_t *prev, chain_link_t *current, uint8_t *out) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    if (!ctx) return ERR_HASH_COMPUTATION;

    unsigned char full[32];
    unsigned int full_len = 0;

    EVP_DigestInit_ex(ctx, EVP_sha256(), NULL);

    if (prev) {
        EVP_DigestUpdate(ctx, prev->layer_hash, HASH_LEN);
    } else {
        /* Genesis: hash biometric directly */
        EVP_DigestUpdate(ctx, current->node_fingerprint, NODE_ID_LEN);
    }

    EVP_DigestUpdate(ctx, &current->layer_id, 1);
    EVP_DigestUpdate(ctx, &current->timestamp, 8);
    EVP_DigestUpdate(ctx, current->node_fingerprint, NODE_ID_LEN);

    EVP_DigestFinal_ex(ctx, full, &full_len);
    EVP_MD_CTX_free(ctx);

    /* Truncate SHA-256 to 128-bit */
    memcpy(out, full, HASH_LEN);
    return CHAIN_VALID;
}

/* ── Full Chain Verification ────────────────────────── */
int verify_chain(crtp_header_t *hdr, uint8_t *layer_attestations, size_t attest_len) {
    if (hdr->magic != IRP_MAGIC)        return ERR_INVALID_MAGIC;
    if (hdr->version != IRP_VERSION)     return ERR_VERSION_MISMATCH;
    if (hdr->recursion_depth > MAX_RECURSION) return ERR_RECURSION_EXCEEDED;

    /* CRC32 over header bytes [0..59] (everything except the CRC field itself) */
    uint32_t comp_crc = crc32_compute(hdr, 60);
    if (comp_crc != hdr->crc32) return ERR_CRC_FAILURE;

    chain_link_t layers[MAX_RECURSION + 1];
    uint8_t current_hash[HASH_LEN];

    /* Layer 0: Biometric genesis */
    memset(&layers[0], 0, sizeof(chain_link_t));
    layers[0].layer_id = LAYER_HUMAN;
    layers[0].timestamp = 0;    /* Genesis has no time */
    memcpy(layers[0].node_fingerprint, hdr->src_biometric, NODE_ID_LEN);
    memcpy(layers[0].layer_hash, hdr->src_biometric, HASH_LEN);

    /*
     * Layer attestations are packed after the header.
     * Each attestation is 32 bytes:
     *   [0]      layer_id
     *   [1-8]    timestamp (uint64_t)
     *   [9-24]   node_fingerprint (16 bytes)
     *   [25-31]  padding / future use
     */
    size_t expected_attest = (size_t)hdr->recursion_depth * 32;
    if (attest_len < expected_attest) return ERR_MALFORMED_ATTESTATION;

    for (int i = 1; i <= hdr->recursion_depth; i++) {
        uint8_t *attest = layer_attestations + ((i - 1) * 32);

        layers[i].layer_id = attest[0];
        memcpy(&layers[i].timestamp, attest + 1, 8);
        memcpy(layers[i].node_fingerprint, attest + 9, NODE_ID_LEN);

        if (compute_chain_hash(&layers[i - 1], &layers[i], current_hash) != CHAIN_VALID) {
            return ERR_HASH_COMPUTATION;
        }
        memcpy(layers[i].layer_hash, current_hash, HASH_LEN);
    }

    /* Final: does the header chain_hash match our recomputation? */
    if (memcmp(current_hash, hdr->chain_hash, HASH_LEN) != 0) {
        log_incident("CHAIN_HASH_MISMATCH", hdr, current_hash);
        return ERR_CHAIN_HASH_MISMATCH;
    }

    return CHAIN_VALID;
}

/* ── Incident Logging ───────────────────────────────── */
void log_incident(const char *type, crtp_header_t *hdr, uint8_t *computed_hash) {
    FILE *fp = fopen(INCIDENT_LOG, "a");
    if (!fp) return;

    time_t now = time(NULL);
    struct tm *tm_info = gmtime(&now);
    char timestr[32];
    strftime(timestr, sizeof(timestr), "%Y-%m-%dT%H:%M:%SZ", tm_info);

    fprintf(fp, "[%s] INCIDENT: %s | Depth: %d | Model: 0x%02x",
            timestr, type, hdr->recursion_depth, hdr->model_type);

    if (computed_hash) {
        fprintf(fp, " | Expected: ");
        for (int i = 0; i < HASH_LEN; i++)
            fprintf(fp, "%02x", computed_hash[i]);
    }

    fprintf(fp, " | Received: ");
    for (int i = 0; i < HASH_LEN; i++)
        fprintf(fp, "%02x", hdr->chain_hash[i]);

    fprintf(fp, "\n");
    fclose(fp);
    chmod(INCIDENT_LOG, 0600);
}

/* ── Guardian Kill Switch ───────────────────────────── */
int guardian_kill_switch(uint8_t *biometric_id) {
    /* Append banned biometric to guardian ban list */
    FILE *fp = fopen(GUARDIAN_BAN, "a");
    if (fp) {
        for (int i = 0; i < BIOMETRIC_LEN; i++)
            fprintf(fp, "%02x", biometric_id[i]);
        fprintf(fp, "\n");
        fclose(fp);
    }

    /* Trigger MCSE checkpoint rollback */
    /* NOTE: In production, replace with D-Bus call or direct IPC */
    syslog(LOG_ALERT,
           "IRP Guardian: Kill switch activated for biometric %02x%02x...",
           biometric_id[0], biometric_id[1]);

    return 0;
}

/* ── Biometric Enrollment Check ─────────────────────── */
int verify_biometric_enrolled(uint8_t *biometric) {
    FILE *fp = fopen(ENROLLED_KEYS, "r");
    if (!fp) return -1;    /* No keys enrolled = fail closed */

    char line[64];
    while (fgets(line, sizeof(line), fp)) {
        uint8_t enrolled[BIOMETRIC_LEN];
        int matches = 1;
        for (int i = 0; i < BIOMETRIC_LEN; i++) {
            unsigned int byte_val;
            if (sscanf(line + (i * 2), "%2x", &byte_val) != 1) {
                matches = 0;
                break;
            }
            enrolled[i] = (uint8_t)byte_val;
            if (enrolled[i] != biometric[i]) {
                matches = 0;
                break;
            }
        }
        if (matches) {
            fclose(fp);
            return 0;  /* Found */
        }
    }
    fclose(fp);
    return -1;  /* Not enrolled */
}

/* ── Main Server Loop ───────────────────────────────── */
int main(int argc, char *argv[]) {
    (void)argc;
    (void)argv;

    signal(SIGINT,  signal_handler);
    signal(SIGTERM, signal_handler);

    /* Ensure directories exist */
    mkdir("/var/log/irp", 0755);
    mkdir("/etc/irp",     0700);

    openlog("irp-crtp", LOG_PID, LOG_DAEMON);
    syslog(LOG_INFO, "CRTP Daemon v%d starting on port %d", IRP_VERSION, CRTP_PORT);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    /* Resolve bind address from environment or default */
    const char *bind_addr = getenv("IRP_BIND_ADDR");
    if (!bind_addr) bind_addr = DEFAULT_BIND_ADDR;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port   = htons(CRTP_PORT);
    addr.sin_addr.s_addr = inet_addr(bind_addr);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        /* Fallback to any interface */
        addr.sin_addr.s_addr = INADDR_ANY;
        if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
            perror("bind");
            close(sock);
            return 1;
        }
        syslog(LOG_WARNING, "Bound to 0.0.0.0 - configured interface not available");
    } else {
        syslog(LOG_INFO, "Bound to %s:%d", bind_addr, CRTP_PORT);
    }

    uint8_t buffer[4096];
    struct sockaddr_in client;
    socklen_t client_len;

    while (keep_running) {
        client_len = sizeof(client);
        ssize_t len = recvfrom(sock, buffer, sizeof(buffer), 0,
                               (struct sockaddr *)&client, &client_len);
        if (len < 0) continue;
        if ((size_t)len < sizeof(crtp_header_t)) continue;  /* Too small */

        crtp_header_t *hdr = (crtp_header_t *)buffer;

        /* Layer 0: Biometric verification (fail closed) */
        if (verify_biometric_enrolled(hdr->src_biometric) != 0) {
            log_incident("UNENROLLED_BIOMETRIC", hdr, NULL);
            continue;  /* Silent drop - no response */
        }

        /* Extract layer attestations (after header) */
        uint8_t *attestations = buffer + sizeof(crtp_header_t);
        size_t attest_len = (size_t)len - sizeof(crtp_header_t);

        /* Verify chain */
        int result = verify_chain(hdr, attestations, attest_len);

        if (result == CHAIN_VALID) {
            syslog(LOG_DEBUG, "Valid CRTP packet from %s depth=%d model=0x%02x",
                   inet_ntoa(client.sin_addr),
                   hdr->recursion_depth,
                   hdr->model_type);

            /* Forward to local model API if payload present */
            if (hdr->payload_len > 0 && attest_len >= hdr->payload_len) {
                FILE *audit = fopen(CHAIN_LOG, "a");
                if (audit) {
                    fprintf(audit, "%ld: Valid chain depth=%d model=0x%02x from=%s\n",
                            (long)time(NULL),
                            hdr->recursion_depth,
                            hdr->model_type,
                            inet_ntoa(client.sin_addr));
                    fclose(audit);
                }
                /*
                 * TODO: Forward payload to local model endpoint
                 * (e.g., localhost:11434 for Ollama / Kimi)
                 * Implementation depends on deployment topology.
                 */
            }
        } else {
            const char *reason;
            switch (result) {
            case ERR_INVALID_MAGIC:
                reason = "INVALID_MAGIC";
                break;
            case ERR_VERSION_MISMATCH:
                reason = "VERSION_MISMATCH";
                break;
            case ERR_RECURSION_EXCEEDED:
                reason = "RECURSION_EXCEEDED";
                guardian_kill_switch(hdr->src_biometric);
                break;
            case ERR_CRC_FAILURE:
                reason = "CRC_FAILURE";
                break;
            case ERR_CHAIN_HASH_MISMATCH:
                reason = "CHAIN_HASH_MISMATCH";
                guardian_kill_switch(hdr->src_biometric);
                break;
            default:
                reason = "UNKNOWN_FAILURE";
            }
            syslog(LOG_WARNING, "Rejected packet from %s: %s",
                   inet_ntoa(client.sin_addr), reason);
        }
    }

    syslog(LOG_INFO, "CRTP Daemon shutting down");
    closelog();
    close(sock);
    return 0;
}
