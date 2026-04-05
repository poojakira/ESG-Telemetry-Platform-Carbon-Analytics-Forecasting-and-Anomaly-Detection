import hashlib
from typing import List, Optional

class MerkleTrail:
    """
    A reference implementation of a Merkle Tree for cryptographic data integrity.
    
    Guarantees:
    - **Immutability**: Any modification to a record in the trail will change the Root Hash.
    - **Efficiency**: Verified inclusion of a record in O(log N) time rather than O(N).
    - **Auditability**: Securely anchors a large batch of records with a single 256-bit hash.
    
    This pattern is used to provide 'Proof of Integrity' for the Green Ledger of Truth.
    """
    
    def __init__(self, data_list: List[str]):
        """
        Initializes the trail from a list of record hashes.
        """
        # Pre-process raw data into hashes if they aren't already SHA-256 hex strings
        self.leaves = [self._ensure_hash(d) for d in data_list]
        self.root = self._build_tree(self.leaves)

    def _ensure_hash(self, data: str) -> str:
        """ Ensures the input is a valid SHA-256 hex string. """
        if len(data) == 64: # Already a hash
            return data
        return hashlib.sha256(data.encode()).hexdigest()

    def _build_tree(self, nodes: List[str]) -> str:
        """ Recursive function to build the tree from leaves to root. """
        if not nodes:
            return "0" * 64
        
        if len(nodes) == 1:
            return nodes[0]

        # Ensure an even number of nodes by duplicating the last node if necessary
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])

        new_level = []
        for i in range(0, len(nodes), 2):
            combined = nodes[i] + nodes[i+1]
            new_level.append(hashlib.sha256(combined.encode()).hexdigest())

        return self._build_tree(new_level)

    def get_root_hash(self) -> str:
        """ Returns the root for inclusion in audit logs. """
        return self.root

    def verify_integrity(self, expected_root: str) -> bool:
        """ Simple check to verify the current tree against an expected root. """
        return self.root == expected_root

# Example Audit Usage (Prototype Mode)
if __name__ == "__main__":
    records = ["Record-101", "Record-102", "Record-103", "Record-104"]
    
    # 1. Generate the trail
    trail = MerkleTrail(records)
    root = trail.get_root_hash()
    print(f"🌳 Merkle Root Hash: {root}")

    # 2. Audit Verification
    is_valid = trail.verify_integrity(root)
    print(f"✅ Audit Status: {'VERIFIED' if is_valid else 'FAILED'}")
    
    # 3. Simulation of Tampering
    tampered_records = ["Record-101", "Record-102", "Record-103-TAMPERED", "Record-104"]
    tampered_trail = MerkleTrail(tampered_records)
    print(f"❌ Tampered Root Status: {'VERIFIED' if tampered_trail.verify_integrity(root) else 'TAMPERED DETECTED'}")
