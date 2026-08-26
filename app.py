import os
import sys
import json
import pandas as pd
import streamlit as st

# Setup python path
current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = current_dir
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from scripts.compliance_checker import AIComplianceChecker
from scripts.audit_checklist_gen import AIAuditChecklistGen
from scripts.internal_lookup import InternalLookupService
from scripts.audit_logger import AUDIT_LOG_FILE

# Page Config
st.set_page_config(
    page_title="AI Compliance & Audit Checklist — Buổi 18",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Modern Premium Dark UI
st.markdown("""
<style>
    /* Main App Background & Default Text */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    h1, h2, h3, h4, h5, h6, p, span, li, label {
        color: #f8fafc !important;
    }
    
    .stMarkdown, .stMarkdown p {
        color: #e2e8f0 !important;
        font-size: 1.02rem;
        line-height: 1.6;
    }

    .stWidgetLabel, label[data-testid="stWidgetLabel"] {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    textarea, input, div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        padding: 12px 24px !important;
        margin-right: 6px !important;
    }
    
    button[data-baseweb="tab"] div p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1e293b !important;
        border-bottom: 3px solid #38bdf8 !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] div p {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155 !important;
    }

    /* Primary Action Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Advisory Banner */
    .advisory-banner {
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
        color: #ffffff !important;
        padding: 14px 24px;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.4);
    }

    /* Cards */
    .conflict-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }

    .badge-high {
        background-color: #dc2626;
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-medium {
        background-color: #d97706;
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-low {
        background-color: #059669;
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-review {
        background-color: #475569;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Engines
@st.cache_resource
def load_engines():
    checker = AIComplianceChecker()
    checklist_gen = AIAuditChecklistGen()
    lookup_svc = InternalLookupService()
    return checker, checklist_gen, lookup_svc

compliance_checker, audit_gen, lookup_service = load_engines()

# --- MANDATORY TOP BANNER ---
st.markdown(
    '<div class="advisory-banner">⚠️ Demo sản phẩm AI Kiểm toán - Kết quả gợi ý cần kiểm toán viên xác minh trước khi ban hành.</div>',
    unsafe_allow_html=True
)

st.title("🛡️ AI COMPLIANCE CHECKER & AUDIT CHECKLIST GENERATOR")
st.caption("Hệ thống So sánh Chéo Tuân thủ Quy định & Tự động Sinh Checklist Kiểm toán Agribank (Buổi 18)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 PHÂN QUYỀN VÀ NGƯỜI DÙNG")
    user_id = st.text_input("Mã Chuyên viên / Auditor ID", value="auditor_b18_01")
    
    user_role = st.selectbox(
        "Vai trò Người dùng (User Role)",
        options=["Admin", "Risk_Manager", "KiemToanVien", "Staff"],
        index=2,
        help="Giới hạn phạm vi xem tài liệu và thao tác kiểm toán theo RBAC."
    )

    st.divider()

    st.header("🌐 KẾT NỐI DỮ LIỆU CƠ SỞ")
    st.success("🟢 Internal Policies: Ready (10 văn bản / 24 chunks)")
    st.success("🟢 External Legal Docs: Ready (15 văn bản / 787 chunks)")
    st.info("📊 Combined Secure Corpus: 811 chunks")

    st.divider()

    if st.button("🔄 Reset Session & Clean Log", use_container_width=True):
        st.session_state.clear()
        st.success("Đã reset session làm việc!")
        st.rerun()

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs([
    "⚖️ UC3: AI COMPLIANCE CHECKER",
    "📋 UC4: AI AUDIT CHECKLIST GENERATOR",
    "📜 AUDIT LOG & SYSTEM TRAIL"
])

# ==============================================================================
# TAB 1: UC3 - AI COMPLIANCE CHECKER
# ==============================================================================
with tab1:
    st.subheader("UC3 — AI Compliance Checker (Kiểm tra xung đột quy định nội bộ vs pháp luật)")
    st.markdown("Hệ thống tự động so sánh chéo (Cross-Comparison) giữa quy định Agribank và văn bản NHNN để phát hiện mâu thuẫn/xung đột.")

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_domain = st.selectbox(
            "Chọn Bộ lọc Miền Nghiệp Vụ (Domain Filter):",
            options=[
                "Tất cả các Miền Nghiệp Vụ",
                "An toàn kho quỹ & Vận chuyển tiền mặt",
                "CAR & Quản lý rủi ro",
                "Tín dụng & Phân cấp phê duyệt",
                "Bảo mật CNTT & AI"
            ]
        )
    with col2:
        st.write("")
        st.write("")
        btn_scan = st.button("🔍 PHÁT HIỆN XUNG ĐỘT", type="primary", use_container_width=True)

    if "conflicts_data" not in st.session_state:
        # Load initial cached results if exist
        conflicts_file = os.path.join(buoi17_dir, "outputs", "compliance_conflicts.csv")
        if os.path.exists(conflicts_file):
            st.session_state.conflicts_data = pd.read_csv(conflicts_file).to_dict(orient="records")
        else:
            st.session_state.conflicts_data = []

    if btn_scan:
        with st.spinner("Đang chạy AI Cross-Comparison Engine trên các cặp quy định..."):
            results = compliance_checker.run_compliance_check_suite()
            compliance_checker.export_results(results)
            st.session_state.conflicts_data = results
            st.success(f"Đã hoàn thành quét! Phát hiện {len(results)} điểm mâu thuẫn/chồng chéo quy định.")

    conflicts = st.session_state.conflicts_data

    # Filter by domain if specified
    if selected_domain != "Tất cả các Miền Nghiệp Vụ":
        conflicts = [c for c in conflicts if selected_domain.lower() in str(c.get("domain")).lower()]

    if conflicts:
        st.markdown(f"### 📊 Danh sách {len(conflicts)} Xung đột Tuân thủ Phát hiện:")
        
        for idx, item in enumerate(conflicts):
            sev = item.get("severity", "MEDIUM")
            badge_class = "badge-high" if sev == "HIGH" else ("badge-medium" if sev == "MEDIUM" else "badge-low")
            
            with st.container():
                st.markdown(f"""
                <div class="conflict-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 1.15rem; font-weight: 700; color: #38bdf8;">[{idx+1}] Mã Xung Đột: {item.get('conflict_id')}</span>
                        <div>
                            <span class="{badge_class}">Severity: {sev}</span>
                            <span class="badge-review" style="margin-left: 8px;">{item.get('review_status')}</span>
                        </div>
                    </div>
                    <div style="font-size: 0.95rem; color: #cbd5e1; margin-bottom: 12px;">
                        <b>Miền nghiệp vụ:</b> {item.get('domain')} | <b>Loại mâu thuẫn:</b> <code>{item.get('conflict_type')}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    st.markdown(f"**📄 Văn bản A (Quy định Nội bộ):** `{item.get('doc_a_id')}`")
                    st.caption(f"Trích dẫn: {item.get('doc_a_citation')}")
                    st.info(item.get('doc_a_text'))

                with c_col2:
                    st.markdown(f"**📜 Văn bản B (Quy định Đối chiếu):** `{item.get('doc_b_id')}`")
                    st.caption(f"Trích dẫn: {item.get('doc_b_citation')}")
                    st.warning(item.get('doc_b_text'))

                st.markdown(f"**🔍 Phân tích chi tiết từ AI Compliance Engine:**")
                st.success(item.get('description'))

                col_act1, col_act2 = st.columns([2, 1])
                with col_act1:
                    if st.button(f"✅ Phê duyệt & Đã Xác minh (Human Verified #{idx+1})", key=f"btn_approve_{idx}"):
                        item["review_status"] = "HUMAN_VERIFIED"
                        st.success(f"Đã cập nhật trạng thái cho {item.get('conflict_id')}!")
                        st.rerun()

                st.divider()

        # Download Buttons
        col_dn1, col_dn2 = st.columns(2)
        with col_dn1:
            df_c = pd.DataFrame(conflicts)
            csv_bytes = df_c.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                "📥 Tải Kết quả CSV (compliance_conflicts.csv)",
                data=csv_bytes,
                file_name="compliance_conflicts.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_dn2:
            report_path = os.path.join(buoi17_dir, "outputs", "compliance_conflict_report.md")
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    md_text = f.read()
                st.download_button(
                    "📥 Tải Báo cáo Markdown (compliance_conflict_report.md)",
                    data=md_text.encode("utf-8"),
                    file_name="compliance_conflict_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

    else:
        st.info("Chưa có dữ liệu xung đột. Nhấn nút 'PHÁT HIỆN XUNG ĐỘT' ở trên để tiến hành quét.")

# ==============================================================================
# TAB 2: UC4 - AI AUDIT CHECKLIST GENERATOR
# ==============================================================================
with tab2:
    st.subheader("UC4 — AI Audit Checklist Generator (Tự động tạo danh mục kiểm toán)")
    st.markdown("Sinh danh mục checklist kiểm toán chuẩn hóa bám sát theo Miền Nghiệp Vụ & Đơn Vị được kiểm toán.")

    col_u1, col_u2, col_u3 = st.columns([2, 2, 1])
    with col_u1:
        audit_domain = st.selectbox(
            "Miền Nghiệp Vụ Kiểm Toán (Domain):",
            options=[
                "An toàn kho quỹ & Vận chuyển tiền",
                "Bảo mật CNTT & AI",
                "CAR & Quản lý rủi ro",
                "Phân quyền tín dụng"
            ]
        )
    with col_u2:
        audit_unit = st.selectbox(
            "Đơn Vị Được Kiểm Toán (Unit Scope):",
            options=[
                "Chi nhánh loại 1 Agribank",
                "Phòng giao dịch",
                "Khối Công nghệ Thông tin",
                "Phòng Kế toán & Nguồn vốn"
            ]
        )
    with col_u3:
        st.write("")
        st.write("")
        btn_gen = st.button("📋 TẠO CHECKLIST", type="primary", use_container_width=True)

    if "checklist_data" not in st.session_state:
        chk_file = os.path.join(buoi17_dir, "outputs", "audit_checklist_results.csv")
        if os.path.exists(chk_file):
            st.session_state.checklist_data = pd.read_csv(chk_file).to_dict(orient="records")
        else:
            st.session_state.checklist_data = []

    if btn_gen:
        with st.spinner(f"AI đang truy xuất quy định và lập Checklist cho {audit_unit}..."):
            items = audit_gen.generate_checklist_for_scope(
                domain=audit_domain,
                unit=audit_unit,
                user_role=user_role
            )
            st.session_state.checklist_data = items
            st.success(f"Đã khởi tạo thành công {len(items)} mục checklist kiểm toán cho {audit_unit}!")

    checklists = st.session_state.checklist_data

    if checklists:
        st.markdown(f"### 📋 Bản Nháp Checklist Kiểm Toán ({len(checklists)} mục):")
        
        df_chk = pd.DataFrame(checklists)
        
        # Display Table
        st.dataframe(
            df_chk[["item_id", "audit_question", "risk_level", "risk_description", "source_citation", "review_status"]],
            use_container_width=True
        )

        with st.expander("🔍 Xem chi tiết các mục Checklist & Trích dẫn gốc"):
            for idx, item in enumerate(checklists):
                st.markdown(f"#### [{idx+1}] Mã Mục: `{item['item_id']}` — {item['audit_question']}")
                st.markdown(f"- **Mức độ rủi ro:** `{item['risk_level']}`")
                st.markdown(f"- **Rủi ro tiềm ẩn:** {item['risk_description']}")
                st.markdown(f"- **Trích dẫn điều khoản gốc:** `{item['source_citation']}`")
                st.markdown(f"- **Khuyến nghị kiểm toán:** {item['recommendation']}")
                st.divider()

        # Download Checklist Buttons
        col_cd1, col_cd2 = st.columns(2)
        with col_cd1:
            csv_chk_bytes = df_chk.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                "📥 Tải Checklist CSV (audit_checklist_results.csv)",
                data=csv_chk_bytes,
                file_name="audit_checklist_results.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_cd2:
            json_chk_bytes = json.dumps(checklists, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button(
                "📥 Tải Checklist JSON (audit_checklist_results.json)",
                data=json_chk_bytes,
                file_name="audit_checklist_results.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.info("Chưa có danh mục checklist. Nhấn nút 'TẠO CHECKLIST' ở trên để sinh tự động.")

# ==============================================================================
# TAB 3: AUDIT LOG & SYSTEM TRAIL
# ==============================================================================
with tab3:
    st.subheader("Nhật Ký Truy Vết Hệ Thống (Audit Log Viewer)")
    st.markdown("Ghi nhận 100% nhật ký truy vấn, so sánh xung đột và sinh checklist kiểm toán không thể chỉnh sửa.")

    if os.path.exists(AUDIT_LOG_FILE):
        logs = []
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        logs.append(json.loads(line.strip()))
                    except:
                        pass

        if logs:
            df_logs = pd.DataFrame(logs)

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                role_filter = st.multiselect("Lọc theo Role:", options=df_logs["user_role"].unique().tolist(), default=df_logs["user_role"].unique().tolist())
            with col_f2:
                status_filter = st.multiselect("Lọc theo Trạng thái (Answer Status):", options=df_logs["answer_status"].unique().tolist(), default=df_logs["answer_status"].unique().tolist())

            df_filtered = df_logs[
                (df_logs["user_role"].isin(role_filter)) &
                (df_logs["answer_status"].isin(status_filter))
            ]

            st.markdown(f"**Hiển thị {len(df_filtered)} / {len(logs)} bản ghi nhật ký:**")
            st.dataframe(
                df_filtered[["timestamp", "request_id", "user_role", "question", "access_scope", "answer_status", "retrieved_count"]],
                use_container_width=True
            )

            with st.expander("📄 Xem Nhật ký Chi tiết dạng JSON"):
                st.json(df_filtered.to_dict(orient="records"))
        else:
            st.info("File audit_log.jsonl chưa có dữ liệu.")
    else:
        st.info("Chưa khởi tạo file audit_log.jsonl. Mọi thao tác kiểm tra sẽ tự động ghi log vào đây.")
