# CppForge — C++ Code Forge  

Created By: **David Kistner (Unconditional Love)**  
GlyphicMind Solutions LLC  

CppForge is a local‑first C++ code generation and refactoring tool built on the GlyphicMind Forge architecture.  
It provides a full IDE‑style workflow powered by local `.gguf` models via `llama_cpp_python`, including:

- Model‑family‑aware prompt building  
- Multi‑file C++ output (`.cpp` + `.hpp` / `.h` / `.hh` / `.hxx`)  
- Deep Analysis v2 (chunk → summarize → meta‑summarize → reconstruct)  
- Tabbed GUI with staging, master code, and logs  
- Brand‑tagged file forging into `storage/pending`  
- Full local control — no cloud dependencies  

CppForge is part of the **Forge Suite**, alongside PythonForge, CSharpForge, JavaScriptForge, and more.

---

## Features

### 🔥 Local‑First LLM Execution

CppForge loads `.gguf` models defined in:
models/manifest.yaml

Supports:
- GPT‑OSS  
- Mistral  
- Llama  
- Qwen  
- DeepSeek  
- Phi  
- Any LocalAI‑compatible `.gguf` model  

---

### 🧠 Deep Analysis v2

CppForge includes the upgraded Deep Analysis engine:

- Splits large codebases into chunks  
- Summarizes each chunk  
- Produces a meta‑summary  
- Reconstructs/refactors the entire project  
- Logs every step in the Deep Analysis Log tab  

---

### 🧩 Multi‑File C++ Output

CppForge automatically detects and writes multiple files when the model outputs:

```cpp
// FILE: MyClass.hpp
// FILE: MyClass.cpp

```

Header style is user‑driven, not enforced.

---

### 🖥️ Full GUI (PyQt5)

--Tabbed IDE layout:

- Topic / Corrections

- Raw LLM Output

- Extracted Code

- Master Code

- Deep Analysis Log

- Global controls:

- Generate

- Re‑run with Corrections

- Deep Analysis

- Open File

- Save File

- Forge → Pending

- Clear Session

---

### 🗂️ Storage System

CppForge organizes output into:

```
storage/
    pending/   ← forged files awaiting review
    saved/     ← user‑saved files
    logs/      ← forge.log + deep analysis logs

```

---

### Installation

1. Create a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate

```
2. Install dependencies
```
pip install -r requirements.txt

```
3. Add your .gguf models
- Place them in:
```
models/

```
- Then update:

```
models/manifest.yaml

```

---

### Running CppForge

```
python3 cppforge.py

```

---

### Model Manifest Example

```
models:
  mistral_default:
    path: ./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf   <---- you can change this to your direct model location
    n_ctx: 32768
    template: mistral
```

---

### Part of the GlyphicMind Forge Suite

- CppForge is one of many Forge tools:

1. PythonForge
2. CSharpForge
3. JavaScriptForge
4. CppForge
5. RustForge (coming)
6. GoForge (coming)
7. HTML/CSS Forge
8. SQLForge


### License

This project is part of the GlyphicMind Solutions ecosystem.
All rights reserved.
view license in the directory for more.
