import os
import sys
import json
import hashlib
import dotenv
from cryptography.fernet import Fernet

sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir)
base_dir = os.path.dirname(buoi17_dir)

# Load environment variables
dotenv.load_dotenv(os.path.join(base_dir, ".env"))
dotenv.load_dotenv(os.path.join(buoi17_dir, ".env"))

outputs_dir = os.path.join(buoi17_dir, "outputs")
config_dir = os.path.join(buoi17_dir, "config")

os.makedirs(outputs_dir, exist_ok=True)
os.makedirs(config_dir, exist_ok=True)

KEY_FILE = os.path.join(config_dir, "secret.key")
RAW_FILE = os.path.join(outputs_dir, "demo_audit_raw.jsonl")
ENC_FILE = os.path.join(outputs_dir, "demo_audit_encrypted.enc")
DEC_FILE = os.path.join(outputs_dir, "demo_audit_decrypted.jsonl")

def get_or_create_key() -> bytes:
    """
    Retrieves Fernet key from .env environment variable if defined,
    otherwise loads from *.key file or generates dynamically.
    Key is NEVER hardcoded in python source files.
    """
    env_key = os.getenv("ENCRYPTION_KEY")
    if env_key:
        return env_key.strip().encode('utf-8')

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as kf:
            return kf.read().strip()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as kf:
            kf.write(key)
        return key

def prepare_sample_audit_file() -> str:
    """
    Creates a sample audit trail JSONL file for encryption demonstration.
    """
    sample_records = [
        {"timestamp": "2026-08-21T20:30:00Z", "user_role": "Staff", "question": "Quy trình vận chuyển tiền mặt", "accessed_chunk": "44209_chunk_021", "access_decision": "GRANTED"},
        {"timestamp": "2026-08-21T20:31:15Z", "user_role": "Guest", "question": "Quy trình vận chuyển tiền mặt", "accessed_chunk": "44209_chunk_021", "access_decision": "DENIED_RBAC"},
        {"timestamp": "2026-08-21T20:32:05Z", "user_role": "Risk_Manager", "question": "Nội quy kho tiền", "accessed_chunk": "44209_chunk_043", "access_decision": "GRANTED"}
    ]
    with open(RAW_FILE, "w", encoding="utf-8") as f:
        for rec in sample_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return RAW_FILE

def run_encryption_demo():
    print("=== DEMO ENCRYPTION AT-REST (BUỔI 17) ===")
    
    # 1. Key setup
    key = get_or_create_key()
    fernet = Fernet(key)
    source_desc = ".env (ENCRYPTION_KEY)" if os.getenv("ENCRYPTION_KEY") else KEY_FILE
    print(f"[1] Encryption Key Loaded from: {source_desc}")
    print(f"    Key (Base64 URL-safe): {key.decode()[:10]}... (Len: {len(key)})")
    
    # 2. Prepare RAW file
    prepare_sample_audit_file()
    with open(RAW_FILE, "rb") as rf:
        raw_bytes = rf.read()
    raw_hash = hashlib.sha256(raw_bytes).hexdigest()
    print(f"[2] Raw Audit File Created: {RAW_FILE}")
    print(f"    Raw Size: {len(raw_bytes)} bytes | SHA256: {raw_hash}")
    
    # 3. Encrypt
    encrypted_bytes = fernet.encrypt(raw_bytes)
    with open(ENC_FILE, "wb") as ef:
        ef.write(encrypted_bytes)
    enc_hash = hashlib.sha256(encrypted_bytes).hexdigest()
    print(f"[3] File Encrypted -> {ENC_FILE}")
    print(f"    Encrypted Size: {len(encrypted_bytes)} bytes | SHA256: {enc_hash}")
    
    # 4. Decrypt & Match Check
    with open(ENC_FILE, "rb") as ef:
        bytes_to_decrypt = ef.read()
    decrypted_bytes = fernet.decrypt(bytes_to_decrypt)
    with open(DEC_FILE, "wb") as df:
        df.write(decrypted_bytes)
    dec_hash = hashlib.sha256(decrypted_bytes).hexdigest()
    print(f"[4] File Decrypted -> {DEC_FILE}")
    print(f"    Decrypted Size: {len(decrypted_bytes)} bytes | SHA256: {dec_hash}")
    
    # 5. Verification
    is_encrypt_pass = os.path.exists(ENC_FILE) and len(encrypted_bytes) > 0 and raw_bytes != encrypted_bytes
    is_match_pass = (raw_bytes == decrypted_bytes) and (raw_hash == dec_hash)
    
    print("\n=== DEMO VERIFICATION RESULTS ===")
    print(f"ENCRYPT RESULT: {'PASS' if is_encrypt_pass else 'FAIL'}")
    print(f"DECRYPT MATCH: {'PASS' if is_match_pass else 'FAIL'}")
    print("PRODUCTION READY: NO (Chỉ minh họa mã hóa file at-rest)")
    
    return {
        "encrypt_pass": is_encrypt_pass,
        "match_pass": is_match_pass,
        "raw_hash": raw_hash,
        "enc_hash": enc_hash,
        "dec_hash": dec_hash
    }

if __name__ == '__main__':
    run_encryption_demo()
