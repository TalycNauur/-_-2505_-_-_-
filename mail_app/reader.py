from mail_app.models import MailMessage

class MailReader:
    ext = {".txt", ""}

    def read(self, path):
        suffix = path.suffix.lower()

        if suffix not in self.ext:
            raise ValueError(f"Тип файла не поддерживается: {suffix or 'no extension'}")

        with open(path, "r", encoding = "utf-8") as file:
            text = file.read().strip()

        if not text:
            raise ValueError("пустой файл")

        return MailMessage(path = path, text = text)
