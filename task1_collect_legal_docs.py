import os

def setup_folders():
    paths = [
        "data/landing/legal",
        "data/landing/news",
        "data/standardized/legal",
        "data/standardized/news"
    ]
    for path in paths:
        os.makedirs(path, exist_ok=True)
    print("✓ Cấu trúc thư mục data đã được khởi tạo.")

if __name__ == "__main__":
    setup_folders()
