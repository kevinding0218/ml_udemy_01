# Section 6 — LLM from Scratch

## `llm_from_scratch.py / .ipynb`

**What it does:**
Builds and trains a simple Transformer language model from scratch using PyTorch.
Loads the WikiText dataset, tokenises it, trains for 5 epochs, then generates text.

**Things to learn:**
- The core components of a Transformer: embedding, positional encoding, encoder layers, linear output
- How language model training works: predict the next word given previous words
- `DataLoader` and custom `Dataset` classes in PyTorch
- What `nn.TransformerEncoder` and `nn.TransformerEncoderLayer` do
- How to generate text from a trained model (greedy decoding with `argmax`)
- Why pretrained models (CLIP, BERT) are preferred over training from scratch

**Known fixes applied:**
- Dataset name changed from `"wikitext"` → `"Salesforce/wikitext"` (newer datasets library requires full namespace)
- Added `batch_first=True` to `TransformerEncoderLayer` to silence UserWarning

---

**这个文件做什么：**
用 PyTorch 从零构建并训练一个简单的 Transformer 语言模型。
加载 WikiText 数据集、进行 tokenize、训练 5 个 epoch，然后生成文本。

**可以学到什么：**
- Transformer 的核心组件：embedding、位置编码、encoder 层、线性输出层
- 语言模型训练的工作方式：根据前面的词预测下一个词
- PyTorch 中的 `DataLoader` 和自定义 `Dataset` 类
- `nn.TransformerEncoder` 和 `nn.TransformerEncoderLayer` 的作用
- 如何用训练好的模型生成文本（用 `argmax` 进行贪婪解码）
- 为什么实际中更常用预训练模型（如 CLIP、BERT）而非从头训练

**已修复的问题：**
- 数据集名称从 `"wikitext"` 改为 `"Salesforce/wikitext"`（新版 datasets 库需要完整命名空间）
- 给 `TransformerEncoderLayer` 加了 `batch_first=True` 以消除 UserWarning
