import os
import sys
import pandas as pd
import streamlit as st

# Add src to sys.path
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import config
from secure_retriever import SecureRetriever

# Page config
st.set_page_config(
    page_title="RAG Secure Search (RBAC) — Buổi 15",
    page_icon="🔒",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .role-badge {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 6px;
    }
    .citation-box {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    .filtered-warning {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 10px 14px;
        border-radius: 6px;
        border-left: 4px solid #EF4444;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .graph-hint-card {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 14px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Secure Retriever Engine
@st.cache_resource
def get_secure_retriever():
    return SecureRetriever()

try:
    secure_retriever = get_secure_retriever()
except Exception as e:
    st.error(f"Lỗi khởi tạo SecureRetriever: {e}")
    st.stop()

# Title
st.markdown('<div class="main-header">🔒 RAG Secure Search (RBAC Data Level) — Buổi 15</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hệ thống Tìm kiếm An toàn Phân quyền Vai trò ở Mức Dữ liệu (BM25, Dense, Hybrid RRF & Rerank)</div>', unsafe_allow_html=True)

st.divider()

# Sidebar Controls
with st.sidebar:
    st.header("👤 Cấu Hình Người Dùng & RBAC")
    
    # Multiselect for User Roles
    available_roles = config.VALID_ROLES + ["HR", "Risk_Manager", "Staff"]
    # Deduplicate while preserving order
    available_roles = list(dict.fromkeys(available_roles))

    selected_user_roles = st.multiselect(
        "Vai trò của bạn (Your Roles):",
        options=available_roles,
        default=["Guest"],
        help="Chọn một hoặc nhiều vai trò để kiểm thử quyền truy cập dữ liệu."
    )

    st.divider()
    st.header("⚙️ Cấu Hình Retrieval")
    
    method_display_map = {
        "BM25": "bm25",
        "Dense": "dense",
        "Hybrid (RRF)": "hybrid",
        "Hybrid + Rerank": "hybrid_rerank"
    }
    
    selected_method_label = st.selectbox(
        "Chọn Phương Thức Retrieval:",
        options=list(method_display_map.keys()),
        index=3
    )
    selected_method = method_display_map[selected_method_label]

    top_k = st.slider("Top-K Kết Quả:", min_value=1, max_value=10, value=5)
    candidate_k = st.slider("Candidate-K (Hybrid Candidates):", min_value=10, max_value=30, value=20)
    
    st.info(f"🔑 **Vai trò hiện tại:** `{selected_user_roles if selected_user_roles else ['Guest']}`")

# Main Query Input Form
with st.form("secure_query_form"):
    query_text = st.text_input(
        "Nhập câu hỏi tìm kiếm:",
        value="Điều 4 Thông tư 01/2014/TT-NHNN đóng gói tiền mặt quy định những gì?",
        placeholder="Ví dụ: Quy trình thu hồi nợ xấu, bảng lương cấp quản lý..."
    )
    submit_button = st.form_submit_button("🔒 Tìm kiếm An toàn", type="primary")

if submit_button or query_text:
    active_roles = selected_user_roles if selected_user_roles else ["Guest"]
    
    st.subheader(f"📌 Kết Quả Tìm Kiếm An Toàn — [{selected_method_label}] — Roles: `{active_roles}`")

    # Execute Secure Retrieval
    results, total_filtered_out = secure_retriever.retrieve(
        query_text,
        user_roles=active_roles,
        method=selected_method,
        top_k=top_k,
        candidate_k=candidate_k
    )

    # Display Security Filter Alert Metric
    if total_filtered_out > 0:
        st.markdown(
            f'<div class="filtered-warning">🛡️ THÔNG BÁO BẢO MẬT: Hệ thống đã lọc bỏ <b>{total_filtered_out} chunks</b> do vai trò <code>{active_roles}</code> không đủ quyền truy cập.</div>',
            unsafe_allow_html=True
        )

    # If method is hybrid_rerank, display BEFORE RERANK vs AFTER RERANK comparison
    if selected_method == "hybrid_rerank":
        st.markdown("### 🔄 So Sánh Thứ Hạng Bảo Mật: BEFORE RERANK vs AFTER RERANK")
        col1, col2 = st.columns(2)
        
        before_results, _ = secure_retriever.retrieve(
            query_text, user_roles=active_roles, method="hybrid", top_k=top_k, candidate_k=candidate_k
        )
        
        with col1:
            st.markdown("#### 1️⃣ BEFORE RERANK (Hybrid Search Đã Lọc Quyền)")
            if before_results:
                df_b = pd.DataFrame(before_results)[['rank', 'chunk_id', 'document_id', 'score', 'allowed_roles']]
                df_b.columns = ['Rank', 'Chunk ID', 'Doc ID', 'RRF Score', 'Quyền Xem']
                st.dataframe(df_b, use_container_width=True, hide_index=True)
            else:
                st.info("Không có kết quả đủ quyền.")

        with col2:
            st.markdown("#### 2️⃣ AFTER RERANK (Reranked Final Đã Lọc Quyền)")
            if results:
                df_a = pd.DataFrame(results)[['rank', 'chunk_id', 'document_id', 'score', 'allowed_roles']]
                df_a.columns = ['Final Rank', 'Chunk ID', 'Doc ID', 'Rerank Score', 'Quyền Xem']
                st.dataframe(df_a, use_container_width=True, hide_index=True)
            else:
                st.info("Không có kết quả đủ quyền.")

        st.divider()

    if not results:
        st.warning("🔒 Không tìm thấy kết quả nào phù hợp với câu hỏi và vai trò hiện tại của bạn.")
    else:
        st.markdown(f"### 📋 Chi Tiết Top {len(results)} Chunks An Toàn Đã Trích Xuất")
        
        for idx, r in enumerate(results, 1):
            roles_str = ", ".join(r.get('allowed_roles', []))
            with st.expander(f"Top {r['rank']} | Chunk: {r['chunk_id']} | Quyền xem: [{roles_str}] | Score: {r['score']:.4f}", expanded=(idx==1)):
                st.markdown(f'<div class="citation-box">📌 Citation: {r["citation"]}</div>', unsafe_allow_html=True)
                
                m_c1, m_c2, m_c3, m_c4 = st.columns(4)
                m_c1.metric("Rank", r['rank'])
                m_c2.metric("Chunk ID", r['chunk_id'])
                m_c3.metric("Document ID", r['document_id'])
                m_c4.metric("Allowed Roles", f"[{roles_str}]")

                st.markdown("**Nội dung đoạn trích văn bản:**")
                st.text_area("Text Content", value=r['text'], height=150, key=f"sec_text_{r['chunk_id']}_{idx}")

    # Secure Graph Hints Section
    st.divider()
    st.markdown("### 🕸️ SECURE GRAPH HINTS (Bằng Chứng Liên Kết Đồ Thị Đã Lọc Quyền)")
    
    hints = secure_retriever.get_secure_graph_hints(results, active_roles)
    
    with st.container():
        st.markdown('<div class="graph-hint-card">', unsafe_allow_html=True)
        g_c1, g_c2, g_c3 = st.columns(3)
        g_c1.write(f"**Document IDs Được Phép Xem:** `{hints['retrieved_doc_ids']}`")
        g_c2.write(f"**Chunk IDs Được Phép Xem:** `{len(hints['retrieved_chunk_ids'])} chunks`")
        g_c3.write(f"**Nguồn Đồ Thị:** {hints['source']}")
        
        if hints['direct_relationships']:
            st.markdown("**Quan hệ 1-hop hợp lệ được phép xem:**")
            df_rel = pd.DataFrame(hints['direct_relationships'])
            df_rel.columns = ['Source Document', 'Relationship Type', 'Target Node / Entity', 'Evidence Snippet']
            st.dataframe(df_rel, use_container_width=True, hide_index=True)
        else:
            st.info("Không tìm thấy quan hệ 1-hop trực tiếp hợp lệ nào cho các vai trò này.")
            
        st.markdown('</div>', unsafe_allow_html=True)
