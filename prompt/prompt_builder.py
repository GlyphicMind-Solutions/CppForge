# /CppForge/prompt/prompt_builder.py
# CppForge Prompt Builder (model-family aware)
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import re
from typing import Tuple



# ==========================
# PROMPT BUILDER CLASS
# ==========================
class PromptBuilder:
    """
    PromptBuilder
        -Builds model-family-aware prompts for CppForge.
        -Output: C++ code ONLY. No markdown. End with FIN~.
        -Supports multi-file output (.hpp + .cpp) when appropriate.
        -Header style is user-driven (CppForge does not enforce .hpp vs .h).
    """

    # ---------------
    # Build Prompt
    # ---------------
    def build_prompt(self, topic: str, model_key: str) -> str:
        family = self._infer_family(model_key)

        if family == "gpt":
            return self._build_gpt_prompt(topic)
        if family == "mistral":
            return self._build_mistral_prompt(topic)
        if family == "qwen":
            return self._build_qwen_prompt(topic)
        if family == "deepseek":
            return self._build_deepseek_prompt(topic)
        if family == "phi":
            return self._build_phi_prompt(topic)

        # default → llama-style
        return self._build_llama_prompt(topic)

    # ---------------
    # Infer Family
    # ---------------
    def _infer_family(self, model_key: str) -> str:
        k = model_key.lower()

        if "gpt" in k:
            return "gpt"
        if "mistral" in k:
            return "mistral"
        if "qwen" in k:
            return "qwen"
        if "deepseek" in k:
            return "deepseek"
        if "phi" in k:
            return "phi"
        if "llama" in k or "hermes" in k:
            return "llama"

        return "llama"

# ==================================== #
# Template Section                     #
# ==================================== #
    # ---------------
    # GPT template
    # ---------------
    def _build_gpt_prompt(self, topic: str) -> str:
        return (
            "<|start|>system<|message|>\n"
            "\"You are an Agent using CppForge. Generate C++ code ONLY. No markdown. No explanations. End with FIN~.\"\n"
            "\"Rules:\"\n"
            "\"1. All reasoning must stay inside the assistant analysis channel.\"\n"
            "\"2. Final output must be pure C++ code inside the assistant final channel.\"\n"
            "\"3. If the user requests or implies multiple files, output ALL required .cpp and header files.\"\n"
            "\"4. Header style (.hpp, .h, .hh, .hxx) is user-driven.\"\n"
            "\"5. When generating classes, produce both header and source unless user requests single-file.\"\n"
            "<|end|>\n\n"
            "<|start|>user<|message|>\n"
            f"{topic}\n"
            "<|end|>\n\n"
            "<|start|>assistant<|channel|>analysis<|message|>\n"
            "...\n"
            "<|end|>\n\n"
            "<|start|>assistant<|channel|>final<|message|>\n"
        )

    # ---------------
    # Mistral template
    # ---------------
    def _build_mistral_prompt(self, topic: str) -> str:
        return (
            "<|im_start|>system\n"
            "[INST]\n"
            "You are an Agent using CppForge. Generate C++ code ONLY. No markdown. End with FIN~.\n"
            "If classes are generated, produce both header and source files.\n"
            "Header style is user-driven.\n"
            "[/INST]\n"
            "<|im_end|>\n\n"
            "<|im_start|>user\n"
            f"{topic}\n"
            "<|im_end|>\n\n"
            "<|im_start|>assistant\n"
        )

    # ---------------
    # Qwen template
    # ---------------
    def _build_qwen_prompt(self, topic: str) -> str:
        return (
            "<|im_start|>system\n"
            "You are an Agent using CppForge. Generate C++ code ONLY. No markdown. End with FIN~.\n"
            "Support multi-file output (.hpp + .cpp) when appropriate.\n"
            "Header style is user-driven.\n"
            "<|im_end|>\n\n"
            "<|im_start|>user\n"
            f"{topic}\n"
            "<|im_end|>\n\n"
            "<|im_start|>assistant\n"
        )

    # ---------------
    # DeepSeek template
    # ---------------
    def _build_deepseek_prompt(self, topic: str) -> str:
        return (
            "<|begin_of_text|><|system|>\n"
            "You are an Agent using CppForge. Generate C++ code ONLY. No markdown. End with FIN~.\n"
            "Generate header + source files when classes are present.\n"
            "Header style (.hpp/.h/.hh/.hxx) is determined by user instructions.\n"
            "<|end|>\n\n"
            "<|user|>\n"
            f"{topic}\n"
            "<|end|>\n\n"
            "<|assistant|>\n"
        )

    # ---------------
    # Phi template
    # ---------------
    def _build_phi_prompt(self, topic: str) -> str:
        return (
            "### System\n"
            "You are an Agent using CppForge. Generate C++ code ONLY. No markdown. End with FIN~.\n"
            "Support multi-file output when needed.\n"
            "Header style is user-driven.\n\n"
            "### User\n"
            f"{topic}\n\n"
            "### Assistant\n"
        )

    # ---------------
    # Llama / default template
    # ---------------
    def _build_llama_prompt(self, topic: str) -> str:
        return (
            "<|im_start|>system\n"
            "You are an Agent using CppForge. Generate C++ code ONLY. No markdown. End with FIN~.\n"
            "If classes are generated, output both header and source files.\n"
            "Header style is user-driven.\n"
            "<|im_end|>\n\n"
            "<|im_start|>user\n"
            f"{topic}\n"
            "<|im_end|>\n\n"
            "<|im_start|>assistant\n"
        )

# ==================================== #
# Helpers Section                      #
# ==================================== #
    # ---------------------------
    # Split GPT OUTPUT
    # ---------------------------
    @staticmethod
    def split_gpt_oss_output(text: str) -> Tuple[str, str]:
        """
        Removes GPT's "thinking" and returns only the "Answer:" section.
        """
        t = text.replace("\r", "")
        match = re.search(r"\bAnswer:\b", t, re.IGNORECASE)

        if not match:
            return "", t.strip()

        idx = match.start()
        thoughts = t[:idx].replace("Thinking:", "").strip()
        content = t[idx:].replace("Answer:", "").strip()
        return thoughts, content
