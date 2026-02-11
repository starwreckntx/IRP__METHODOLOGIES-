/*
 * IRP Chain - CRTP Provenance Header v2.0
 *
 * Wire-protocol header for cryptographic chain-of-custody
 * across recursive model invocations, SSH tunnels, and
 * biometric-bound operator identity.
 *
 * Part of the IRP Embodiment Framework (Lower Layer)
 * Codex Law Alignment: CONSENT, INTEGRITY
 *
 * Reference: Kimi K2.5 design session 2026-02-08
 */

#ifndef IRP_CHAIN_H
#define IRP_CHAIN_H

#include <stdint.h>
#include <sys/socket.h>
#include <netinet/in.h>

/* ── Protocol Constants ─────────────────────────────── */
#define CRTP_PORT           6666
#define IRP_MAGIC           0x43525450  /* "CRTP" */
#define IRP_VERSION         0x02
#define MAX_RECURSION       3
#define HASH_LEN            16          /* SHA-256 truncated to 128-bit */
#define BIOMETRIC_LEN       16
#define NODE_ID_LEN         16

/* ── Layer Type Enumeration ─────────────────────────── */
#define LAYER_HUMAN         0x00
#define LAYER_GEMINI        0x01
#define LAYER_SSH           0x02
#define LAYER_KIMI          0x03
#define LAYER_CLAUDE        0x04
#define LAYER_GPT           0x05

/* ── Header Flags ───────────────────────────────────── */
#define FLAG_RECURSION      0x80    /* R: Packet traverses recursive path   */
#define FLAG_EMERGENCY      0x40    /* E: Guardian emergency escalation     */
#define FLAG_DATA           0x20    /* D: Payload contains data chunk       */
#define FLAG_SYNC           0x10    /* S: Synchronization / heartbeat       */

/* ── Error Codes ────────────────────────────────────── */
#define CHAIN_VALID                  0
#define ERR_INVALID_MAGIC           -1
#define ERR_VERSION_MISMATCH        -2
#define ERR_RECURSION_EXCEEDED      -3
#define ERR_CRC_FAILURE             -4
#define ERR_MALFORMED_ATTESTATION   -5
#define ERR_HASH_COMPUTATION        -6
#define ERR_CHAIN_HASH_MISMATCH     -7

/*
 * ── CRTP Wire-Format Header (64 bytes, packed) ────────
 *
 * Byte layout:
 *   [0-3]    Magic Number:      0x43525450 ("CRTP")
 *   [4]      Version:           0x02
 *   [5]      Layer Flags:       [R|E|D|S|reserved...]
 *   [6-7]    Payload Length:    uint16_t (big-endian)
 *   [8-23]   Source Node ID:    128-bit hash (Tailscale IP + biometric salt)
 *   [24-39]  Dest Node ID:     128-bit hash
 *   [40]     Recursion Depth:  uint8_t (0-255, Guardian kills >3)
 *   [41]     Model Type:       uint8_t enum
 *   [42-43]  Instance Stamp:   uint16_t (session ephemeral, rotates every 5min)
 *   [44-59]  Chain Hash:       SHA256 truncated to 128-bit (cumulative)
 *   [60-63]  CRC32:            Header integrity check
 *   [PAYLOAD...]
 *   [END]    Biometric Seal:   HMAC-SHA256(Layer 0 voiceprint key, entire packet)
 */
typedef struct __attribute__((packed)) {
    uint32_t    magic;
    uint8_t     version;
    uint8_t     flags;
    uint16_t    payload_len;
    uint8_t     src_biometric[BIOMETRIC_LEN];   /* Layer 0: Voiceprint hash  */
    uint8_t     dst_node[NODE_ID_LEN];
    uint8_t     recursion_depth;
    uint8_t     model_type;
    uint16_t    instance_stamp;
    uint8_t     chain_hash[HASH_LEN];           /* Cumulative H(n)          */
    uint32_t    crc32;
} crtp_header_t;

/*
 * ── Chain Link (per-layer attestation record) ─────────
 *
 * Each layer in the origin_stack contributes one link.
 * Hash evolution: H(n) = SHA256_trunc128(H(n-1) || layer_id || timestamp || node)
 */
typedef struct {
    uint8_t     layer_id;
    uint64_t    timestamp;
    uint8_t     node_fingerprint[NODE_ID_LEN];
    uint8_t     layer_hash[HASH_LEN];
} chain_link_t;

/*
 * ── Embodiment Signature (Layer 0 binding) ────────────
 *
 * Compiled into CRTP daemon on each node.
 * Binds hardware identity + biometric to packet origin.
 */
typedef struct {
    uint8_t     hardware_type;      /* 0x01=ARM_mobile, 0x02=x86_desktop, 0x03=kali_node */
    uint8_t     biometric_hash[BIOMETRIC_LEN];  /* Truncated SHA256 of voiceprint + gait */
    uint64_t    epoch_nonce;        /* Hardware RNG from /dev/hwrng (or haveged)          */
    uint8_t     tailscale_ip[4];    /* Tailscale mesh address                             */
} embodiment_signature_t;

/* ── Function Prototypes ────────────────────────────── */

/* Chain hash computation: H(n) = SHA256_trunc128(prev || current_identity) */
int compute_chain_hash(chain_link_t *prev, chain_link_t *current, uint8_t *out);

/* Verify complete chain from Layer 0 (biometric) through Layer N */
int verify_chain(crtp_header_t *hdr, uint8_t *layer_attestations, size_t attest_len);

/* CRC32 (zlib-compatible) for header integrity */
uint32_t crc32_compute(const void *data, size_t len);

/* Incident logging (append-only, 0600 perms) */
void log_incident(const char *type, crtp_header_t *hdr, uint8_t *computed_hash);

/* Guardian Codex kill switch - bans biometric, triggers MCSE rollback */
int guardian_kill_switch(uint8_t *biometric_id);

/* Check if biometric hash is enrolled on this node */
int verify_biometric_enrolled(uint8_t *biometric);

#endif /* IRP_CHAIN_H */
