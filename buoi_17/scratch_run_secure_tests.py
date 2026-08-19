import os
import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r'd:\03.08\buoi_17')
from scripts.secure_retrieval_adapter import SecureRetrievalAdapter

adapter = SecureRetrievalAdapter(r'd:\03.08\buoi_16\data\processed\chunks_secure.csv')
df = adapter.df_corpus

print('=== SECURE RETRIEVAL SUITE TEST ===')

# Pick restricted chunk 44209_chunk_021 (allowed for Staff/Risk_Manager, but NOT Guest)
target_cid = '44209_chunk_021'
matched_row = df[df['chunk_id'] == target_cid].iloc[0]

print("Target Restricted Chunk:")
print(f"  - chunk_id: {matched_row['chunk_id']}")
print(f"  - document_id: {matched_row['document_id']}")
print(f"  - title: {matched_row['title']}")
print(f"  - allowed_roles: {matched_row['allowed_roles']}")

query = "Bảo quản tài sản tại quầy giao dịch và trong kho tiền nghỉ buổi trưa"
print(f"\nTest Query: '{query}'")

# Test 1: Authorized Role (Staff)
res_staff = adapter.retrieve(query, user_roles=['Staff'], method='bm25', top_k=5)
staff_cids = [item['chunk_id'] for item in res_staff['results']]
test1_pass = target_cid in staff_cids
print(f"\n[TEST 1] Authorized Role ('Staff') received chunk {target_cid}: {test1_pass} (Found at Rank: {staff_cids.index(target_cid)+1 if test1_pass else 'N/A'})")

# Test 2: Unauthorized Role (Guest)
res_guest = adapter.retrieve(query, user_roles=['Guest'], method='bm25', top_k=5)
guest_cids = [item['chunk_id'] for item in res_guest['results']]
test2_pass = target_cid not in guest_cids
print(f"[TEST 2] Unauthorized Role ('Guest') denied chunk {target_cid}: {test2_pass} (Guest Top 5 CIDs: {guest_cids})")

# Test 3: No Unauthorized Chunk in Context
test3_pass = True
unauth_found_count = 0
for role in ['Guest', 'HR', 'Staff', 'Risk_Manager']:
    res_role = adapter.retrieve("quy trình kho quỹ và vận chuyển tiền", user_roles=[role], method='bm25', top_k=5)
    for item in res_role['results']:
        roles_item = item['allowed_roles']
        if role not in roles_item:
            test3_pass = False
            unauth_found_count += 1

print(f"[TEST 3] Unauthorized Chunks in Context: {unauth_found_count} (PASS if 0): {test3_pass}")

# Test 4: Preservation of Metadata (chunk_id, document_id, citation, title, article, access_decision, etc.)
res_check = adapter.retrieve("bảo quản tài sản", user_roles=['Admin'], method='bm25', top_k=3)
test4_pass = True
missing_keys = []
for item in res_check['results']:
    for key in ['rank', 'chunk_id', 'document_id', 'title', 'article', 'citation', 'allowed_roles', 'access_decision', 'retrieval_method']:
        if key not in item or item[key] is None or item[key] == '':
            test4_pass = False
            missing_keys.append(f"{key} in {item.get('chunk_id')}")

print(f"[TEST 4] Metadata & Citation Preserved (chunk_id, document_id, citation, access_decision...): {test4_pass}")
if missing_keys:
    print(f"  Missing fields: {missing_keys}")

print("\n--- SUMMARY FOR REPORT ---")
print(f"SECURE RETRIEVAL REUSE: {'PASS' if test1_pass and test2_pass else 'FAIL'}")
print(f"NO UNAUTHORIZED CONTEXT: {'PASS' if test3_pass else 'FAIL'}")
print(f"CITATION PRESERVED: {'PASS' if test4_pass else 'FAIL'}")
