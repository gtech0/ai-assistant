import json
import re
from llama_cpp import Llama
from config import Config
from llm_client_prompts import _get_risk_messages, _get_ideas_messages


class LLMClient:
    def __init__(self):
        self.engine = None
        try:
            self.engine = Llama(
                model_path=Config.LLAMA_MODEL_PATH,
                n_gpu_layers=Config.LLAMA_N_GPU_LAYERS,
                n_ctx=Config.LLAMA_CONTEXT_SIZE,
                verbose=False
            )
            print("Llama-CPP Engine Loaded.")
        except Exception as e:
            print(f"Initialization Error: {e}")

    def _chat_completion(self, messages, temperature):
        if not self.engine: return ""
        try:
            output = self.engine.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=Config.LLAMA_MAX_TOKENS,
                top_p=Config.LLAMA_TOP_P,
                repeat_penalty=Config.LLAMA_REPEAT_PENALTY,
            )
            return output["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Generation Error: {e}")
            return ""

    def generate_risks(self, project_params, doc_text=""):
        messages = _get_risk_messages(project_params, doc_text)
        for _ in range(3):
            res = self._chat_completion(messages, Config.LLAMA_TEMPERATURE_RISKS)
            risks = self._parse_json_risks(res)
            if risks: return risks
        return []

    def generate_ideas(self, project_params, doc_text=""):
        messages = _get_ideas_messages(project_params, doc_text)
        res = self._chat_completion(messages, Config.LLAMA_TEMPERATURE_IDEAS)
        return res.strip().replace('**', '').replace('*', '')

    def _parse_json_risks(self, text):
        if not text:
            return []

        try:
            clean_text = re.sub(r'```json\s*|```', '', text).strip()
            data = json.loads(clean_text)

            risks_list = data.get('risks', []) if isinstance(data, dict) else []

            for r in risks_list:
                r['probability'] = float(r.get('probability', 0.5))
                r['impact'] = int(r.get('impact', 3))

            return risks_list

        except Exception as e:
            print(f"DEBUG: JSON Parsing failed: {e}")
            print(f"DEBUG: Raw text was: {text}")
            return []
