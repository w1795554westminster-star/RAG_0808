import os
import sys
import json
import pandas as pd

# Add src to sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import config

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

def load_secure_kg_neo4j():
    sys.stdout.reconfigure(encoding='utf-8')

    secure_csv = os.path.join(base_dir, "data", "processed", "chunks_secure.csv")
    if not os.path.exists(secure_csv):
        print(f" Lỗi: Không tìm thấy file dữ liệu bảo mật tại {secure_csv}")
        sys.exit(1)

    df_secure = pd.read_csv(secure_csv, dtype=str)
    print(f" Đã đọc {len(df_secure)} dòng từ {secure_csv}")

    # Check Neo4j connection
    if not GraphDatabase:
        print(" [NEO4J NOTICE]: Thư viện python 'neo4j' chưa được cài đặt. Bỏ qua bước nạp graph trực tiếp.")
        return

    uri = config.NEO4J_URI
    user = config.NEO4J_USER
    password = config.NEO4J_PASSWORD
    db_name = config.NEO4J_DATABASE

    print(f" Đang kết nối tới Neo4j tại: {uri} (database: {db_name})...")

    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print(" Kết nối Neo4j THÀNH CÔNG!")
    except Exception as e:
        print(f" [NEO4J NOTICE]: Không thể kết nối tới Neo4j ({e}).")
        print(" Dữ liệu phân quyền bảo mật đã được ghi nhận an toàn tại CSV local `chunks_secure.csv` (lab_session='buoi_15').")
        return

    # Update Neo4j graph nodes using MERGE
    print(" Đang cập nhật thuộc tính allowed_roles và lab_session='buoi_15' vào Neo4j...")
    
    records = []
    for _, row in df_secure.iterrows():
        try:
            roles_list = json.loads(row['allowed_roles'])
        except Exception:
            roles_list = ["Guest"]

        records.append({
            'chunk_id': str(row['chunk_id']),
            'document_id': str(row['document_id']),
            'title': str(row.get('title', '')),
            'so_ky_hieu': str(row.get('so_ky_hieu', '')),
            'article': str(row.get('article', '')),
            'text': str(row.get('text', ''))[:500],
            'citation': str(row.get('citation', '')),
            'allowed_roles': roles_list
        })

    cypher_update = """
    UNWIND $batch AS row
    MERGE (v:VanBan {document_id: row.document_id})
    ON CREATE SET 
        v.title = row.title,
        v.so_ky_hieu = row.so_ky_hieu,
        v.created_at = timestamp()
    SET 
        v.allowed_roles = row.allowed_roles,
        v.lab_session = 'buoi_15'

    MERGE (d:DieuKhoan {chunk_id: row.chunk_id})
    ON CREATE SET 
        d.article = row.article,
        d.text = row.text,
        d.citation = row.citation
    SET 
        d.document_id = row.document_id,
        d.allowed_roles = row.allowed_roles,
        d.lab_session = 'buoi_15'

    MERGE (v)-[:CO_DIEU_KHOAN]->(d)
    """

    batch_size = 500
    with driver.session(database=db_name) as session:
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            session.run(cypher_update, batch=batch)
            print(f"  Đã nạp/cập nhật batch {i} -> {i + len(batch)} nodes...")

    print(" Nạp dữ liệu phân quyền Neo4j THÀNH CÔNG!\n")

    # Run verification Cypher queries
    print("=" * 75)
    print(" BÁO CÁO KIỂM TRÁ DIỄN BIẾN TRÊN NEO4J (VERIFICATION QUERIES)")
    print("=" * 75)
    
    with driver.session(database=db_name) as session:
        # Query 1: Count nodes with allowed_roles
        q1 = """
        MATCH (n) 
        WHERE n.allowed_roles IS NOT NULL AND n.lab_session = 'buoi_15'
        RETURN count(n) AS node_count, labels(n)[0] AS label
        """
        result1 = session.run(q1)
        print("1. Số lượng Node đã cập nhật thuộc tính allowed_roles:")
        for r in result1:
            print(f"   - Label [{r['label']}]: {r['node_count']} nodes")

        # Query 2: Sample VanBan and linked DieuKhoan
        q2 = """
        MATCH (v:VanBan)-[:CO_DIEU_KHOAN]->(d:DieuKhoan)
        WHERE v.lab_session = 'buoi_15'
        RETURN v.document_id AS doc_id, v.so_ky_hieu AS doc_code, v.allowed_roles AS v_roles, 
               d.chunk_id AS chunk_id, d.allowed_roles AS d_roles
        LIMIT 3
        """
        result2 = session.run(q2)
        print("\n2. Mẫu kiểm tra liên kết 1-hop VanBan -> DieuKhoan:")
        for r in result2:
            print(f"   - VanBan [{r['doc_code']} | ID: {r['doc_id']}] Allowed Roles: {r['v_roles']}")
            print(f"     └─ DieuKhoan [{r['chunk_id']}] Allowed Roles: {r['d_roles']}")

    driver.close()
    print("=" * 75 + "\n")

if __name__ == "__main__":
    load_secure_kg_neo4j()
