/*
 * CRTP Chain Verification Module
 *
 * Standalone chain-hash validation that can be linked
 * into any IRP node binary (daemon, CLI tool, eBPF loader).
 *
 * Algorithm: SHA-256_trunc128(prev_hash || layer_identity || timestamp || node_fingerprint)
 *
 * Hash evolution for a typical 4-layer stack:
 *
 *   Layer 0 (Human/Biometric):
 *     H0 = SHA256_trunc128(biometric_seed || 0x00 || timestamp || node_fp)
 *
 *   Layer 1 (Entry Model, e.g. Gemini):
 *     H1 = SHA256_trunc128(H0 || 0x01 || timestamp || node_fp)
 *
 *   Layer 2 (SSH Tunnel):
 *     H2 = SHA256_trunc128(H1 || 0x02 || timestamp || node_fp)
 *
 *   Layer 3 (Execution Model, e.g. Kimi):
 *     H3 = SHA256_trunc128(H2 || 0x03 || timestamp || node_fp)
 *
 * Verification: Recompute H0..H(n), compare H(n) to header chain_hash.
 *
 * Part of the IRP Embodiment Framework (Lower Layer)
 * Reference: Kimi K2.5 design session 2026-02-08
 */

#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include "irp_chain.h"

/*
 * validate_provenance_chain()
 *
 * Full packet validation including CRC, biometric check,
 * and cumulative hash chain reconstruction.
 *
 * Returns CHAIN_VALID (0) on success, negative error code on failure.
 */
int validate_provenance_chain(uint8_t *packet_header, size_t len) {
    if (len < sizeof(crtp_header_t))
        return ERR_MALFORMED_ATTESTATION;

    crtp_header_t *hdr = (crtp_header_t *)packet_header;

    /* Quick rejection: magic number */
    if (hdr->magic != IRP_MAGIC)
        return ERR_INVALID_MAGIC;

    /* Version gate */
    if (hdr->version != IRP_VERSION)
        return ERR_VERSION_MISMATCH;

    /* CRC32 over bytes [0..59] */
    uint32_t computed_crc = crc32_compute(packet_header, 60);
    if (computed_crc != hdr->crc32)
        return ERR_CRC_FAILURE;

    /* Guardian Codex Article 5: recursion depth limit */
    if (hdr->recursion_depth > MAX_RECURSION)
        return ERR_RECURSION_EXCEEDED;

    /* Reconstruct chain based on recursion depth */
    uint8_t computed_hash[HASH_LEN];
    uint8_t prev_hash[HASH_LEN];

    /* Layer 0: Genesis (Biometric) - biometric IS the genesis hash */
    memcpy(prev_hash, hdr->src_biometric, HASH_LEN);

    /* Iterate through claimed layers */
    for (int i = 1; i <= hdr->recursion_depth; i++) {
        size_t offset = sizeof(crtp_header_t) + ((size_t)(i - 1) * 32);

        if (offset + 32 > len)
            return ERR_MALFORMED_ATTESTATION;

        uint8_t *layer_data = packet_header + offset;

        /* Hash(prev || layer_identity) */
        EVP_MD_CTX *ctx = EVP_MD_CTX_new();
        if (!ctx) return ERR_HASH_COMPUTATION;

        unsigned char full[32];
        unsigned int full_len = 0;

        EVP_DigestInit_ex(ctx, EVP_sha256(), NULL);
        EVP_DigestUpdate(ctx, prev_hash, HASH_LEN);
        EVP_DigestUpdate(ctx, layer_data, 32);  /* layer_id + timestamp + node_sig */
        EVP_DigestFinal_ex(ctx, full, &full_len);
        EVP_MD_CTX_free(ctx);

        memcpy(computed_hash, full, HASH_LEN);
        memcpy(prev_hash, computed_hash, HASH_LEN);
    }

    /* Final verification */
    if (memcmp(computed_hash, hdr->chain_hash, HASH_LEN) != 0) {
        log_incident("CHAIN_HASH_MISMATCH", hdr, computed_hash);
        guardian_kill_switch(hdr->src_biometric);
        return ERR_CHAIN_HASH_MISMATCH;
    }

    return CHAIN_VALID;
}
