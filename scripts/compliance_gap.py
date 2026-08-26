import os
import sys
import json
import uuid
import pandas as pd
import requests
import dotenv
from datetime import datetime

# Reconfigure stdout for UTF-8 on Windows shell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "scripts" else current_dir
base_dir = os.path.dirname(buoi17_dir)
outputs_dir = os.path.join(buoi17_dir, "outputs")
os.makedirs(outputs_dir, exist_ok=True)

# Load environment variables
dotenv.load_dotenv(os.path.join(buoi17_dir, ".env"))
dotenv.load_dotenv(os.path.join(base_dir, ".env"))

sys.path.append(buoi17_dir)
try:
    from scripts.secure_retrieval_adapter import SecureRetrievalAdapter
    from scripts.ollama_adapter import OllamaClient
except ImportError:
    from secure_retrieval_adapter import SecureRetrievalAdapter
    from ollama_adapter import OllamaClient

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-3.6-flash")

CSV_RESULTS_FILE = os.path.join(outputs_dir, "compliance_gap_results.csv")
CSV_SCHEMA_HEADERS = [
    "gap_id",
    "external_document_id",
    "external_chunk_id",
    "external_requirement",
    "external_citation",
    "internal_document_id",
    "internal_chunk_id",
    "internal_evidence",
    "internal_citation",
    "classification",
    "reason",
    "confidence",
    "review_status",
    "request_id"
]

class ComplianceGapChecker:
    """
    AI Compliance Gap Checker for Buổi 17 / Buổi 19.
    Compares External Requirements (e.g. NHNN Circulars) vs Internal Policies.
    Enforces Strict Audit & Governance Rules:
    - All outputs marked as NEEDS_HUMAN_REVIEW.
    """
    def __init__(self, csv_path: str = None):
        self.adapter = SecureRetrievalAdapter(csv_path)
        self.df_corpus = self.adapter.df_corpus
        
        self.internal_docs = []
        self.external_docs = []
        
        for did, group in self.df_corpus.groupby('document_id'):
            row = group.iloc[0]
            cq = str(row.get('co_quan_ban_hanh', '')).lower()
            title = str(row.get('title', '')).lower()
            loai = str(row.get('document_type', row.get('loai_van_ban', ''))).lower()
            
            is_external_agency = any(k in cq for k in ['ngân hàng nhà nước', 'quốc hội', 'chính phủ', 'bộ tài chính'])
            is_external_type = any(k in loai or k in title for k in ['thông tư', 'nghị định', 'luật', 'văn bản hợp nhất'])
            
            is_internal = ('agribank' in cq or 'agribank' in title or 'quy định nội bộ' in title) and not (is_external_agency or is_external_type)
            
            if is_internal:
                self.internal_docs.append(did)
            else:
                self.external_docs.append(did)
                
        self.is_data_ready = len(self.internal_docs) > 0 and len(self.external_docs) > 0

    def inspect_data_readiness(self) -> dict:
        return {
            "total_documents": len(self.df_corpus['document_id'].unique()),
            "external_docs_count": len(self.external_docs),
            "internal_docs_count": len(self.internal_docs),
            "is_data_ready": self.is_data_ready,
            "status": "COMPLIANCE_GAP_DATA_READY" if self.is_data_ready else "COMPLIANCE_GAP_DATA_INSUFFICIENT",
            "message": "Sẵn sàng phân tích gap" if self.is_data_ready else "DATA GAP: INTERNAL POLICY NOT FOUND trong tập dữ liệu nguồn."
        }

    def analyze_gap(self, external_requirement_chunk: dict, user_role: str = "Risk_Manager") -> dict:
        """
        Analyzes a single external requirement chunk against internal policies using configured LLM_PROVIDER.
        """
        req_id = str(uuid.uuid4())
        gap_id = f"GAP_{uuid.uuid4().hex[:8].upper()}"

        ext_did = external_requirement_chunk.get("document_id", "N/A")
        ext_cid = external_requirement_chunk.get("chunk_id", "N/A")
        ext_req_text = external_requirement_chunk.get("text", "")
        ext_cit = external_requirement_chunk.get("citation", f"[{ext_did} | {ext_cid}]")

        if not self.is_data_ready:
            record = {
                "gap_id": gap_id,
                "external_document_id": ext_did,
                "external_chunk_id": ext_cid,
                "external_requirement": ext_req_text[:150],
                "external_citation": ext_cit,
                "internal_document_id": "N/A",
                "internal_chunk_id": "N/A",
                "internal_evidence": "Không tìm thấy dữ liệu quy định nội bộ trong corpus",
                "internal_citation": "N/A",
                "classification": "CHUA_DU_BANG_CHUNG",
                "reason": "Corpus nguồn khuyết thiếu tập dữ liệu INTERNAL_POLICY. Không gán nhầm hoặc tự bịa kết luận.",
                "confidence": 0.0,
                "review_status": "NEEDS_HUMAN_REVIEW",
                "request_id": req_id
            }
            return record

        retrieval_res = self.adapter.retrieve(
            question=ext_req_text[:200],
            user_roles=[user_role],
            method="bm25",
            top_k=3
        )
        candidates = retrieval_res.get("results", [])

        internal_candidates = [c for c in candidates if c.get("document_id") in self.internal_docs]

        if not internal_candidates:
            record = {
                "gap_id": gap_id,
                "external_document_id": ext_did,
                "external_chunk_id": ext_cid,
                "external_requirement": ext_req_text[:150],
                "external_citation": ext_cit,
                "internal_document_id": "N/A",
                "internal_chunk_id": "N/A",
                "internal_evidence": "Retriever chưa tìm thấy trích dẫn nội bộ tương ứng trong phạm vi được xem",
                "internal_citation": "N/A",
                "classification": "CHUA_DU_BANG_CHUNG",
                "reason": "Chưa đủ bằng chứng để xác định ĐÁP ỨNG hay THIẾU. Yêu cầu chuyên viên kiểm toán review thủ công.",
                "confidence": 0.5,
                "review_status": "NEEDS_HUMAN_REVIEW",
                "request_id": req_id
            }
            return record

        top_match = internal_candidates[0]
        
        # Determine LLM Provider
        provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        classification = "CHENH_LECH"
        reason = "Phát hiện quy định nội bộ tương ứng nhưng cần đánh giá lại mức độ đáp ứng."

        if provider == "ollama":
            client = OllamaClient()
            prompt = f"""So sánh yêu cầu quy định ngoại bối với quy định nội bộ:
Yêu cầu ngoại bối: {ext_req_text[:200]}
Bằng chứng nội bộ: {top_match.get("text", "")[:200]}

Trả về JSON có dạng: {{"classification": "DAP_UNG"|"CHENH_LECH"|"KHONG_DAP_UNG", "reason": "Mô tả chi tiết"}}"""
            llm_res = client.generate(prompt, format_json=True, temperature=0.1)
            if isinstance(llm_res, dict):
                classification = llm_res.get("classification", classification)
                reason = llm_res.get("reason", reason)

        record = {
            "gap_id": gap_id,
            "external_document_id": ext_did,
            "external_chunk_id": ext_cid,
            "external_requirement": ext_req_text[:150],
            "external_citation": ext_cit,
            "internal_document_id": top_match.get("document_id"),
            "internal_chunk_id": top_match.get("chunk_id"),
            "internal_evidence": top_match.get("text", "")[:150],
            "internal_citation": top_match.get("citation"),
            "classification": classification,
            "reason": reason,
            "confidence": 0.85,
            "review_status": "NEEDS_HUMAN_REVIEW", # Mandatory Guardrail
            "request_id": req_id
        }
        return record

