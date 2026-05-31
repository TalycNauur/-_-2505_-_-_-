set -euo pipefail

INPUT_DIR="${1:-inbox}"
OUTPUT_DIR="${2:-sorted_mail}"
REPORTS_DIR="${3:-reports}"

echo "Запуск приложения"
echo "Папка с письмами: $INPUT_DIR"
echo "Папка для результата: $OUTPUT_DIR"
echo "Папка для отчетов: $REPORTS_DIR"

if [ ! -d "$INPUT_DIR" ]; then
  echo "Ошибка: папка '$INPUT_DIR' не найдена"
  exit 1
fi

mkdir -p "$REPORTS_DIR"

python3 main.py --input "$INPUT_DIR" --output "$OUTPUT_DIR" --reports "$REPORTS_DIR"

echo
echo "Краткий отчет:"
cat "$REPORTS_DIR/summary.txt"

echo "Готово"
