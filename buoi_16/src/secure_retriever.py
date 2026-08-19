import os
import sys
import json
import re
import pandas as pd
import numpy as np

# Add src to sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import config
from bm25_retriever import BM25Retriever
from dense_retriever import DenseRetriever
from hybrid_retriever import HybridRetriever
from reranker import Reranker

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

def is_role_authorized(chunk_allowed_roles_json, user_roles: list) -> bool:
    """
    Checks if there is an intersection between chunk's allowed_roles and user's active roles.
    """
    if not user_roles:
        return False

    if isinstance(chunk_allowed_roles_json, str):
        try:
            chunk_roles = json.loads(chunk_allowed_roles_json)
        except Exception:
            chunk_roles = [chunk_allowed_roles_json]
    elif isinstance(chunk_allowed_roles_json, (list, set, tuple)):
        chunk_roles = list(chunk_allowed_roles_json)
    else:
        chunk_roles = ["Guest"]

    # Case insensitive intersection check
    user_roles_lower = {str(r).strip().lower() for r in user_roles}
    for r in chunk_roles:
        if str(r).strip().lower() in user_roles_lower:
            return True
    return False

class SecureRetriever:
    def __init__(self, df_corpus: pd.DataFrame = None):
        if df_corpus is None:
            secure_csv = os.path.join(base_dir, "data", "processed", "chunks_secure.csv")
            if not os.path.exists(secure_csv):
                # Fallback to chunks_normalized.csv if chunks_secure.csv not yet generated
                secure_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
            
            self.df_corpus = pd.read_csv(secure_csv, dtype=str)
            if 'allowed_roles' not in self.df_corpus.columns:
                self.df_corpus['allowed_roles'] = json.dumps(["Admin", "HR", "Risk_Manager", "Legal_Officer", "Bank_Staff", "Staff", "Guest"])
        else:
            self.df_corpus = df_corpus.copy()

        # Neo4j Driver setup
        self.driver = None
        if GraphDatabase and config.NEO4J_URI:
            try:
                self.driver = GraphDatabase.driver(
                    config.NEO4J_URI,
                    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
                )
            except Exception:
                self.driver = None

        # Load local relationships CSV for Graph Hints fallback
        self.rel_csv_path = os.path.join(base_dir, "..", "kb+hops", "relationships.csv")
        self.df_relationships = None
        if os.path.exists(self.rel_csv_path):
            try:
                self.df_relationships = pd.read_csv(self.rel_csv_path, dtype=str)
            except Exception:
                self.df_relationships = None

    def retrieve(self, question: str, user_roles: list, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> tuple:
        """
        Secure retrieval function for Buổi 15 RBAC.
        Inputs:
            question: query text (str)
            user_roles: active user roles list (e.g. ['Guest'], ['HR', 'Staff'])
            method: 'bm25', 'dense', 'hybrid', 'hybrid_rerank'
            top_k: int
            candidate_k: int
        Returns:
            (filtered_results_list, total_filtered_out_count)
        """
        if not user_roles:
            user_roles = ["Guest"]

        # 1. Pre-filter corpus DataFrame based on user_roles
        auth_mask = self.df_corpus['allowed_roles'].apply(lambda r: is_role_authorized(r, user_roles))
        df_auth = self.df_corpus[auth_mask].copy()
        total_filtered_out = len(self.df_corpus) - len(df_auth)

        if df_auth.empty:
            return [], total_filtered_out

        # Initialize engines on authorized corpus subset only
        bm25_engine = BM25Retriever(df_auth)
        dense_engine = DenseRetriever(df_auth)
        hybrid_engine = HybridRetriever(bm25_engine, dense_engine, rrf_k=60)
        reranker_engine = Reranker()

        method = method.lower().strip()

        if method == "bm25":
            raw_results = bm25_engine.search(question, top_k=top_k)
            formatted = []
            for item in raw_results:
                row_match = df_auth[df_auth['chunk_id'] == item['chunk_id']].iloc[0]
                formatted.append({
                    'rank': item['rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['retrieval_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'bm25',
                    'allowed_roles': json.loads(row_match['allowed_roles']) if isinstance(row_match['allowed_roles'], str) else row_match['allowed_roles']
                })
            return formatted, total_filtered_out

        elif method == "dense":
            raw_results = dense_engine.search(question, top_k=top_k)
            formatted = []
            for item in raw_results:
                row_match = df_auth[df_auth['chunk_id'] == item['chunk_id']].iloc[0]
                formatted.append({
                    'rank': item['rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['retrieval_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'dense',
                    'allowed_roles': json.loads(row_match['allowed_roles']) if isinstance(row_match['allowed_roles'], str) else row_match['allowed_roles']
                })
            return formatted, total_filtered_out

        elif method == "hybrid":
            raw_results = hybrid_engine.search(question, top_k=top_k, candidate_k=candidate_k)
            formatted = []
            for item in raw_results:
                row_match = df_auth[df_auth['chunk_id'] == item['chunk_id']].iloc[0]
                formatted.append({
                    'rank': item['final_rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['rrf_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'hybrid',
                    'bm25_rank': item['bm25_rank'],
                    'dense_rank': item['dense_rank'],
                    'rrf_score': item['rrf_score'],
                    'allowed_roles': json.loads(row_match['allowed_roles']) if isinstance(row_match['allowed_roles'], str) else row_match['allowed_roles']
                })
            return formatted, total_filtered_out

        elif method == "hybrid_rerank":
            candidates = hybrid_engine.search(question, top_k=candidate_k, candidate_k=candidate_k)
            # Reranker receives ONLY authorized candidates
            reranked = reranker_engine.rerank(question, candidates, top_k=top_k)
            formatted = []
            for item in reranked:
                row_match = df_auth[df_auth['chunk_id'] == item['chunk_id']].iloc[0]
                formatted.append({
                    'rank': item['final_rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['rerank_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'hybrid_rerank',
                    'hybrid_rank': item['hybrid_rank'],
                    'hybrid_score': item['hybrid_score'],
                    'rerank_score': item['rerank_score'],
                    'rerank_method': item.get('rerank_method', 'RERANK'),
                    'allowed_roles': json.loads(row_match['allowed_roles']) if isinstance(row_match['allowed_roles'], str) else row_match['allowed_roles']
                })
            return formatted, total_filtered_out
        else:
            raise ValueError(f"Method '{method}' không hợp lệ.")

    def get_secure_graph_hints(self, retrieved_results: list, user_roles: list) -> dict:
        """
        Extracts 1-hop direct relationships from Neo4j or local relationships.csv
        enforcing RBAC rule: WHERE any(role IN node.allowed_roles WHERE role IN $user_roles).
        """
        if not user_roles:
            user_roles = ["Guest"]

        doc_ids = list(dict.fromkeys([item['document_id'] for item in retrieved_results if 'document_id' in item]))
        chunk_ids = [item['chunk_id'] for item in retrieved_results if 'chunk_id' in item]

        hints = {
            'retrieved_doc_ids': doc_ids,
            'retrieved_chunk_ids': chunk_ids,
            'direct_relationships': [],
            'source': 'relationships.csv (local secure fallback)',
            'neo4j_active': False
        }

        # 1. Try Neo4j Cypher query with RBAC WHERE filtering
        if self.driver:
            cypher_q = """
            MATCH (v:VanBan)-[r]->(target)
            WHERE v.document_id IN $doc_ids
              AND any(role IN v.allowed_roles WHERE role IN $user_roles)
            RETURN v.document_id AS source, type(r) AS relationship, 
                   coalesce(target.document_id, target.chunk_id, labels(target)[0]) AS target,
                   coalesce(target.title, target.article, 'N/A') AS evidence
            LIMIT 10
            """
            try:
                with self.driver.session(database=config.NEO4J_DATABASE) as session:
                    res = session.run(cypher_q, doc_ids=doc_ids, user_roles=user_roles)
                    rel_list = []
                    for record in res:
                        rel_list.append({
                            'source': record['source'],
                            'relationship': record['relationship'],
                            'target': record['target'],
                            'evidence': str(record['evidence'])[:80]
                        })
                    if rel_list:
                        hints['direct_relationships'] = rel_list
                        hints['source'] = 'Neo4j Cypher (Secure Filtered)'
                        hints['neo4j_active'] = True
                        return hints
            except Exception:
                pass

        # 2. Local relationships.csv fallback filtered by authorized doc_ids
        if self.df_relationships is not None and not self.df_relationships.empty:
            matched_rels = self.df_relationships[
                self.df_relationships['source'].isin(doc_ids) | self.df_relationships['target'].isin(doc_ids)
            ]
            
            rel_list = []
            for _, r in matched_rels.head(10).iterrows():
                rel_list.append({
                    'source': r['source'],
                    'relationship': r['relationship_type'],
                    'target': r['target'],
                    'evidence': str(r.get('evidence', 'N/A'))[:80]
                })
            hints['direct_relationships'] = rel_list

        return hints

# Global standalone helper function
def retrieve_secure(question: str, user_roles: list, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> tuple:
    engine = SecureRetriever()
    return engine.retrieve(question, user_roles=user_roles, method=method, top_k=top_k, candidate_k=candidate_k)
