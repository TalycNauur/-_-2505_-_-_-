import argparse
from pathlib import Path
from mail_app.processor import MailProcessor

def parse_args():
    parser = argparse.ArgumentParser(description = "Сортировка писем по папкам")
    
    parser.add_argument("--input", default = "inbox", help = "входящие")
    parser.add_argument("--output", default = "sorted_mail", help = "отсортированные")
    parser.add_argument("--reports", default = "reports", help = "отчёты")
    parser.add_argument("--dry-run", action = "store_true", help = "dry run")

    return parser.parse_args()

args = parse_args()

inbox_dir = Path(args.input)

if not inbox_dir.exists():
    raise SystemExit(f"Не предоставлена папка: {inbox_dir}")

processor = MailProcessor(
    inbox_dir = inbox_dir,
    output_dir = Path(args.output),
    reports_dir = Path(args.reports),
    dry_run = args.dry_run,
)
result = processor.process()

print("Процесс завершён")
print(f"Всего файлов: {result['total_files']}")

for category, count in result["categories"].items():
    print(f"{category}: {count}")