def export_initial_gap_results_csv():
    """
    Ensures outputs/compliance_gap_results.csv is initialized with clean headers.
    """
    checker = ComplianceGapChecker()
    status_info = checker.inspect_data_readiness()
    
    df_empty = pd.DataFrame(columns=CSV_SCHEMA_HEADERS)
    
    if not status_info["is_data_ready"]:
        sample_gap = {
            "gap_id": "GAP_DATA_INSUFFICIENT",
            "external_document_id": "N/A",
            "external_chunk_id": "N/A",
            "external_requirement": "Dữ liệu nguồn khuyết thiếu tập dữ liệu INTERNAL_POLICY",
            "external_citation": "N/A",
            "internal_document_id": "N/A",
            "internal_chunk_id": "N/A",
            "internal_evidence": "N/A",
            "internal_citation": "N/A",
            "classification": "CHUA_DU_BANG_CHUNG",
            "reason": "DATA GAP: INTERNAL POLICY NOT FOUND trong corpus. Không kết luận compliance.",
            "confidence": 0.0,
            "review_status": "NEEDS_HUMAN_REVIEW",
            "request_id": str(uuid.uuid4())
        }
        df_empty = pd.DataFrame([sample_gap], columns=CSV_SCHEMA_HEADERS)
        
    df_empty.to_csv(CSV_RESULTS_FILE, index=False, encoding="utf-8-sig")
    print(f"Exported Compliance Gap Results CSV -> {CSV_RESULTS_FILE}")
    return status_info

if __name__ == "__main__":
    info = export_initial_gap_results_csv()
    print("Data Readiness Status:", info)
