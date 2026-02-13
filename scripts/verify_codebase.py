import os
import subprocess
import re
import sys

def run_test(command):
    print(f"🏃 Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Pass")
        return True, result.stdout
    else:
        print(f"❌ Fail")
        print(result.stderr)
        return False, result.stderr

def check_english_comments():
    print("🔍 Checking for Korean characters in source code (English comment policy)")
    # Using unicode escapes to avoid triggering this check on this script itself
    ko_regex = re.compile('[\uac00-\ud7af]')
    violations = []
    
    # Scan python files
    for root, _, files in os.walk("."):
        # Exclude common directories and this specific script
        if any(d in root for d in ["venv", ".git", "scripts", ".venv"]):
            continue
        for file in files:
            if file.endswith(".py") and file != "verify_codebase.py":
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if ko_regex.search(line):
                            violations.append(f"{path}:{i} - {line.strip()}")
    
    if violations:
        print(f"❌ Found {len(violations)} files with Korean characters")
        for v in violations[:5]: # Show first 5
            print(f"  > {v}")
        return False
    print("✅ No Korean characters found in source code")
    return True

def verify_all():
    print("🚀 Starting All-in-One Codebase Verification")
    print("-" * 50)
    
    results = {}
    
    # 1. Functional Tests
    test_files = [f for f in os.listdir("tests") if f.startswith("test_") and f.endswith(".py")]
    for tf in test_files:
        success, _ = run_test(f"python3 tests/{tf}")
        results[f"Functional Test [{tf}]"] = success
    
    # 2. English Comment Policy
    results["English Comment Policy"] = check_english_comments()
    
    # 3. Dual-Language Docs Sync
    success, _ = run_test("python3 scripts/sync_docs.py")
    results["Dual-Language Sync"] = success
    
    print("-" * 50)
    print("📊 VERIFICATION SUMMARY")
    all_pass = True
    for task, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{task.ljust(40)}: {status}")
        if not passed:
            all_pass = False
    
    if all_pass:
        print("\n🎊 CODEBASE IS CLEAN AND STABLE!")
    else:
        print("\n⚠️ SOME VERIFICATIONS FAILED. Please review the logs.")
        sys.exit(1)

if __name__ == "__main__":
    verify_all()
