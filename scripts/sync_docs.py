import os
import sys

def sync_docs(docs_dir="docs"):
    """
    Checks for missing pairs of .en.md and .ko.md files and 
    synchronizes missing files with placeholders if necessary.
    """
    files = os.listdir(docs_dir)
    en_files = {f.replace(".en.md", "") for f in files if f.endswith(".en.md")}
    ko_files = {f.replace(".ko.md", "") for f in files if f.endswith(".ko.md")}
    
    all_bases = en_files.union(ko_files)
    
    for base in all_bases:
        en_path = os.path.join(docs_dir, f"{base}.en.md")
        ko_path = os.path.join(docs_dir, f"{base}.ko.md")
        
        if not os.path.exists(ko_path):
            print(f"⚠️ Missing Korean version for: {base}.en.md. Creating placeholder...")
            with open(en_path, 'r') as f:
                content = f.read()
            with open(ko_path, 'w') as f:
                f.write(f"<!-- TRANSLATION_REQUIRED -->\n# {base} (Korean)\n\nOriginal content from {base}.en.md needs translation.\n\n" + content)
        
        if not os.path.exists(en_path):
            print(f"⚠️ Missing English version for: {base}.ko.md. Creating placeholder...")
            with open(ko_path, 'r') as f:
                content = f.read()
            with open(en_path, 'w') as f:
                f.write(f"<!-- TRANSLATION_REQUIRED -->\n# {base} (English)\n\nOriginal content from {base}.ko.md needs translation.\n\n" + content)

if __name__ == "__main__":
    sync_docs()
