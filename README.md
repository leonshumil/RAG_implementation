# Hash-RAG: Efficient Retrieval-Augmented Generation

[cite_start]This project implements a high-performance Retrieval-Augmented Generation (RAG) system based on the principles of **Deep Hashing** and **Hamming Distance**[cite: 8, 422]. [cite_start]By converting text into compact binary fingerprints, this system achieves significant reductions in retrieval time and storage overhead compared to traditional vector-based methods[cite: 9, 12, 423].

## 🚀 Key Features
* [cite_start]**Binary Hashing:** Uses a custom 64-bit SimHash implementation to represent queries and documents[cite: 423].
* [cite_start]**Fast Retrieval:** Employs bitwise XOR operations to calculate Hamming distance, enabling $O(1)$ bucket lookups[cite: 168, 423].
* [cite_start]**Fine-Grained Chunking:** Optimized for "propositions"—atomic semantic units that preserve meaning while reducing noise[cite: 10, 156, 161].
* [cite_start]**Collision Management:** Implements a Hash Table with chaining (linked lists) to handle hash collisions effectively[cite: 422, 425].

---

## 🛠 Technical Architecture

### 1. Hashing Mechanism (`custom_hash`)
The system transforms natural language into a 64-bit binary code through several steps:
* [cite_start]**Preprocessing:** Removal of redundant "stop words" (e.g., 'the', 'is', 'what') that carry low semantic weight[cite: 9].
* **Tokenization:** Text is cleaned, lowercased, and split into tokens.
* **SimHash Vectorization:** Each token is hashed into a numerical value; these values are then aggregated into a bit-vector to create a final 64-bit fingerprint.

### 2. Retrieval Logic
[cite_start]During inference, the system calculates the **Hamming Distance** between the query hash ($h_q$) and stored document hashes ($h_p$)[cite: 167, 168]:
$$dist_{H}(h_{q}, h_{p}) = \frac{1}{2}(d - \langle h_{q}, h_{p} \rangle)$$
[cite_start]Matches are returned only if they fall within the defined `HAMMING_THRESHOLD` (default: 10)[cite: 426].

---

## ⚖️ Implementation Trade-offs
[cite_start]As detailed in the project documentation[cite: 424]:
| Trade-off | Choice | Benefit |
| :--- | :--- | :--- |
| **Collision Handling** | Chaining | [cite_start]Easier to implement and more robust than open addressing[cite: 425]. |
| **Distance Metric** | Hamming Distance | [cite_start]Extremely fast $O(1)$ operations via XOR[cite: 423]. |
| **Storage** | Binary Codes | [cite_start]90% reduction in retrieval time and significantly lower memory footprint[cite: 12, 423]. |
| **Sensitivity** | Hamming Threshold | [cite_start]Adjustable balance between precise answers and handling varied user syntax[cite: 426]. |

---

## 📂 Project Structure
* `RAG.py`: The core Python implementation of the `HashTable` and `custom_hash` functions.
* [cite_start]`2505.16133v4.pdf`: The original research paper: *Hash-RAG: Bridging Deep Hashing with Retriever for Efficient, Fine-grained Retrieval and Augmented Generation*.
* [cite_start]`RAG_explaine.pdf`: Hebrew documentation detailing specific implementation logic and student credentials[cite: 419, 422].

---

## 🚦 Getting Started
Run the demonstration script to test the retriever:
```bash
python RAG.py
