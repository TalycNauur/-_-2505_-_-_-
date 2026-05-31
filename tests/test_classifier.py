import tempfile
import unittest
from pathlib import Path
from mail_app.classifier import MailClassifier
from mail_app.models import MailMessage

class TestMailClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = MailClassifier()

    def test_classify_categories(self):
        cases = [
            ("Тема: Срочно, система возвращает ошибка 500", "Критичные моменты"),
            ("Прошу выдать доступ к GitLab новому сотруднику", "Запросы"),
            ("Принтер зависает, нужна заявка на ремонт", "Аппаратура"),
            ("Chrome не запускается после обновления", "Поддержка ПО"),
            ("Счёт на оплату и закрывающие документы", "Документы"),
            ("Прошу оформить больничный лист", "Эйчар"),
            ("Клиент спрашивает статус тикета", "Заявки клиентов"),
            ("Корпоративный дайджест и плановый отчёт", "Информация"),
            ("Вы выиграли iPhone, подтвердите личность", "Спам"),
            ("Просто нейтральное сообщение без известных слов", "Другое"),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "mail.txt"

            for text, expected_category in cases:
                with self.subTest(text = text):
                    mail = MailMessage(path = path, text = text)

                    self.assertEqual(self.classifier.classify(mail), expected_category)

    def test_spam_has_priority_over_urgent(self):
        mail = MailMessage(
            path = Path("mail.txt"),
            text = "Срочно подтвердите личность и введите логин и пароль",
        )

        self.assertEqual(self.classifier.classify(mail), "Спам")

    def test_normal_login_problem_is_not_spam(self):
        mail = MailMessage(
            path = Path("mail.txt"),
            text = "Логин и пароль правильные, но корпоративный портал недоступен",
        )

        self.assertEqual(self.classifier.classify(mail), "Критичные моменты")

if "__main__" == __name__:
    unittest.main()