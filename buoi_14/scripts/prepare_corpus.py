import os
import sys
import re
import pandas as pd
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    """Standardize UTF-8 text, whitespace, and newline formatting without removing terms/numbers."""
    if not text:
        return ""
    # Standardize whitespace on each line
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in text.splitlines()]
    # Remove empty lines while maintaining structure
    cleaned = '\n'.join([l for l in lines if l])
    return cleaned

def parse_html_content(doc_id: str, html: str, meta_info: dict) -> list:
    """Parse HTML content into structured legal chunks (Chapters, Sections, Articles, Clauses)."""
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text(separator='\n')
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    current_chapter = ""
    current_section = ""
    current_article = ""
    current_lines = []
    doc_chunks = []
    chunk_index = 0

    def add_chunk(art: str, chap: str, sec: str, clause_num: str, raw_lines_buf: list):
        nonlocal chunk_index
        full_text = clean_text('\n'.join(raw_lines_buf))
        if not full_text:
            return

        # If chunk is large (> 3500 chars), split by Clauses ('1.', '2.', etc.) for optimal retrieval context
        if len(full_text) > 3500 and not clause_num:
            clause_splits = []
            c_header = []
            c_curr_num = ""
            c_curr_lines = []

            for line in raw_lines_buf:
                m = re.match(r'^(\d+)\.\s+', line)
                if m and int(m.group(1)) <= 50:
                    if c_curr_lines:
                        clause_splits.append((c_curr_num, c_curr_lines))
                        c_curr_lines = []
                    else:
                        c_header = c_curr_lines
                    c_curr_num = m.group(1)
                    c_curr_lines.append(line)
                else:
                    c_curr_lines.append(line)
            if c_curr_lines:
                clause_splits.append((c_curr_num, c_curr_lines))

            if len(clause_splits) > 1:
                header_str = '\n'.join(c_header).strip()
                for c_num, c_lines in clause_splits:
                    sub_text = clean_text(header_str + '\n' + '\n'.join(c_lines)) if header_str else clean_text('\n'.join(c_lines))
                    c_id = f"{doc_id}_chunk_{chunk_index:03d}"
                    doc_chunks.append({
                        'chunk_id': c_id,
                        'document_id': doc_id,
                        'text': sub_text,
                        'source_file': 'content.csv',
                        'title': meta_info.get('title', ''),
                        'document_type': meta_info.get('loai_van_ban', ''),
                        'chapter': chap,
                        'section': sec,
                        'article': art,
                        'clause': f"Khoản {c_num}" if c_num else "",
                        'effective_date': meta_info.get('ngay_co_hieu_luc', ''),
                        'status': meta_info.get('tinh_trang_hieu_luc', ''),
                        'so_ky_hieu': meta_info.get('so_ky_hieu', ''),
                        'co_quan_ban_hanh': meta_info.get('co_quan_ban_hanh', ''),
                        'ngay_ban_hanh': meta_info.get('ngay_ban_hanh', ''),
                        'linh_vuc': meta_info.get('linh_vuc', ''),
                        'nganh': meta_info.get('nganh', ''),
                        'nguoi_ky': meta_info.get('nguoi_ky', ''),
                        'chuc_danh': meta_info.get('chuc_danh', '')
                    })
                    chunk_index += 1
                return

        c_id = f"{doc_id}_chunk_{chunk_index:03d}"
        doc_chunks.append({
            'chunk_id': c_id,
            'document_id': doc_id,
            'text': full_text,
            'source_file': 'content.csv',
            'title': meta_info.get('title', ''),
            'document_type': meta_info.get('loai_van_ban', ''),
            'chapter': chap,
            'section': sec,
            'article': art,
            'clause': clause_num,
            'effective_date': meta_info.get('ngay_co_hieu_luc', ''),
            'status': meta_info.get('tinh_trang_hieu_luc', ''),
            'so_ky_hieu': meta_info.get('so_ky_hieu', ''),
            'co_quan_ban_hanh': meta_info.get('co_quan_ban_hanh', ''),
            'ngay_ban_hanh': meta_info.get('ngay_ban_hanh', ''),
            'linh_vuc': meta_info.get('linh_vuc', ''),
            'nganh': meta_info.get('nganh', ''),
            'nguoi_ky': meta_info.get('nguoi_ky', ''),
            'chuc_danh': meta_info.get('chuc_danh', '')
        })
        chunk_index += 1

    for line in lines:
        if re.match(r'^Chương\s+[I|V|X|L|C|D|M\d]+', line, re.IGNORECASE):
            if current_lines:
                add_chunk(current_article, current_chapter, current_section, '', current_lines)
                current_lines = []
            current_chapter = line
            current_article = ""
            current_lines.append(line)
        elif re.match(r'^Mục\s+\d+', line, re.IGNORECASE):
            if current_lines:
                add_chunk(current_article, current_chapter, current_section, '', current_lines)
                current_lines = []
            current_section = line
            current_article = ""
            current_lines.append(line)
        elif re.match(r'^Điều\s+\d+', line, re.IGNORECASE):
            if current_lines:
                add_chunk(current_article, current_chapter, current_section, '', current_lines)
                current_lines = []
            current_article = line.split('.')[0] if '.' in line else line.split(':')[0]
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        add_chunk(current_article, current_chapter, current_section, '', current_lines)

    return doc_chunks

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Resolve absolute paths relative to current script/project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(base_dir, "..", "kb+hops")
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    output_csv = os.path.join(output_dir, "chunks_normalized.csv")
    
    content_path = os.path.join(source_dir, "content.csv")
    metadata_path = os.path.join(source_dir, "metadata.csv")
    
    print(f" Reading source data from: {os.path.abspath(source_dir)}")
    if not os.path.exists(content_path) or not os.path.exists(metadata_path):
        print(f" Error: Source files not found in {source_dir}")
        sys.exit(1)
        
    content_df = pd.read_csv(content_path, dtype=str)
    metadata_df = pd.read_csv(metadata_path, dtype=str)
    
    # Map metadata by ID
    meta_dict = metadata_df.set_index('id').to_dict(orient='index')
    
    all_chunks = []
    for _, row in content_df.iterrows():
        doc_id = str(row['id']).strip()
        html_content = str(row.get('content_html', ''))
        doc_meta = meta_dict.get(doc_id, {})
        chunks = parse_html_content(doc_id, html_content, doc_meta)
        all_chunks.extend(chunks)
        
    df_out = pd.DataFrame(all_chunks)
    
    # Validation checks
    total_chunks = len(df_out)
    total_docs = df_out['document_id'].nunique()
    missing_text_count = df_out['text'].isna().sum() + (df_out['text'].str.strip() == '').sum()
    duplicate_chunk_ids = df_out['chunk_id'].duplicated().sum()
    duplicate_rows = df_out.duplicated().sum()
    
    # Save output CSV
    df_out.to_csv(output_csv, index=False, encoding='utf-8')
    print(f" Saved normalized corpus to: {os.path.abspath(output_csv)}")
    
    print("\n" + "=" * 60)
    print(" CORPUS NORMALIZATION REPORT")
    print("=" * 60)
    print(f"Tổng số chunk (Total chunks)     : {total_chunks}")
    print(f"Số document (Total documents)   : {total_docs}")
    print(f"Số chunk thiếu text (Missing)   : {missing_text_count}")
    print(f"Trùng lặp chunk_id (Duplicates) : {duplicate_chunk_ids}")
    print(f"Trùng lặp dòng (Row Duplicates) : {duplicate_rows}")
    print("=" * 60)
    
    print("\n 3 SAMPLE RECORDS:")
    sample_records = df_out.head(3).to_dict(orient='records')
    for idx, rec in enumerate(sample_records, 1):
        print(f"\n--- SAMPLE RECORD #{idx} ---")
        print(f"Chunk ID        : {rec['chunk_id']}")
        print(f"Document ID     : {rec['document_id']}")
        print(f"Title           : {rec['title']}")
        print(f"Document Type   : {rec['document_type']}")
        print(f"Số Ký Hiệu      : {rec['so_ky_hieu']}")
        print(f"Chapter         : {rec['chapter']}")
        print(f"Section         : {rec['section']}")
        print(f"Article         : {rec['article']}")
        print(f"Clause          : {rec['clause']}")
        print(f"Effective Date  : {rec['effective_date']}")
        print(f"Status          : {rec['status']}")
        print(f"Text Snippet    : {rec['text'][:250]}...")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
