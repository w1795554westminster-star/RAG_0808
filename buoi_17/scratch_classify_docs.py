import pandas as pd
import json
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

p_sec = r'd:\03.08\buoi_16\data\processed\chunks_secure.csv'
df = pd.read_csv(p_sec)

print(f'Total chunks in CSV: {len(df)}')

# Group by document_id to list all unique documents
docs = {}
for idx, row in df.iterrows():
    did = str(row.get('document_id', '')).strip()
    if did not in docs:
        docs[did] = {
            'document_id': did,
            'title': str(row.get('title', '')).strip(),
            'so_ky_hieu': str(row.get('so_ky_hieu', '')).strip(),
            'loai_van_ban': str(row.get('document_type', row.get('loai_van_ban', ''))).strip(),
            'co_quan_ban_hanh': str(row.get('co_quan_ban_hanh', '')).strip(),
            'ngay_ban_hanh': str(row.get('ngay_ban_hanh', '')).strip(),
            'chunk_count': 0
        }
    docs[did]['chunk_count'] += 1

print(f'Total Unique Documents Found: {len(docs)}')

internal_count = 0
external_count = 0

doc_list = []

for did, info in docs.items():
    cq = info['co_quan_ban_hanh'].lower()
    title = info['title'].lower()
    loai = info['loai_van_ban'].lower()
    skh = info['so_ky_hieu'].lower()
    
    # Check if internal policy evidence exists
    is_internal = ('agribank' in cq or 'agribank' in title or 'nội bộ' in title or 'nội bộ' in cq or 'hđtv' in cq or 'hđqt' in cq)
    
    if is_internal:
        cls = 'INTERNAL_POLICY'
        internal_count += 1
        evidence = f"Phát hành bởi đơn vị nội bộ / Agribank ({info['co_quan_ban_hanh']})"
    else:
        cls = 'EXTERNAL_REQUIREMENT'
        external_count += 1
        evidence = f"Văn bản quy phạm pháp luật do cơ quan nhà nước ban hành ({info['co_quan_ban_hanh']})"
        
    info['classification'] = cls
    info['evidence'] = evidence
    doc_list.append(info)
    
    print(f"\nDoc ID: {did}")
    print(f"  Title: {info['title']}")
    print(f"  Số ký hiệu: {info['so_ky_hieu']}")
    print(f"  Loại văn bản: {info['loai_van_ban']}")
    print(f"  Cơ quan ban hành: {info['co_quan_ban_hanh']}")
    print(f"  Classification: {cls}")
    print(f"  Evidence: {evidence}")
    print(f"  Chunks: {info['chunk_count']}")

print(f"\n--- SUMMARY CLASSIFICATION ---")
print(f"External Requirements (NHNN/CP/QH...): {external_count}")
print(f"Internal Policies (Agribank/Internal): {internal_count}")
print(f"Data Status: {'READY' if internal_count > 0 and external_count > 0 else 'INSUFFICIENT (INTERNAL POLICY NOT FOUND)'}")
