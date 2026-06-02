class MailMessage:
    def __init__(self, path, text):
        self.path = path
        self.text = text

    @property
    def filename(self):
        return self.path.name
