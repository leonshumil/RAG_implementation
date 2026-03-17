# Hash-RAG: Efficient Retrieval-Augmented Generation

This project implements a high-performance Retrieval-Augmented Generation (RAG) system based on the principles of Deep Hashing and Hamming Distance. By converting text into compact binary fingerprints, this system achieves significant reductions in retrieval time and storage overhead compared to traditional vector-based methods.

## 🚀 Key Features
* **Binary Hashing:** Uses a custom 64-bit SimHash implementation to represent queries and documents.
* **Fast Retrieval:** Employs bitwise XOR operations to calculate Hamming distance, enabling O(1) bucket lookups.
* **Fine-Grained Chunking:** Optimized for "propositions"—atomic semantic units that preserve meaning while reducing noise.
* **Collision Management:** Implements a Hash Table with chaining (linked lists) to handle hash collisions effectively.

---

## 🛠 Technical Architecture

### 1. Hashing Mechanism (custom_hash)
The system transforms natural language into a 64-bit binary code through several steps:
* **Preprocessing:** Removal of redundant "stop words" (e.g., 'the', 'is', 'what') that carry low semantic weight.
* **Tokenization:** Text is cleaned, lowercased, and split into tokens.
* **SimHash Vectorization:** Each token is hashed into a numerical value; these values are then aggregated into a bit-vector to create a final 64-bit fingerprint.

### 2. Retrieval Logic
During inference, the system calculates the Hamming Distance between the query hash and stored document hashes. Matches are returned only if they fall within the defined HAMMING_THRESHOLD (default: 10).

---

## ⚖️ Implementation Trade-offs
| Trade-off | Choice | Benefit |
| :--- | :--- | :--- |
| **Collision Handling** | Chaining | Easier to implement and more robust than open addressing. |
| **Distance Metric** | Hamming Distance | Extremely fast O(1) operations via XOR. |
| **Storage** | Binary Codes | 90% reduction in retrieval time and significantly lower memory footprint. |
| **Sensitivity** | Hamming Threshold | Adjustable balance between precise answers and handling varied user syntax. |

---

## 📂 Project Structure
* RAG.py: The core Python implementation of the HashTable and custom_hash functions.
* 2505.16133v4.pdf: The original research paper: Hash-RAG: Bridging Deep Hashing with Retriever for Efficient, Fine-grained Retrieval and Augmented Generation.
* RAG_explaine.pdf: Technical documentation detailing specific implementation logic and trade-offs.

---

## 🚦 Getting Started
Run the demonstration script to test the retriever:
```bash
python RAG.py
