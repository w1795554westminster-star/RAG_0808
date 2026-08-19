import os
import sys
import pandas as pd
import streamlit as st

# Add src to sys.path
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from unified_retriever import UnifiedRetriever

# Page config
st.set_page_config(
    page_title="RAG Hybrid Search — Buổi 14",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for modern design
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
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid #3B82F6;
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
    .graph-hint-card {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 14px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Retriever Engine (cached)
@st.cache_resource
def get_retriever():
    return UnifiedRetriever()

try:
    retriever = get_retriever()
except Exception as e:
    st.error(f"Lỗi khởi tạo UnifiedRetriever: {e}")
    st.stop()

# Title
st.markdown('<div class="main-header">🔍 RAG Hybrid Search — Buổi 14</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Kiến trúc Tìm kiếm Hỗn hợp (BM25 + Dense RRF), Reranking & Mini Knowledge Graph Hints</div>', unsafe_allow_html=True)

st.divider()

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Cấu Hình Truy Vấn")
    
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
    
    st.info("💡 **Ghi chú:**\n- **BM25**: Khớp từ khóa pháp lý cứng.\n- **Dense**: Ngữ nghĩa vector.\n- **Hybrid**: Hợp nhất RRF.\n- **Rerank**: Đánh giá lại ngữ cảnh.")

# Main Input Form
with st.form("query_form"):
    query_text = st.text_input(
        "Nhập câu hỏi tìm kiếm:",
        value="Điều 4 Thông tư 01/2014/TT-NHNN đóng gói tiền mặt quy định những gì?",
        placeholder="Ví dụ: Quy định về bảo quản và vận chuyển tiền mặt..."
    )
    submit_button = st.form_submit_button("🔍 Tìm kiếm", type="primary")

if submit_button or query_text:
    if not query_text.strip():
        st.warning("Vui lòng nhập câu hỏi tìm kiếm.")
        st.stop()

    st.subheader(f"📌 Kết Quả Truy Vấn — [{selected_method_label}]")

    # If method is hybrid_rerank, display BEFORE vs AFTER RERANK comparison
    if selected_method == "hybrid_rerank":
        st.markdown("### 🔄 So Sánh Thứ Hạng: BEFORE RERANK vs AFTER RERANK")
        
        col1, col2 = st.columns(2)
        
        # Get BEFORE RERANK candidates
        before_results = retriever.retrieve(query_text, method="hybrid", top_k=top_k, candidate_k=candidate_k)
        
        # Get AFTER RERANK results
        after_results = retriever.retrieve(query_text, method="hybrid_rerank", top_k=top_k, candidate_k=candidate_k)

        with col1:
            st.markdown("#### 1️⃣ BEFORE RERANK (Hybrid Search)")
            df_before = pd.DataFrame(before_results)[['rank', 'chunk_id', 'document_id', 'bm25_rank', 'dense_rank', 'score']]
            df_before.columns = ['Rank', 'Chunk ID', 'Doc ID', 'BM25 Rank', 'Dense Rank', 'RRF Score']
            st.dataframe(df_before, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("#### 2️⃣ AFTER RERANK (Reranked Final)")
            df_after = pd.DataFrame(after_results)[['rank', 'chunk_id', 'document_id', 'hybrid_rank', 'hybrid_score', 'score']]
            df_after.columns = ['Final Rank', 'Chunk ID', 'Doc ID', 'Hybrid Rank', 'Hybrid Score', 'Rerank Score']
            st.dataframe(df_after, use_container_width=True, hide_index=True)

        st.divider()

    # Get final results for display
    results = retriever.retrieve(query_text, method=selected_method, top_k=top_k, candidate_k=candidate_k)

    if not results:
        st.error("Không tìm thấy kết quả phù hợp.")
    else:
        st.markdown(f"### 📋 Chi Tiết Top {len(results)} Chunks Được Trích Xuất")
        
        for idx, r in enumerate(results, 1):
            with st.expander(f"Top {r['rank']} | Chunk: {r['chunk_id']} | Score: {r['score']:.4f}", expanded=(idx==1)):
                st.markdown(f'<div class="citation-box">📌 Citation: {r["citation"]}</div>', unsafe_allow_html=True)
                
                # Metadata breakdown
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Rank", r['rank'])
                m_col2.metric("Chunk ID", r['chunk_id'])
                m_col3.metric("Document ID", r['document_id'])
                m_col4.metric("Method", r['retrieval_method'].upper())

                if 'bm25_rank' in r and 'dense_rank' in r:
                    sub_c1, sub_c2, sub_c3 = st.columns(3)
                    sub_c1.write(f"**BM25 Rank:** {r['bm25_rank']}")
                    sub_c2.write(f"**Dense Rank:** {r['dense_rank']}")
                    sub_c3.write(f"**RRF Score:** {r['rrf_score']:.6f}")

                if 'rerank_score' in r:
                    sub_c1, sub_c2 = st.columns(2)
                    sub_c1.write(f"**Hybrid Rank (Trước):** {r.get('hybrid_rank', 'N/A')}")
                    sub_c2.write(f"**Rerank Score (Sau):** {r['rerank_score']:.4f}")

                st.markdown("**Nội dung đoạn trích văn bản:**")
                st.text_area("Text Content", value=r['text'], height=160, key=f"text_{r['chunk_id']}_{idx}")

    # GRAPH HINTS Section
    st.divider()
    st.markdown("### 🕸️ GRAPH HINTS (Bằng Chứng Liên Kết Mini Knowledge Graph)")
    
    hints = retriever.get_graph_hints(results)
    
    with st.container():
        st.markdown('<div class="graph-hint-card">', unsafe_allow_html=True)
        g_c1, g_c2, g_c3 = st.columns(3)
        g_c1.write(f"**Retrieved Document IDs:** `{hints['retrieved_doc_ids']}`")
        g_c2.write(f"**Retrieved Chunk IDs:** `{len(hints['retrieved_chunk_ids'])} chunks`")
        g_c3.write(f"**Trạng thái Graph:** {hints['source']}")
        
        st.caption("ℹ️ *Lưu ý: Neo4j không kết nối trực tiếp trong màn hình này. Đồ thị đầy đủ xem tại Neo4j Browser.*")

        if hints['direct_relationships']:
            st.markdown("**Quan hệ 1-hop trực tiếp tìm thấy:**")
            df_rel = pd.DataFrame(hints['direct_relationships'])
            df_rel.columns = ['Source Document', 'Relationship Type', 'Target Node / Entity', 'Evidence Snippet']
            st.dataframe(df_rel, use_container_width=True, hide_index=True)
        else:
            st.info("Không tìm thấy quan hệ 1-hop trực tiếp nào trong Mini KG cho các văn bản này.")
            
        st.markdown('</div>', unsafe_allow_html=True)
