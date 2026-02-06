import os
import sys
from pathlib import Path

def check_file_exists(path: Path) -> bool:
    if path.exists():
        print(f"[OK] Found {path}")
        return True
    else:
        print(f"[FAIL] Missing {path}")
        return False

def check_content(path: Path, must_contain: list[str] = [], must_not_contain: list[str] = []) -> bool:
    if not path.exists():
        return False
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    passed = True
    for term in must_contain:
        if term not in content:
            print(f"[FAIL] {path} missing required term: '{term}'")
            passed = False
    
    for term in must_not_contain:
        if term in content:
            print(f"[WARN] {path} contains discouraged term: '{term}'")
            # Warnings don't fail the check
            
    if passed:
        print(f"[OK] Content verification for {path}")
    return passed

def main():
    root_dir = Path(__file__).parent.parent
    specs_dir = root_dir / "specs"
    
    print(f"Checking project specs in {root_dir}")
    
    required_files = [
        root_dir / "pyproject.toml",
        root_dir / "README.md",
        root_dir / "Dockerfile",
        specs_dir / "_meta.md",
        specs_dir / "api_contracts.md",
        specs_dir / "database_schema.md",
        specs_dir / "functional.md",
        specs_dir / "technical.md",
    ]
    
    all_passed = True
    
    print("\n--- Checking File Existence ---")
    for file_path in required_files:
        if not check_file_exists(file_path):
            all_passed = False

    print("\n--- Checking Spec Content ---")
    # Example: Ensure _meta.md has a Mission section
    if not check_content(specs_dir / "_meta.md", must_contain=["## Mission"]):
        all_passed = False
        
    # Example: Ensure pyproject.toml has the project name
    if not check_content(root_dir / "pyproject.toml", must_contain=["name = \"project-chimera\""]):
        all_passed = False

    if all_passed:
        print("\n[SUCCESS] All spec checks passed!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Some checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
