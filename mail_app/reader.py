from mail_app.models import MailMessage

class MailReader:
    TEXT_EXTENSIONS = {".txt", ""}

    def read(self, path):
        suffix = path.suffix.lower()

        if suffix not in self.TEXT_EXTENSIONS:
            raise ValueError(f"unsupported file type: {suffix or 'no extension'}")

        with open(path, "r", encoding = "utf-8") as file:
            text = file.read().strip()

        if not text:
            raise ValueError("empty mail file")

        return MailMessage(path = path, text = text)