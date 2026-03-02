# =============================================================================
# CORTICAL ENGINE: Phi-3.5-mini-instruct (Native FP16)
# =============================================================================
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

LLM_MODEL_ID = "microsoft/Phi-3.5-mini-instruct"
MAX_NEW_TOKENS = 250
TEMPERATURE = 0.7
TOP_P = 0.9

class ResponseGenerator:
    """
    The Neural Cortex: Loads Phi-3.5 in native FP16.
    Bypasses CPU RAM bottleneck for smooth T4 GPU operation.
    """
    def __init__(self):
        print("   ⚡ Initializing Cortical Engine...")
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_ID,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        print("   ✅ Cortical Engine Online")
    
    def generate(self, prompt: str) -> str:
        """Generate response with proper memory management."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if response.startswith(prompt):
            response = response[len(prompt):].lstrip()
        return response
