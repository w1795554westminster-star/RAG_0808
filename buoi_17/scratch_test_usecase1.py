import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r'd:\03.08\buoi_17')
from scripts.internal_lookup import InternalLookupService

service = InternalLookupService()

test_cases = [
    {
        "id": "CASE_1",
        "name": "Tra cứu đúng quyền (Authorized Staff / Risk Manager)",
        "question": "Quy định về việc bảo quản và vận chuyển tiền mặt, tài sản quý tại quầy giao dịch và kho tiền?",
        "role": "Risk_Manager"
    },
    {
        "id": "CASE_2",
        "name": "Tra cứu ngoài phạm vi quyền (Guest - Denied Restricted Content)",
        "question": "Quy định quy trình chi tiết việc sắp xếp bảo quản tài sản tại kho tiền ngân hàng?",
        "role": "Guest"
    },
    {
        "id": "CASE_3",
        "name": "Câu hỏi không có trong dữ liệu (Insufficient Context)",
        "question": "Quy định về việc tài trợ chi phí mua sắm xe ô tô cá nhân cho cán bộ?",
        "role": "Staff"
    }
]

print("=== RUNNING USE CASE 1 TEST SUITE ===")
results = []

for case in test_cases:
    print(f"\n==========================================")
    print(f"Executing {case['id']}: {case['name']}")
    print(f"Role: {case['role']} | Question: {case['question']}")
    
    res = service.lookup(case['question'], user_role=case['role'], top_k=3, method="bm25")
    results.append(res)
    
    print(f"Request ID: {res['request_id']}")
    print(f"Scope: {res['access_scope']}")
    print(f"Document IDs: {res['document_ids']}")
    print(f"Citations count: {len(res['citations'])}")
    print(f"Citations: {res['citations']}")
    print(f"Answer:\n{res['answer']}")

print("\n=== SUMMARY VERIFICATION ===")
audit_file = r'd:\03.08\buoi_17\outputs\audit_log.jsonl'
print(f"Audit log file exists: {os.path.exists(audit_file)}")
if os.path.exists(audit_file):
    with open(audit_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"Total audit log lines written: {len(lines)}")
