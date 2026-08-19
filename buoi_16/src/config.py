import os
import json
from dotenv import load_dotenv

# Path resolution relative to buoi_14 root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
ROLES_JSON_PATH = os.path.join(BASE_DIR, "roles.json")

# Load local .env
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH, override=True)
else:
    load_dotenv(override=True)

# Neo4j Database Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")

# Load Valid Roles
VALID_ROLES = ["Admin", "Legal_Officer", "Bank_Staff", "Guest"]
ROLE_CONFIG = {}

if os.path.exists(ROLES_JSON_PATH):
    try:
        with open(ROLES_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            ROLE_CONFIG = data
            VALID_ROLES = [r["name"] for r in data.get("roles", [])]
    except Exception as e:
        print(f" Warning: Không thể đọc roles.json ({e}). Sử dụng cấu hình mặc định.")

def validate_role(role_name: str) -> str:
    """Ensures role_name is valid to prevent typos."""
    if not role_name:
        return "Guest"
    role_clean = role_name.strip()
    for valid in VALID_ROLES:
        if valid.lower() == role_clean.lower():
            return valid
    raise ValueError(f"Role '{role_name}' không hợp lệ. Chọn một trong: {VALID_ROLES}")

def get_allowed_labels(role_name: str) -> list:
    """Returns allowed security labels for a given role."""
    r_valid = validate_role(role_name)
    if "roles" in ROLE_CONFIG:
        for r in ROLE_CONFIG["roles"]:
            if r["name"] == r_valid:
                return r.get("allowed_security_labels", ["PUBLIC"])
    # Default fallback mapping
    mapping = {
        "Admin": ["PUBLIC", "INTERNAL", "RESTRICTED", "CONFIDENTIAL"],
        "Legal_Officer": ["PUBLIC", "INTERNAL", "RESTRICTED"],
        "Bank_Staff": ["PUBLIC", "INTERNAL"],
        "Guest": ["PUBLIC"]
    }
    return mapping.get(r_valid, ["PUBLIC"])
