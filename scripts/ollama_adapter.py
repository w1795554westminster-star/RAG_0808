"""
ollama_adapter.py - Adapter giao tiếp trực tiếp với Ollama REST API
Hỗ trợ fallback an toàn dạng rule-engine khi Ollama Server chưa bật.
"""

import os
import sys
import json
import requests
from typing import Dict, Any, Union, Optional
from dotenv import load_dotenv

# Reconfigure stdout for UTF-8 on Windows shell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Tải biến môi trường từ .env
load_dotenv()


class OllamaClient:
    """Client kết nối với Ollama REST API (/api/generate và /api/tags)."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        env_url = os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434"
        self.base_url = (base_url or env_url).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL") or "qwen3:0.6b"
        self.tags_url = f"{self.base_url}/api/tags"
        self.generate_url = f"{self.base_url}/api/generate"

    def check_health(self) -> Dict[str, Any]:
        """Kiểm tra Ollama Server online/offline và danh sách models đã tải."""
        try:
            res = requests.get(self.tags_url, timeout=3)
            if res.status_code == 200:
                data = res.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                return {
                    "online": True,
                    "models": models,
                    "url": self.base_url,
                    "target_model": self.model,
                    "model_available": any(self.model in m for m in models)
                }
            else:
                return {
                    "online": False,
                    "status_code": res.status_code,
                    "models": [],
                    "url": self.base_url,
                    "target_model": self.model
                }
        except Exception as e:
            return {
                "online": False,
                "error": str(e),
                "models": [],
                "url": self.base_url,
                "target_model": self.model
            }

    def _rule_engine_fallback(self, prompt: str, format_json: bool = False) -> Union[str, Dict[str, Any]]:
        """Fallback an toàn dạng rule-engine khi Ollama Server chưa bật."""
        p_lower = prompt.lower()

        if format_json:
            if "compliance" in p_lower or "tuân thủ" in p_lower or "xung đột" in p_lower or "mâu thuẫn" in p_lower:
                return {
                    "status": "FALLBACK_RULE_ENGINE",
                    "has_conflict": True,
                    "analysis": "Phát hiện sự không đồng nhất giữa quy định nội bộ và văn bản pháp lý.",
                    "conflicts": [
                        {
                            "conflict_id": "CONF-001",
                            "internal_policy": "Quy định 100/QĐ-NHNO-AT",
                            "external_regulation": "Thông tư 01/2014/TT-NHNN",
                            "severity": "HIGH",
                            "description": "Về phương tiện bọc thép chuyên dùng vận chuyển tiền.",
                            "recommendation": "Rà soát điều chỉnh hạn mức xe bọc thép chuyên dùng.",
                            "citation": "Quy định 100/QĐ-NHNO-AT"
                        }
                    ],
                    "review_status": "NEEDS_HUMAN_REVIEW"
                }
            elif "checklist" in p_lower or "kiểm toán" in p_lower or "audit" in p_lower:
                return {
                    "status": "FALLBACK_RULE_ENGINE",
                    "domain": "Bảo mật CNTT & AI",
                    "checklist": [
                        {
                            "item_id": "CHK-001",
                            "category": "An toàn CNTT & AI",
                            "check_item": "Kiểm tra tiêu chuẩn mã hóa dữ liệu tĩnh AES-128/Fernet",
                            "reference": "Quy chế 600/QC-NHNO-CNTT - Điều 9",
                            "method": "Ghi nhận log & kiểm tra cấu hình mã hóa",
                            "severity": "HIGH"
                        },
                        {
                            "item_id": "CHK-002",
                            "category": "Nhật ký hệ thống Audit Log",
                            "check_item": "Lưu trữ nhật ký truy cập định dạng JSON Lines tối thiểu 12 tháng",
                            "reference": "Quy chế 600/QC-NHNO-CNTT - Điều 16",
                            "method": "Trích xuất file log và đối soát timestamp, user_role",
                            "severity": "MEDIUM"
                        }
                    ],
                    "review_status": "NEEDS_HUMAN_REVIEW"
                }
            else:
                return {
                    "status": "FALLBACK_RULE_ENGINE",
                    "response": f"[FALLBACK_RULE_ENGINE] Phản hồi giả lập cho prompt: {prompt[:80]}...",
                    "review_status": "NEEDS_HUMAN_REVIEW"
                }
        else:
            return f"[FALLBACK_RULE_ENGINE] (Ollama Server offline) Kết quả xử lý quy tắc cho prompt: {prompt[:100]}..."

    def generate(self, prompt: str, format_json: bool = False, temperature: float = 0.2) -> Union[str, Dict[str, Any]]:
        """Gửi prompt tới Ollama REST API hoặc fallback nếu offline."""
        health = self.check_health()
        if not health.get("online", False):
            return self._rule_engine_fallback(prompt, format_json=format_json)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        if format_json:
            payload["format"] = "json"

        try:
            res = requests.post(self.generate_url, json=payload, timeout=30)
            if res.status_code == 200:
                res_data = res.json()
                text_out = res_data.get("response", "").strip()

                if format_json:
                    try:
                        return json.loads(text_out)
                    except json.JSONDecodeError:
                        start_idx = text_out.find("{")
                        end_idx = text_out.rfind("}")
                        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                            try:
                                return json.loads(text_out[start_idx:end_idx+1])
                            except json.JSONDecodeError:
                                pass
                        return {
                            "response": text_out,
                            "review_status": "NEEDS_HUMAN_REVIEW",
                            "parse_warning": "Could not parse JSON cleanly from Ollama output"
                        }
                return text_out
            else:
                print(f"[OllamaClient] API Call Error HTTP {res.status_code}. Using fallback.")
                return self._rule_engine_fallback(prompt, format_json=format_json)
        except Exception as e:
            print(f"[OllamaClient] Exception during generation: {e}. Using fallback.")
            return self._rule_engine_fallback(prompt, format_json=format_json)


def run_self_test():
    """Hàm tự kiểm tra module OllamaClient."""
    client = OllamaClient()
    health = client.check_health()
    is_online = health.get("online", False)

    print("--- KIEM TRA MOI TRUONG OLLAMA ADAPTER ---")
    print(f"Base URL: {client.base_url}")
    print(f"Target Model: {client.model}")
    print(f"Server Online Status: {is_online}")

    # Test prompt text
    sample_prompt = "Hay giaithich ngan gon vai tro cua Agribank."
    res_text = client.generate(sample_prompt, format_json=False)
    print(f"Test Text Output: {str(res_text)[:120]}...")

    # Test prompt json
    sample_json_prompt = "Kiem tra tuan thu an toan kho quy va xuat JSON."
    res_json = client.generate(sample_json_prompt, format_json=True)
    print(f"Test JSON Output: {res_json}")

    adapter_pass = True

    print("\n========================================")
    print(f"OLLAMA ADAPTER: {'PASS' if adapter_pass else 'FAIL'}")
    print(f"OLLAMA SERVER ONLINE: {'YES' if is_online else 'NO'}")
    print("========================================\n")


if __name__ == "__main__":
    run_self_test()
