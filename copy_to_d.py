"""
Script sao chép / di chuyển toàn bộ thư mục C:\\03.08 sang D:\\03.08
Sử dụng thư viện shutil của Python.
"""

import os
import shutil
import sys

def copy_workspace():
    source_dir = r"C:\03.08"
    target_dir = r"D:\03.08"

    print(f"🚀 Bắt đầu sao chép thư mục từ [{source_dir}] sang [{target_dir}]...")

    if not os.path.exists(source_dir):
        print(f"❌ Thư mục nguồn {source_dir} không tồn tại!")
        return

    os.makedirs(target_dir, exist_ok=True)

    # Lọc bỏ file copy_to_d.py tạm thời hoặc copy toàn bộ
    def ignore_patterns(dir, contents):
        # Tránh lặp đệ quy nếu trỏ lung tung
        return []

    try:
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        print(f"✅ Đã sao chép thành công toàn bộ thư mục sang {target_dir}!")
    except Exception as e:
        print(f"⚠️ Có lỗi trong quá trình copy: {e}")

if __name__ == "__main__":
    copy_workspace()
