import os
import sys
import json
import socket
import pandas as pd
import streamlit as st

# Setup python path to import buoi_17 scripts
current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = current_dir
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from scripts.internal_lookup import InternalLookupService
from scripts.compliance_gap import ComplianceGapChecker
from scripts.secure_retrieval_adapter import SecureRetrievalAdapter

# Page Config
st.set_page_config(
    page_title="Secure RAG & AI Compliance — Buổi 17",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Premium High-Contrast Dark Mode UI
st.markdown("""
<style>
    /* Main App Background & Default Text */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* All Headings, Paragraphs, Markdown & Labels */
    h1, h2, h3, h4, h5, h6, p, span, li, label {
        color: #f8fafc !important;
    }
    
    .stMarkdown, .stMarkdown p {
        color: #e2e8f0 !important;
        font-size: 1.02rem;
        line-height: 1.6;
    }

    /* Input Widget Labels (Textarea, Selectbox, Slider) */
    .stWidgetLabel, label[data-testid="stWidgetLabel"] {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Input Fields (Text Area, Text Input, Selectbox) */
    textarea, input, div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    
    textarea:focus, input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3) !important;
    }

    /* Tabs Styling - High Contrast & High Visibility */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 10px 20px !important;
        margin-right: 4px !important;
    }
    
    button[data-baseweb="tab"] div p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
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
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] span {
        color: #cbd5e1 !important;
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
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Top Mandatory Banner */
    .mandatory-banner {
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
        color: #ffffff !important;
        padding: 14px 24px;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.4);
        letter-spacing: 0.3px;
    }

    /* Status Badges */
    .badge-granted {
        background-color: #059669;
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-denied {
        background-color: #dc2626;
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-review {
        background-color: #d97706;
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-insufficient {
        background-color: #475569;
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }
    
    /* Answer Output Card Container */
    .css-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Citation Box */
    .citation-box {
        background-color: #0f172a;
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        margin-top: 10px;
        border-radius: 6px;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 0.95rem;
        color: #7dd3fc !important;
        line-height: 1.5;
    }

    /* Caption Override */
    .stCaption, caption, small {
        color: #cbd5e1 !important;
        font-size: 0.95rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Check Neo4j Connectivity
def check_neo4j_active() -> bool:
    try:
        s = socket.socket()
        s.settimeout(1)
        res = s.connect_ex(('127.0.0.1', 7687))
        s.close()
        return res == 0
    except Exception:
        return False

# Initialize Services
@st.cache_resource
def get_services():
    lookup_service = InternalLookupService()
    gap_checker = ComplianceGapChecker()
    adapter = SecureRetrievalAdapter()
    return lookup_service, gap_checker, adapter

lookup_svc, gap_chk, secure_adapter = get_services()

# --- MANDATORY TOP BANNER ---
st.markdown(
    '<div class="mandatory-banner">⚠️ Demo đào tạo — kết quả AI cần kiểm toán viên xác minh.</div>',
    unsafe_allow_html=True
)

st.title("🛡️ SECURE RAG & COMPLIANCE GOVERNANCE — BUỔI 17")
st.caption("Hệ thống Tra cứu Quy định Nội bộ Phân quyền (RBAC) & Audit Trail & AI Compliance Gap Checker")

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 DEMO USER & ROLE")
    user_id = st.text_input("User ID Demo", value="demo_auditor_01")
    
    user_role = st.selectbox(
        "User Role (Phân quyền truy cập)",
        options=["Admin", "Risk_Manager", "Staff", "HR", "Guest"],
        index=1,
        help="Lọc RBAC pre-filter loại bỏ các tài liệu không được phép trước retrieval."
    )
    
    st.divider()
    
    st.header("🌐 KNOWLEDGE GRAPH & DATA")
    neo4j_active = check_neo4j_active()
    if neo4j_active:
        st.success("🟢 Neo4j Database: ACTIVE (bolt://127.0.0.1:7687)")
    else:
        st.info("🟡 Neo4j Database: INACTIVE (Dùng Fallback local relationships.csv)")

    st.divider()
    st.markdown("### 📊 Target Corpus")
    st.markdown("- **Corpus**: `chunks_secure.csv`")
    st.markdown("- **Total Chunks**: `2,823` chunks")
    st.markdown("- **Unique Docs**: `30` documents")

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs([
    "🔍 TAB 1: TRA CỨU QUY ĐỊNH",
    "⚖️ TAB 2: COMPLIANCE GAP CHECKER",
    "📜 TAB 3: AUDIT TRAIL"
])

# ==============================================================================
# TAB 1: TRA CỨU QUY ĐỊNH (USE CASE 1)
# ==============================================================================
with tab1:
    st.subheader("Tra cứu Quy định Nội bộ có Phân quyền (RBAC Secure RAG)")
    
    col_q, col_k = st.columns([4, 1])
    with col_q:
        question_input = st.text_area(
            "Nhập câu hỏi tra cứu quy định:",
            value="Quy định về việc bảo quản và vận chuyển tiền mặt, tài sản quý tại quầy giao dịch và kho tiền?",
            height=100
        )
    with col_k:
        top_k = st.slider("Top-K Chunks", min_value=1, max_value=10, value=3)
        retrieval_method = st.selectbox("Search Method", options=["bm25", "hybrid", "hybrid_rerank"], index=0)

    if st.button("🔍 TRA CỨU QUY ĐỊNH", type="primary", use_container_width=True):
        with st.spinner("Đang kiểm tra RBAC Pre-filter và chạy Secure Retrieval..."):
            res = lookup_svc.lookup(
                question=question_input,
                user_role=user_role,
                top_k=top_k,
                method=retrieval_method
            )

        st.divider()
        
        # Access Decision & Scope Summary
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Request ID", res["request_id"][:13] + "...")
        with col_m2:
            st.metric("Role hiện tại", res["user_role"])
        with col_m3:
            st.metric("Citations trả về", len(res["citations"]))
        with col_m4:
            if res["answer"] == "Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập.":
                st.markdown('<span class="badge-denied">DENIED / INSUFFICIENT</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-granted">ACCESS GRANTED</span>', unsafe_allow_html=True)

        st.caption(res["access_scope"])

        # Display Answer
        st.markdown("### 💬 Câu trả lời của AI:")
        if res["answer"] == "Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập.":
            st.error(f"🚫 {res['answer']}")
            st.info("💡 Lưu ý: Các văn bản không thuộc quyền xem của vai trò hiện tại đã bị Pre-filter loại bỏ hoàn toàn khỏi Context.")
        else:
            st.success(res["answer"])

        # Display Citations (Only if access granted & citations exist)
        if res["citations"] and res["answer"] != "Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập.":
            st.markdown("### 📌 Trích dẫn Nguồn Pháp lý (Citations):")
            for cit in res["citations"]:
                st.markdown(f'<div class="citation-box">📖 {cit}</div>', unsafe_allow_html=True)

        # Display Retrieved Chunk Metadata Table
        if res["retrieved_chunks"] and res["answer"] != "Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập.":
            with st.expander("📄 Chi tiết các Chunk được xem trong Context (Click để mở)"):
                for chunk in res["retrieved_chunks"]:
                    st.markdown(f"**Chunk ID**: `{chunk['chunk_id']}` | **Doc ID**: `{chunk['document_id']}`")
                    st.markdown(f"**Title**: {chunk.get('title')}")
                    st.text_area(f"Nội dung Chunk ({chunk['chunk_id']})", value=chunk.get('text', ''), height=120, key=chunk['chunk_id'])
                    st.divider()

# ==============================================================================
# TAB 2: COMPLIANCE GAP CHECKER (USE CASE 2)
# ==============================================================================
with tab2:
    st.subheader("AI Compliance Gap Checker (So sánh Tuân thủ Quy định)")
    
    # Inspect Data Readiness
    readiness = gap_chk.inspect_data_readiness()
    
    if not readiness["is_data_ready"]:
        st.warning("⚠️ COMPLIANCE GAP DATA: INSUFFICIENT — DATA GAP DETECTED")
        st.info(
            "Tập dữ liệu nguồn `chunks_secure.csv` hiện tại có 30 văn bản quy định nhà nước (EXTERNAL_REQUIREMENT) "
            "nhưng khuyết thiếu tập dữ liệu quy định nội bộ (INTERNAL_POLICY).\n\n"
            "**Nguyên tắc Quản trị**: Hệ thống không tự tạo văn bản giả hoặc sinh kết luận tuân thủ giả khi chưa có đủ bằng chứng hai phía."
        )
    else:
        st.success("🟢 COMPLIANCE GAP DATA: READY")

    st.markdown("### 📝 Chọn Yêu cầu Quy định Bên ngoài (NHNN Requirement):")
    sample_reqs = [
        "[Thông tư 01/2014/TT-NHNN] Điều 15: Bảo quản tiền mặt, tài sản quý tại quầy giao dịch và trong kho tiền hàng ngày.",
        "[Thông tư 01/2014/TT-NHNN] Điều 59: Tiêu chuẩn và quy trình vận chuyển tiền mặt bằng xe chuyên dùng.",
        "[Thông tư 41/2016/TT-NHNN] Điều 4: Quy định tỷ lệ an toàn vốn tối thiểu 8%."
    ]
    selected_req = st.selectbox("Chọn điều khoản NHNN mẫu:", options=sample_reqs)
    custom_req = st.text_area("Hoặc nhập điều khoản NHNN tùy chỉnh:", value=selected_req, height=80)

    if st.button("⚖️ PHÂN TÍCH GAP TUÂN THỦ", type="primary", use_container_width=True):
        with st.spinner("Đang đối soát bằng chứng giữa External Requirement và Internal Policy..."):
            dummy_chunk = {
                "document_id": "44209",
                "chunk_id": "44209_chunk_021",
                "text": custom_req,
                "citation": selected_req
            }
            gap_res = gap_chk.analyze_gap(dummy_chunk, user_role=user_role)

        st.divider()
        st.markdown("### 📊 Kết Quả Đánh Giá Compliance Gap Package:")
        
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.metric("Gap ID", gap_res["gap_id"])
        with col_g2:
            st.metric("Phân loại (Classification)", gap_res["classification"])
        with col_g3:
            st.markdown('<span class="badge-review">NEEDS_HUMAN_REVIEW</span>', unsafe_allow_html=True)
            st.caption("Yêu cầu kiểm toán viên xác minh")

        st.markdown(f"**Lý do đánh giá (Reason)**: {gap_res['reason']}")
        
        # Display Gap Table
        gap_table_df = pd.DataFrame([{
            "Gap ID": gap_res["gap_id"],
            "External Citation": gap_res["external_citation"],
            "Internal Citation": gap_res["internal_citation"],
            "Classification": gap_res["classification"],
            "Confidence": gap_res["confidence"],
            "Review Status": gap_res["review_status"]
        }])
        st.dataframe(gap_table_df, use_container_width=True)

# ==============================================================================
# TAB 3: AUDIT TRAIL
# ==============================================================================
with tab3:
    st.subheader("Nhật Ký Truy Vết Audit Log (Audit Trail Viewer)")
    st.caption("Hiển thị nhật ký truy vấn phù hợp với vai trò demo hiện tại (Không làm lộ Secret/Key)")
    
    audit_file_path = os.path.join(buoi17_dir, "outputs", "audit_log.jsonl")
    
    if os.path.exists(audit_file_path):
        audit_entries = []
        with open(audit_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line.strip())
                        # Filter matching role or show all if Admin
                        if user_role == "Admin" or entry.get("user_role") == user_role:
                            audit_entries.append(entry)
                    except Exception:
                        pass
        
        if audit_entries:
            st.success(f"Tìm thấy {len(audit_entries)} bản ghi Audit Log khớp với Role [{user_role}].")
            df_audit = pd.DataFrame(audit_entries)
            st.dataframe(
                df_audit[["timestamp", "request_id", "user_role", "question", "access_scope", "answer_status", "retrieved_count"]],
                use_container_width=True
            )
            with st.expander("🔍 Xem toàn bộ dữ liệu Audit Log thô (Raw JSONL)"):
                st.json(audit_entries)
        else:
            st.info(f"Chưa có bản ghi Audit Log nào cho Role [{user_role}]. Hãy thực hiện tra cứu ở Tab 1 để tạo log.")
    else:
        st.info("Chưa tìm thấy file audit_log.jsonl. Hãy thực hiện tra cứu ở Tab 1 để tự động ghi log.")
