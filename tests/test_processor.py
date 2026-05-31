import tempfile
import unittest
from pathlib import Path
from mail_app.processor import MailProcessor

class TestMailProcessor(unittest.TestCase):
    def test_processor_moves_files_and_creates_reports(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            inbox = root / "inbox"
            output = root / "sorted"
            reports = root / "reports"

            inbox.mkdir()

            (inbox / "incident.txt").write_text("Срочно: ошибка 500", encoding = "utf-8")
            (inbox / "unknown.txt").write_text("Непонятное письмо", encoding = "utf-8")
            (inbox / "photo.jpeg").write_text("Это не картинка", encoding = "utf-8")
            (inbox / "mail.json").write_text("Нестандартный файл", encoding = "utf-8")

            result = MailProcessor(inbox, output, reports).process()

            self.assertEqual(result["total_files"], 4)

            self.assertTrue((output / "Критичные моменты" / "incident.txt").exists())
            self.assertTrue((output / "Другое" / "unknown.txt").exists())
            self.assertTrue((output / "Ошибочные файлы" / "photo.jpeg").exists())
            self.assertTrue((output / "Ошибочные файлы" / "mail.json").exists())

            self.assertTrue((reports / "summary.txt").exists())
            self.assertTrue((reports / "actions.txt").exists())

            self.assertEqual(list(inbox.iterdir()), [])

    def test_processor_dry_run_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            inbox = root / "inbox"
            output = root / "sorted"
            reports = root / "reports"

            inbox.mkdir()

            mail_path = inbox / "mail.txt"
            mail_path.write_text("тестовое письмо для dry run", encoding = "utf-8")

            result = MailProcessor(inbox, output, reports, dry_run = True).process()

            self.assertTrue(result["dry_run"])
            self.assertTrue(mail_path.exists())

            self.assertFalse((output / "Другое" / "mail.txt").exists())

if "__main__" == __name__:
    unittest.main()