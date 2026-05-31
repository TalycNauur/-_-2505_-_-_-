import tempfile
import unittest
from pathlib import Path
from mail_app.reader import MailReader

class TestMailReader(unittest.TestCase):
    def setUp(self):
        self.reader = MailReader()

    def test_read_text_mail(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "mail.txt"

            path.write_text("Тема: Проверка\n\nТекст письма", encoding = "utf-8")

            mail = self.reader.read(path)

            self.assertEqual(mail.filename, "mail.txt")

            self.assertIn("Текст письма", mail.text)

    def test_reader_rejects_empty_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.txt"

            path.write_text("", encoding = "utf-8")

            with self.assertRaises(ValueError):
                self.reader.read(path)

    def test_reader_rejects_unknown_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "unknown.bin"

            path.write_bytes(b"data")

            with self.assertRaises(ValueError):
                self.reader.read(path)

if "__main__" == __name__:
    unittest.main()