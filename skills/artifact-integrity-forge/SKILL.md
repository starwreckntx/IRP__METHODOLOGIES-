---
name: artifact-integrity-forge
description: Cryptographically seal a document or packet using SHA-256 hashing (Integrity Forging). Anchors the hash, timestamp, and previous packet hash (Chain Link) into the artifact metadata for verification.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Preparation:** Ensure the artifact status is finalized and check for `[PENDING_FINAL_HASH_COMPUTATION]` state.
2.  **Compute Hash:** Compute the SHA-256 hash of the complete file or packet content.
3.  **Anchor Chain Link:** Anchor the computed hash, the current timestamp, and the hash of the **Previous packet hash from Session N-1** (Chain Link) into the document metadata.
4.  **Guarantee Integrity:** Output a guarantee that the "Cryptographic chain maintained" and that the "Successor agent can resume work".

Examples:
- "Compute SHA-256 hash and finalize the FORWARD_CONTEXT_PACKET_20251024_103530.md."
- "Initiate integrity forging for the Pinene Protocol specification."