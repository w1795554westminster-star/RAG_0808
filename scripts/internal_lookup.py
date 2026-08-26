import os
import sys
import json
import uuid
import requests
import dotenv
from datetime import datetime

# Reconfigure stdout for UTF-8 on Windows shell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "scripts" else current_dir
base_dir = os.path.dirname(buoi17_dir)

# Load environment variables
dotenv.load_dotenv(os.path.join(buoi17_dir, ".env"))
dotenv.load_dotenv(os.path.join(base_dir, ".env"))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from scripts.secure_retrieval_adapter import SecureRetrievalAdapter
    from scripts.audit_logger import log_audit_trail
    from scripts.ollama_adapter import OllamaClient
except ImportError:
    from secure_retrieval_adapter import SecureRetrievalAdapter
    from audit_logger import log_audit_trail
    from ollama_adapter import OllamaClient

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-3.6-flash")

FALLBACK_MESSAGE = "Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập."

class InternalLookupService:
    def __init__(self, csv_path: str = None):
        self.adapter = SecureRetrievalAdapter(csv_path)

    def _call_llm(self, prompt: str, context_chunks: list) -> str:
        """
        Calls configured LLM Provider (Ollama or Gemini) with direct answer synthesis fallback.
        """
        provider = os.getenv("LLM_PROVIDER", "ollama").lower()

        if provider == "ollama":
            print(f"[InternalLookup] Using LLM_PROVIDER=ollama (Model: {os.getenv('OLLAMA_MODEL', 'qwen3:0.6b')})")
            client = OllamaClient()
            res = client.generate(prompt, format_json=False, temperature=0.1)
            if res and FALLBACK_MESSAGE not in res:
                return str(res)
            return self._synthesize_direct_answer(context_chunks)

        # Gemini Provider
        print(f"[InternalLookup] Using LLM_PROVIDER=gemini (Model: {MODEL_NAME})")
        if not GEMINI_API_KEY:
            return self._synthesize_direct_answer(context_chunks)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024}
        }
        try:
            r = requests.post(url, json=payload, timeout=8)
            if r.status_code == 200:
                data = r.json()
                text_res = data['candidates'][0]['content']['parts'][0]['text'].strip()
                if not text_res or "không tìm thấy" in text_res.lower():
                    return f"{FALLBACK_MESSAGE}"
                return text_res
            else:
                return self._synthesize_direct_answer(context_chunks)
        except Exception:
            return self._synthesize_direct_answer(context_chunks)

    def _synthesize_direct_answer(self, context_chunks: list) -> str:
        if not context_chunks:
            return FALLBACK_MESSAGE
        first_chunk = context_chunks[0]
        cit = first_chunk.get("citation", "")
        txt = first_chunk.get("text", "")[:250].replace('\n', ' ')
        return f"Theo quy định tại {cit}: {txt}"

    def lookup(self, question: str, user_role: str = "Guest", top_k: int = 5, method: str = "bm25") -> dict:
        """
        Main Use Case 1 function: AI Tra cứu Quy định Nội bộ.
        """
        req_id = str(uuid.uuid4())
        
        # 1. Secure Retrieval via Adapter (Pre-filtering RBAC enforced)
        retrieval_res = self.adapter.retrieve(
            question=question,
            user_roles=[user_role],
            method=method,
            top_k=top_k
        )

        retrieved_chunks = retrieval_res.get("results", [])
        total_corpus = retrieval_res.get("total_corpus_size", 0)
        auth_corpus = retrieval_res.get("authorized_corpus_size", 0)
        filtered_out = retrieval_res.get("total_filtered_out", 0)
        
        access_scope = f"Role '{user_role}' | Authorized Scope: {auth_corpus}/{total_corpus} chunks (Denied: {filtered_out})"

        # 2. Check if context is completely empty
        if not retrieved_chunks:
            answer = FALLBACK_MESSAGE
            log_audit_trail(
                user_role=user_role,
                question=question,
                retrieved_chunks=[],
                filtered_out_count=filtered_out,
                access_scope=access_scope,
                answer_status="DENIED_RBAC",
                answer=answer,
                request_id=req_id
            )
            return {
                "request_id": req_id,
                "question": question,
                "user_role": user_role,
                "access_scope": access_scope,
                "answer": answer,
                "citations": [],
                "document_ids": [],
                "chunk_ids": [],
                "retrieved_chunks": []
            }

        # 3. Build Context & Citations for LLM
        context_blocks = []
        citations_list = []
        doc_ids_set = set()
        chunk_ids_list = []

        for item in retrieved_chunks:
            cid = item['chunk_id']
            did = item['document_id']
            cit = item['citation']
            txt = item['text']

            chunk_ids_list.append(cid)
            if did: doc_ids_set.add(did)
            if cit and cit not in citations_list: citations_list.append(cit)

            context_blocks.append(f"--- CHUNK ID: {cid} | CITATION: {cit} ---\n{txt}")

        context_str = "\n\n".join(context_blocks)

        system_prompt = f"""Bạn là Trợ lý AI Tra cứu Quy định Nội bộ Ngân hàng.
Nhiệm vụ của bạn là trả lời câu hỏi của người dùng DỰA HOÀN TOÀN VÀO CÁC ĐOẠN TRÍCH VĂN BẢN ĐÃ ĐƯỢC PHÂN QUYỀN (CONTEXT) DƯỚI ĐÂY.

CÁC NGUYÊN TẮC BẮT BUỘC:
1. Chỉ sử dụng thông tin có trong phần CONTEXT. KHÔNG dùng kiến thức bên ngoài để bổ sung.
2. Nếu phần CONTEXT không chứa đủ thông tin để trả lời câu hỏi, bạn BẮT BUỘC trả lời chính xác từng từ:
"{FALLBACK_MESSAGE}"
3. Mọi thông tin trả lời phải ghi rõ trích dẫn đính kèm theo định dạng citation trong CONTEXT. KHÔNG tự bịa citation giả.
4. TUYỆT ĐỐI không được lộ hoặc suy đoán bất kỳ nội dung nào từ các văn bản bị từ chối truy cập.

CONTEXT ĐƯỢC PHÉP TRUY CẬP (ROLE: {user_role}):
{context_str}

CÂU HỎI CỦA NGƯỜI DÙNG:
{question}

CÂU TRẢ LỜI CỦA AI:"""

        # 4. Generate Answer via LLM
        llm_response = self._call_llm(system_prompt, retrieved_chunks)
        
        if FALLBACK_MESSAGE in llm_response or "Không tìm thấy đủ thông tin" in llm_response:
            answer_status = "INSUFFICIENT_CONTEXT"
            final_answer = FALLBACK_MESSAGE
        else:
            answer_status = "ANSWERED"
            final_answer = llm_response

        # 5. Log Audit Trail
        log_audit_trail(
            user_role=user_role,
            question=question,
            retrieved_chunks=retrieved_chunks,
            filtered_out_count=filtered_out,
            access_scope=access_scope,
            answer_status=answer_status,
            answer=final_answer,
            request_id=req_id
        )

        return {
            "request_id": req_id,
            "question": question,
            "user_role": user_role,
            "access_scope": access_scope,
            "answer": final_answer,
            "citations": citations_list,
            "document_ids": list(doc_ids_set),
            "chunk_ids": chunk_ids_list,
            "retrieved_chunks": retrieved_chunks
        }

if __name__ == "__main__":
    service = InternalLookupService()
    print("Testing InternalLookupService...")
    res = service.lookup("Vận chuyển tiền mặt qua đêm quy định thế nào?", user_role="Staff", top_k=3)
    print("\n--- SAMPLE TEST OUTPUT ---")
    print(f"Request ID: {res['request_id']}")
    print(f"Role: {res['user_role']}")
    print(f"Citations: {res['citations']}")
    print(f"Answer:\n{res['answer']}")
