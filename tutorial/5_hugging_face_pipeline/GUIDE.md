# Section 5 — Hugging Face Pipeline

---

## `hf_models_pipeline.py / .ipynb`

**What it does:**
Summarises a long paragraph using Facebook's BART model. Shows two approaches side by side:
the low-level way (tokenizer + model manually) and the high-level way (`pipeline()`).

**Things to learn:**
- What a Hugging Face `pipeline` is — a one-liner that wraps tokenizer + model + decode
- The difference between using a model manually vs using `pipeline()`
- How text summarisation works: tokenize → generate → decode
- `AutoTokenizer` and `AutoModelForSeq2SeqLM` — generic loaders that work for any model name

---

**这个文件做什么：**
使用 Facebook 的 BART 模型对一段长文字进行摘要。并排展示两种方式：
手动方式（tokenizer + model）和高级方式（`pipeline()`）。

**可以学到什么：**
- 什么是 Hugging Face `pipeline`——一行代码封装了 tokenizer、模型和解码
- 手动使用模型 vs 使用 `pipeline()` 的区别
- 文本摘要的工作流程：tokenize → generate → decode
- `AutoTokenizer` 和 `AutoModelForSeq2SeqLM`——通用加载器，适用于任何模型名称

---

## `hf_text_to_image_demo.py / .ipynb`

**What it does:**
Generates an image from a text prompt using Stable Diffusion 2.
Loads the model, sets up a scheduler, and runs inference.

**Things to learn:**
- What a diffusion model is — generates images by iteratively denoising random noise
- What a `scheduler` does — controls the denoising steps (EulerDiscreteScheduler)
- `torch_dtype=torch.float16` — uses half-precision to save GPU memory
- `.to("cuda")` / `.to("mps")` — how to move a model to a specific device
- Local vs Colab: Colab has CUDA GPU, Mac needs `mps` instead

**Known local fix:** change `pipe.to("cuda")` → `pipe.to("mps")` and `torch.float16` → `torch.float32` to run on Apple Silicon.

---

**这个文件做什么：**
使用 Stable Diffusion 2 根据文字提示生成图片。
加载模型、设置调度器并运行推理。

**可以学到什么：**
- 什么是扩散模型——通过对随机噪声逐步去噪来生成图像
- `scheduler`（调度器）的作用——控制去噪步骤（EulerDiscreteScheduler）
- `torch_dtype=torch.float16`——使用半精度浮点数以节省 GPU 显存
- `.to("cuda")` / `.to("mps")`——将模型移动到指定设备
- 本地 vs Colab 的区别：Colab 有 CUDA GPU，Mac 需要改用 `mps`

**本地运行修复：** 将 `pipe.to("cuda")` 改为 `pipe.to("mps")`，`torch.float16` 改为 `torch.float32`。
