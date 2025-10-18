import json
import os

REPORT_JSON = os.path.join("reports", "report.json")
SUMMARY_TXT = os.path.join("reports", "summary.txt")

def extract_summary():
    if not os.path.exists(REPORT_JSON):
        print(f"❌ Report file not found: {REPORT_JSON}")
        return

    with open(REPORT_JSON, encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)

    os.makedirs("reports", exist_ok=True)
    with open(SUMMARY_TXT, "w", encoding="utf-8") as out:
        out.write(f"Total: {total}\nPassed: {passed}\nFailed: {failed}\nSkipped: {skipped}\n")

    print("✅ Summary extracted successfully.")
    print(open(SUMMARY_TXT).read())

if __name__ == "__main__":
    extract_summary()
