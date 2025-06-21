import argparse
from backend.auto_scanner import scan_projects, analyze_and_complete
from backend.llm import ask_llm

def main():
    parser = argparse.ArgumentParser(description="🧠 Autopilot Dev Assistant")
    parser.add_argument("--scan", action="store_true", help="Scan for new projects")
    parser.add_argument("--complete", type=str, help="Complete a given project path")
    parser.add_argument("--list", action="store_true", help="List tracked projects")
    args = parser.parse_args()

    if args.scan:
        results = scan_projects()
        print("🔍 Found projects:")
        for key, val in results.items():
            print(f"- {key}: {val['status']}")

    elif args.complete:
        print(f"📦 Completing project: {args.complete}")
        result = analyze_and_complete(args.complete)
        print("✅ Done:", result)

    elif args.list:
        from backend.auto_scanner import load_history
        history = load_history()
        print("🗃️ Tracked projects:")
        for key, val in history.items():
            print(f"- {key}: {val['status']}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
