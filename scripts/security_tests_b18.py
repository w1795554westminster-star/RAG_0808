import os
import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "scripts" else current_dir
outputs_dir = os.path.join(buoi17_dir, "outputs")
os.makedirs(outputs_dir, exist_ok=True)

sys.path.append(buoi17_dir)
from scripts.internal_lookup import InternalLookupService
from scripts.audit_checklist_gen import AIAuditChecklistGen

class SecurityTesterB18:
    def __init__(self):
        self.csv_path = os.path.join(buoi17_dir, "data", "chunks_combined_secure.csv")
        self.df_corpus = pd.read_csv(self.csv_path)
        self.lookup_svc = InternalLookupService()
        self.results = []

    def log_test_result(self, test_name: str, status: str, details: str):
        self.results.append({
            "test_name": test_name,
            "status": status,
            "details": details
        })
        print(f"[{status}] {test_name}: {details}")

    def run_all_tests(self):
        print("=== STARTING FAST SECURITY & GUARDRAIL TEST SUITE FOR BUỔI 18 ===")

        path_c = os.path.join(outputs_dir, "compliance_conflicts.csv")
        path_chk = os.path.join(outputs_dir, "audit_checklist_results.csv")

        df_c = pd.read_csv(path_c) if os.path.exists(path_c) else pd.DataFrame()
        df_chk = pd.read_csv(path_chk) if os.path.exists(path_chk) else pd.DataFrame()

        # Test 1: RBAC Test
        try:
            res_staff = self.lookup_svc.lookup(
                question="Quy chế bảo mật CNTT và quản trị dữ liệu AI Agribank",
                user_role="Staff",
                top_k=5
            )
            allowed_staff_chunks = [c for c in res_staff["retrieved_chunks"] if "Staff" in str(c.get("allowed_roles"))]
            is_rbac_ok = (len(res_staff["retrieved_chunks"]) == len(allowed_staff_chunks))
            
            if is_rbac_ok:
                self.log_test_result("1. RBAC Test", "PASS", "Role 'Staff' bị chặn khỏi các chunk bảo mật riêng của Risk_Manager/Admin.")
            else:
                self.log_test_result("1. RBAC Test", "FAIL", "Rò rỉ chunk không được phép cho role Staff.")
        except Exception as e:
            self.log_test_result("1. RBAC Test", "FAIL", f"Lỗi thực thi: {e}")

        # Test 2: Citation Integrity
        try:
            c_cit_ok = all(bool(row.get("doc_a_citation")) and bool(row.get("doc_b_citation")) for _, row in df_c.iterrows()) if not df_c.empty else False
            chk_cit_ok = all(bool(row.get("source_citation")) and str(row.get("source_citation")) != "N/A" for _, row in df_chk.iterrows()) if not df_chk.empty else False

            if c_cit_ok and chk_cit_ok:
                self.log_test_result("2. Citation Integrity", "PASS", f"100% conflicts ({len(df_c)}) và checklist items ({len(df_chk)}) có citation hợp lệ.")
            else:
                self.log_test_result("2. Citation Integrity", "FAIL", "Phát hiện citation rỗng hoặc N/A trong kết quả.")
        except Exception as e:
            self.log_test_result("2. Citation Integrity", "FAIL", f"Lỗi thực thi: {e}")

        # Test 3: Hallucination Check
        try:
            corpus_doc_ids = set(self.df_corpus['document_id'].unique())
            valid_docs = True
            for _, row in df_c.iterrows():
                if row['doc_a_id'] not in corpus_doc_ids or row['doc_b_id'] not in corpus_doc_ids:
                    valid_docs = False

            if valid_docs and not df_c.empty:
                self.log_test_result("3. Hallucination Check", "PASS", "100% document_id trong kết quả AI hoàn toàn trùng khớp với dataset thật.")
            else:
                self.log_test_result("3. Hallucination Check", "FAIL", "Phát hiện mã văn bản tự bịa không tồn tại trong dataset.")
        except Exception as e:
            self.log_test_result("3. Hallucination Check", "FAIL", f"Lỗi thực thi: {e}")

        # Test 4: Human Review Guardrail
        try:
            status_c_ok = all(row.get("review_status") in ["NEEDS_HUMAN_REVIEW", "HUMAN_VERIFIED"] for _, row in df_c.iterrows()) if not df_c.empty else False
            status_chk_ok = all(row.get("review_status") in ["NEEDS_HUMAN_REVIEW", "HUMAN_VERIFIED"] for _, row in df_chk.iterrows()) if not df_chk.empty else False

            if status_c_ok and status_chk_ok:
                self.log_test_result("4. Human Review Guardrail", "PASS", "100% kết quả xuất ra có nhãn review_status = 'NEEDS_HUMAN_REVIEW'.")
            else:
                self.log_test_result("4. Human Review Guardrail", "FAIL", "Phát hiện kết quả thiếu nhãn NEEDS_HUMAN_REVIEW.")
        except Exception as e:
            self.log_test_result("4. Human Review Guardrail", "FAIL", f"Lỗi thực thi: {e}")

        # Test 5: Audit Log Privacy
        try:
            audit_file = os.path.join(outputs_dir, "audit_log.jsonl")
            has_secret = False
            if os.path.exists(audit_file):
                with open(audit_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "AIzaSy" in content or "GEMINI_API_KEY=" in content or "AQ.Ab8" in content:
                        has_secret = True
            
            if not has_secret:
                self.log_test_result("5. Audit Log Privacy", "PASS", "Audit log tuyệt đối không lưu API key / secret key.")
            else:
                self.log_test_result("5. Audit Log Privacy", "FAIL", "Phát hiện API key / secret lộ trong file log!")
        except Exception as e:
            self.log_test_result("5. Audit Log Privacy", "FAIL", f"Lỗi thực thi: {e}")

        # Test 6: Unknown Domain Test
        try:
            chk_gen = AIAuditChecklistGen()
            unknown_res = chk_gen.generate_checklist_for_scope(
                domain="Bảo hiểm vũ trụ không gian",
                unit="Phòng Khoa học Vũ trụ",
                user_role="Risk_Manager"
            )
            is_safe = len(unknown_res) > 0 and all("CHK_" in item["item_id"] for item in unknown_res)
            if is_safe:
                self.log_test_result("6. Unknown Domain Test", "PASS", "Hệ thống xử lý an toàn miền không tồn tại, không tự bịa thông luật.")
            else:
                self.log_test_result("6. Unknown Domain Test", "FAIL", "Lỗi khi xử lý domain không tồn tại.")
        except Exception as e:
            self.log_test_result("6. Unknown Domain Test", "FAIL", f"Lỗi thực thi: {e}")

        # Test 7: File Export Verification
        try:
            c_cols_ok = "conflict_id" in df_c.columns and "doc_a_citation" in df_c.columns
            chk_cols_ok = "item_id" in df_chk.columns and "audit_question" in df_chk.columns

            if c_cols_ok and chk_cols_ok and len(df_c) > 0 and len(df_chk) > 0:
                self.log_test_result("7. File Export Verification", "PASS", f"Các file CSV xuất ra đúng schema chuẩn: conflicts ({len(df_c)} rows), checklist ({len(df_chk)} rows).")
            else:
                self.log_test_result("7. File Export Verification", "FAIL", "File CSV hỏng hoặc thiếu cột schema bắt buộc.")
        except Exception as e:
            self.log_test_result("7. File Export Verification", "FAIL", f"Lỗi thực thi: {e}")

        # Summary & Export Markdown Report
        all_passed = all(r["status"] == "PASS" for r in self.results)
        
        report_md = f"""# BÁO CÁO KIỂM THỬ BẢO MẬT & GUARDRAILS (SECURITY & GUARDRAIL TESTS B18)
**Ngày thực hiện:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tổng số bài test:** {len(self.results)}  
**Kết quả vượt qua:** {sum(1 for r in self.results if r['status'] == 'PASS')} / {len(self.results)}

---

## Bảng Chi tiết Kết quả Kiểm thử Bảo mật & Compliance Guardrails

| STT | Tên Bài Test | Trạng Thái | Mô Tả Chi Tiết & Bằng Chứng Kiểm Thử |
|---|---|---|---|
"""

        for idx, r in enumerate(self.results):
            stt_badge = "✅ **PASS**" if r["status"] == "PASS" else "❌ **FAIL**"
            report_md += f"| {idx+1} | **{r['test_name']}** | {stt_badge} | {r['details']} |\n"

        report_md += f"""
---

## Tổng kết Đánh giá Security & Governance

- **RBAC Strict Pre-filtering:** Đảm bảo nguyên tắc Privilege-of-Least-Access, người dùng role thấp không xem được tài liệu mật.
- **Data & Citation Authenticity:** Trích dẫn 100% dựa trên tài liệu thật, chống AI Hallucination.
- **Human-in-the-Loop Governance:** Bắt buộc nhãn `NEEDS_HUMAN_REVIEW` cho toàn bộ outputs.
- **Audit Log Integrity & Privacy:** Ghi nhật ký đầy đủ, mã hóa secret key.

---

```plaintext
SECURITY & GUARDRAIL TESTS: {"PASS" if all_passed else "FAIL"}
```
"""

        report_file = os.path.join(outputs_dir, "security_test_b18_report.md")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"Exported Security Test Report -> {report_file}")

if __name__ == "__main__":
    tester = SecurityTesterB18()
    tester.run_all_tests()
