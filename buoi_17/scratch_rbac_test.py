import pandas as pd
import json
import os, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r'd:\03.08\buoi_16')
from src.secure_retriever import SecureRetriever, is_role_authorized

csv_path = r'd:\03.08\buoi_16\data\processed\chunks_secure.csv'
df = pd.read_csv(csv_path)

print('=== 1. PARSING ALLOWED_ROLES & ROLE STATISTICS ===')
parse_errors = 0
role_counts = Counter()
multi_role_chunks = 0
restricted_chunks = 0
role_set_distribution = Counter()

parsed_roles_series = []

for idx, row in df.iterrows():
    raw_val = row['allowed_roles']
    try:
        if isinstance(raw_val, str):
            roles = json.loads(raw_val)
        elif isinstance(raw_val, (list, tuple)):
            roles = list(raw_val)
        else:
            roles = [str(raw_val)]
    except Exception as e:
        parse_errors += 1
        roles = []
    
    parsed_roles_series.append(roles)
    roles_lower = [r.strip() for r in roles]
    
    if len(roles) > 1:
        multi_role_chunks += 1
    if 'Guest' not in roles:
        restricted_chunks += 1
        
    for r in roles_lower:
        role_counts[r] += 1
        
    role_set_key = tuple(sorted(roles_lower))
    role_set_distribution[role_set_key] += 1

print(f'Total chunks: {len(df)}')
print(f'Parsing errors: {parse_errors} (Stability: 100% PASS if 0)')
print(f'Unique roles found: {list(role_counts.keys())}')
print(f'Chunk count per role:')
for role, cnt in role_counts.most_common():
    print(f'  - {role}: {cnt} chunks ({cnt/len(df)*100:.1f}%)')

print(f'\nMulti-role chunks (>1 role): {multi_role_chunks} ({multi_role_chunks/len(df)*100:.1f}%)')
print(f'Restricted/Sensitive chunks (Guest not allowed): {restricted_chunks} ({restricted_chunks/len(df)*100:.1f}%)')

print(f'\nRole Set Combinations (Top 5):')
for rset, cnt in role_set_distribution.most_common(5):
    print(f'  - {list(rset)}: {cnt} chunks')

print('\n=== 2. UNKNOWN ROLE TEST (DEFAULT DENY) ===')
unknown_auth_count = sum(1 for r in parsed_roles_series if is_role_authorized(r, ['UnknownRole_XYZ']))
print(f'Chunks authorized for UnknownRole_XYZ: {unknown_auth_count} (Default Deny: PASS if 0)')

print('\n=== 3. SECURERETRIEVER QUERY EXECUTION FOR 5 ROLES ===')
retriever = SecureRetriever(df)
test_query = 'Quy định bảo quản và vận chuyển tiền mặt, tài sản quý'
roles_to_test = ['Admin', 'HR', 'Risk_Manager', 'Staff', 'Guest', 'UnknownRole']

for role in roles_to_test:
    results, filtered_out = retriever.retrieve(test_query, user_roles=[role], method='hybrid_rerank', top_k=3)
    print(f'\nRole [{role}]:')
    print(f'  - Authorized corpus subset size: {len(df) - filtered_out} / {len(df)}')
    print(f'  - Total chunks filtered out (denied): {filtered_out}')
    print(f'  - Top {len(results)} retrieved chunks:')
    for item in results:
        r_rank = item['rank']
        r_cid = item['chunk_id']
        r_did = item['document_id']
        r_score = item['score']
        r_roles = item.get('allowed_roles')
        print(f'    * Rank {r_rank}: chunk_id={r_cid}, doc_id={r_did}, score={r_score:.4f}')
        print(f'      allowed_roles={r_roles}')

# Test also with buoi_17/data/chunks_combined_secure.csv if needed
b17_csv = r'd:\03.08\buoi_17\data\chunks_combined_secure.csv'
if os.path.exists(b17_csv):
    df_b17 = pd.read_csv(b17_csv)
    print('\n=== 4. TESTING BUOI_17 CHUNKS_COMBINED_SECURE.CSV (811 CHUNKS) ===')
    retriever_b17 = SecureRetriever(df_b17)
    for role in ['Admin', 'HR', 'Risk_Manager', 'Staff', 'Guest']:
        res, filt = retriever_b17.retrieve(test_query, user_roles=[role], method='hybrid_rerank', top_k=3)
        print(f'Role [{role}]: Authorized={len(df_b17)-filt}/{len(df_b17)}, FilteredOut={filt}, Top1={res[0]["chunk_id"] if res else "None"}')
