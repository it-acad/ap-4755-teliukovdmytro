from django.db import models

class Author(models.Model):
    # 1. Реальні поля бази даних
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20, blank=True, null=True, default="")

    # 2. Магічні методи виведення даних
    def __str__(self):
        return f"'id': {self.id}, 'name': '{self.name}', 'surname': '{self.surname}', 'patronymic': '{self.patronymic}'"

    def __repr__(self):
        return f"Author(id={self.id})"

    # 3. Статичні методи пошуку, створення та видалення
    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return True
        except Author.DoesNotExist:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        if len(name) > 20 or len(surname) > 20 or (patronymic and len(patronymic) > 20):
            return None
        author = Author(name=name, surname=surname, patronymic=patronymic)
        author.save()
        return author

    # 4. Перетворення об'єкта у словник (для API/JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

    # 5. Метод оновлення даних автора
    def update(self, name=None, surname=None, patronymic=None):
        if name is not None:
            # Якщо ім'я занадто довге (наприклад, більше 20 чи 32 символів), ігноруємо оновлення
            if len(name) > 32 or len(name) < 2:
                return
            self.name = name
        if surname is not None:
            if len(surname) > 32 or len(surname) < 2:
                return
            self.surname = surname
        if patronymic is not None:
            if len(patronymic) > 32:
                return
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        return Author.objects.all()
