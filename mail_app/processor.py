import logging
import os
import shutil
from mail_app.classifier import MailClassifier
from mail_app.reader import MailReader

class MailProcessor:

    def __init__(self, inbox_dir, output_dir, reports_dir, dry_run = False):
        self.inbox_dir = inbox_dir
        self.output_dir = output_dir
        self.reports_dir = reports_dir
        self.dry_run = dry_run

        self.reader = MailReader()
        self.classifier = MailClassifier()

        self.stats = {}
        self.actions = []

    def process(self):
        self._prepare_dirs()
        self._setup_logging()

        files = []
        for filename in sorted(os.listdir(self.inbox_dir)):
            path = self.inbox_dir / filename

            if path.is_file():
                files.append(path)

        logging.info("Found %s files in %s", len(files), self.inbox_dir)

        for path in files:
            self._process_file(path)

        result = {
            "total_files": len(files),
            "dry_run": self.dry_run,
            "categories": self._sorted_stats(),
        }
        self._write_reports(result)

        return result

    def _prepare_dirs(self):
        self.output_dir.mkdir(parents = True, exist_ok = True)
        self.reports_dir.mkdir(parents = True, exist_ok = True)
        (self.output_dir / "problem_files").mkdir(parents = True, exist_ok = True)

    def _setup_logging(self):
        log_path = self.reports_dir / "processing.log"

        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            force=True,
        )

    def _process_file(self, path):
        try:
            mail = self.reader.read(path)
            category = self.classifier.classify(mail)
            reason = "classified"

        except Exception as error:
            category = "problem_files"
            reason = str(error)

            logging.warning("Problem with %s: %s", path.name, error)

        if category not in self.stats:
            self.stats[category] = 0
        self.stats[category] += 1

        target = self._safe_target_path(self.output_dir / category, path.name)

        self.actions.append(
            {
                "file": path.name,
                "category": category,
                "target": str(target),
                "reason": reason,
            }
        )

        if not self.dry_run:
            target.parent.mkdir(parent = True, exist_ok = True)

            shutil.move(str(path), str(target))

        logging.info("%s -> %s (%s)", path.name, category, reason)

    def _safe_target_path(self, category_dir, filename):
        target = category_dir / filename

        if not target.exists():
            return target

        stem = target.stem
        suffix = target.suffix
        number = 1

        while True:
            new_target = category_dir / f"{stem}_{number}{suffix}"

            if not new_target.exists():
                return new_target
            
            number += 1

    def _sorted_stats(self):
        sorted_stats = {}

        for category in sorted(self.stats):
            sorted_stats[category] = self.stats[category]

        return sorted_stats

    def _write_reports(self, result):
        summary_path = self.reports_dir / "summary.txt"
        actions_path = self.reports_dir / "actions.txt"

        lines = [
            "Mail processing summary",
            f"Total files: {result['total_files']}",
            f"Dry run: {result['dry_run']}",
            "",
            "Categories:",
        ]

        for category, count in result["categories"].items():
            lines.append(f"- {category}: {count}")

        summary_path.write_text("\n".join(lines) + "\n", encoding = "utf-8")

        action_lines = ["File processing details:"]
        for action in self.actions:
            line = f"{action['file']} -> {action['category']} ({action['reason']})"
            action_lines.append(line)

        actions_path.write_text("\n".join(action_lines) + "\n", encoding = "utf-8")