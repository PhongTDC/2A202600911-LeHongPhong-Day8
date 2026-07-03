import os
from markitdown import MarkItDown

def convert_all_to_markdown():
    md = MarkItDown()
    folders = [
        ("data/landing/legal", "data/standardized/legal"),
        ("data/landing/news", "data/standardized/news")
    ]
    
    for src_dir, dest_dir in folders:
        if not os.path.exists(src_dir):
            continue
        os.makedirs(dest_dir, exist_ok=True)
        
        for file_name in os.listdir(src_dir):
            src_file = os.path.join(src_dir, file_name)
            if os.path.isdir(src_file):
                continue
                
            base_name, _ = os.path.splitext(file_name)
            dest_file = os.path.join(dest_dir, f"{base_name}.md")
            
            try:
                if file_name.endswith(".json"):
                    import json
                    with open(src_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    with open(dest_file, "w", encoding="utf-8") as f:
                        f.write(data.get("markdown", ""))
                else:
                    result = md.convert(src_file)
                    with open(dest_file, "w", encoding="utf-8") as f:
                        f.write(result.text_content)
                print(f"✓ Converted: {dest_file}")
            except Exception as e:
                print(f"❌ Fail to convert {file_name}: {e}")

if __name__ == "__main__":
    convert_all_to_markdown()
