import os
import sys
import json
import uuid
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir)
outputs_dir = os.path.join(buoi17_dir, "outputs")
os.makedirs(outputs_dir, exist_ok=True)

AUDIT_LOG_FILE = os.path.join(outputs_dir, "audit_log.jsonl")

def log_audit_trail(
    user_role: str,
    question: str,
    retrieved_chunks: list,
    filtered_out_count: int,
    access_scope: str,
    answer_status: str,
    answer: str,
    request_id: str = None
) -> dict:
    """
    Logs every AI internal lookup request into audit_log.jsonl.
    Preserves full auditability (User Role, Question, Access Scope, Citations, Timestamp, Status).
    """
    if not request_id:
        request_id = str(uuid.uuid4())

    log_entry = {
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "user_role": user_role,
        "question": question,
        "access_scope": access_scope,
        "filtered_out_count": filtered_out_count,
        "retrieved_count": len(retrieved_chunks),
        "retrieved_chunks": [
            {
                "chunk_id": item.get("chunk_id"),
                "document_id": item.get("document_id"),
                "citation": item.get("citation")
            } for item in retrieved_chunks
        ],
        "answer_status": answer_status,
        "answer_snippet": str(answer)[:150]
    }

    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[AUDIT LOG ERROR]: Failed to write audit trail: {e}")

    return log_entry

if __name__ == "__main__":
    print("Testing audit_logger...")
    e = log_audit_trail("Staff", "Test query", [], 0, "Test scope", "TEST", "Test answer")
    print("Logged entry:", e["request_id"])
