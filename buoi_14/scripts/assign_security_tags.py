import os
import sys
import json
import re
import pandas as pd

# Base paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
output_csv = os.path.join(base_dir, "data", "processed", "chunks_secure.csv")

def classify_chunk_roles(row: pd.Series) -> str:
    """
    Classifies a chunk into appropriate RBAC allowed_roles based on text keywords and metadata.
    Returns JSON string of role names list.
    """
    text_content = (str(row.get('text', '')) + " " + str(row.get('title', '')) + " " + str(row.get('section', ''))).lower()

    # 1. HR & Confidential Internal Management
    hr_keywords = [
        "nhân sự", "lương thưởng", "tuyển dụng", "bổ nhiệm", "kỷ luật", 
        "thù lao", "quy hoạch cán bộ", "đánh giá nhân viên", "nội bộ ngân hàng"
    ]
    if any(kw in text_content for kw in hr_keywords):
        roles = ["Admin", "HR", "Legal_Officer"]
        return json.dumps(roles, ensure_ascii=False)

    # 2. Risk, Credit & Financial Limit Management
    risk_keywords = [
        "tín dụng", "rủi ro", "hạn mức", "phê duyệt vay", "bảo đảm tiền vay",
        "thẩm định tài sản", "xử lý nợ", "vốn chủ sở hữu", "công cụ nợ"
    ]
    if any(kw in text_content for kw in risk_keywords):
        roles = ["Admin", "Risk_Manager", "Legal_Officer", "Bank_Staff", "Staff"]
        return json.dumps(roles, ensure_ascii=False)

    # 3. General Public Regulations & Open Circulars
    roles = ["Admin", "HR", "Risk_Manager", "Legal_Officer", "Bank_Staff", "Staff", "Guest"]
    return json.dumps(roles, ensure_ascii=False)

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(input_csv):
        print(f" Lỗi: Không tìm thấy file đầu vào tại {input_csv}")
        sys.exit(1)

    print(f" Đang đọc dữ liệu từ: {input_csv}")
    df = pd.read_csv(input_csv, dtype=str)
    print(f" Tổng số chunks đọc được: {len(df)}")

    # Gán cột allowed_roles
    print(" Đang phân loại security tags (allowed_roles)...")
    df['allowed_roles'] = df.apply(classify_chunk_roles, axis=1)

    # Kiểm tra tính toàn vẹn (không bị null/empty)
    null_roles_count = df['allowed_roles'].isna().sum() + (df['allowed_roles'] == "").sum()
    if null_roles_count > 0:
        print(f" CẢNH BÁO: Có {null_roles_count} dòng bị trống allowed_roles!")
    else:
        print(" VERIFICATION PASSED: 100% dòng dữ liệu đều có ít nhất 1 role phân quyền.")

    # Lưu kết quả
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f" Đã lưu dữ liệu bảo mật ra: {output_csv}\n")

    # Thống kê phân bổ nhóm bảo mật
    print("=" * 75)
    print(" THỐNG KÊ PHÂN BỔ BẢO MẬT (SECURITY TAGS DISTRIBUTION)")
    print("=" * 75)
    group_counts = {}
    for r_json in df['allowed_roles']:
        roles_tuple = tuple(sorted(json.loads(r_json)))
        label = " -> ".join(roles_tuple)
        group_counts[label] = group_counts.get(label, 0) + 1

    for group, count in sorted(group_counts.items(), key=lambda x: x[1], reverse=True):
        print(f" [{count:>4} chunks] Roles: {group}")
    print("=" * 75 + "\n")

    # Hiển thị 3 mẫu dòng đại diện cho 3 cấp độ
    print("=" * 75)
    print(" SAMPLE CHUNKS THEO 3 CẤP ĐỘ BẢO MẬT ĐẠI DIỆN")
    print("=" * 75)

    samples = []
    for r_json in set(df['allowed_roles']):
        sample_row = df[df['allowed_roles'] == r_json].iloc[0]
        samples.append(sample_row)

    for idx, s in enumerate(samples, 1):
        roles_list = json.loads(s['allowed_roles'])
        cit_snip = s.get('citation', str(s.get('title', '')))[:60]
        text_snip = s['text'][:120].replace('\n', ' ')
        print(f"Sample #{idx}:")
        print(f"  Chunk ID      : {s['chunk_id']}")
        print(f"  Allowed Roles : {roles_list}")
        print(f"  Citation      : {cit_snip}...")
        print(f"  Text Snippet  : {text_snip}...")
        print("-" * 75)

if __name__ == "__main__":
    main()
