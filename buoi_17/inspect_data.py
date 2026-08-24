import pandas as pd
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

p1 = r'd:\03.08\buoi_17\data\agribank_internal_policies.csv'
p2 = r'd:\03.08\buoi_17\data\chunks_combined_secure.csv'

df1 = pd.read_csv(p1)
df2 = pd.read_csv(p2)

print("=== AGRIBANK INTERNAL POLICIES SUMMARY ===")
print("Total chunks:", len(df1))
unique_docs_1 = df1.groupby('document_id').first().reset_index()
print("Total unique internal documents:", len(unique_docs_1))
for idx, row in unique_docs_1.iterrows():
    print(f"{idx+1}. [{row['document_id']}] Title: {row['title']} | Số KH: {row['so_ky_hieu']} | Loại: {row['loai_van_ban']} | CQBH: {row['co_quan_ban_hanh']} | Ngày: {row['ngay_ban_hanh']}")

print("\n=== CHECK METADATA COMPLETENESS (14 COLUMNS) ===")
cols = ['chunk_id', 'document_id', 'text', 'source_file', 'title', 'so_ky_hieu', 'loai_van_ban', 'co_quan_ban_hanh', 'ngay_ban_hanh', 'chapter', 'section', 'article', 'citation', 'allowed_roles']
for col in cols:
    null1 = df1[col].isnull().sum()
    null2 = df2[col].isnull().sum()
    print(f"Col: {col:<18} | Internal Policy Nulls: {null1}/{len(df1)} | Combined CSV Nulls: {null2}/{len(df2)}")

print("\n=== ALL DOCUMENTS IN COMBINED SECURE CSV ===")
unique_docs_2 = df2.groupby('document_id').first().reset_index()
print("Total unique documents in combined secure csv:", len(unique_docs_2))
for idx, row in unique_docs_2.iterrows():
    print(f"{idx+1}. [{row['document_id']}] Title: {row['title']} | Số KH: {row['so_ky_hieu']} | CQBH: {row['co_quan_ban_hanh']}")
