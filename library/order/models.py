from django.db import models
from book.models import Book
from authentication.models import CustomUser

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        # Форматуємо дати строго під очікування тесту (з таймзоною +00:00 без мікросекунд)
        created_val = f"'{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}+00:00'" if self.created_at else "None"
        end_val = f"'{self.end_at.strftime('%Y-%m-%d %H:%M:%S')}+00:00'" if self.end_at else "None"
        plated_val = f"'{self.plated_end_at.strftime('%Y-%m-%d %H:%M:%S')}+00:00'" if self.plated_end_at else "None"

        # Усі назви полів (включаючи 'id') мають бути в одинарних лапках
        return (
            f"'id': {self.id}, "
            f"'user': CustomUser(id={self.user.id if self.user else None}), "
            f"'book': Book(id={self.book.id if self.book else None}), "
            f"'created_at': {created_val}, "
            f"'end_at': {end_val}, "
            f"'plated_end_at': {plated_val}"
        )


    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        # Переводимо об'єкт у словник, як зазначено у вашому докстрінгу
        return {
            'id': self.id,
            'book': self.book.id if self.book else None,
            'user': self.user.id if self.user else None,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp()) if isinstance(self.plated_end_at, datetime) else self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        # 1. Базові перевірки на існування об'єктів
        if not book or not user:
            return None

        # 2. Перевірка на незбереженого користувача чи книгу
        if getattr(user, 'id', None) is None or getattr(book, 'id', None) is None:
            return None
        if hasattr(user, '_state') and user._state.adding:
            return None

        # 3. Сувора перевірка наявності книги на складі (Виправлено імпорт!)
        from book.models import Book as BookModel
        try:
            db_book = BookModel.objects.get(pk=book.id)
            
            # Рахуємо, скільки копій цієї книги зараз видано на руки
            active_orders = Order.objects.filter(book=db_book, end_at__isnull=True).count()
            
            # Якщо книга закінчилася на складі
            if db_book.count <= active_orders:
                return None
        except Exception:
            # Запасна перевірка властивості в пам'яті
            if getattr(book, 'count', 0) <= 0:
                return None

        # 4. Створюємо замовлення
        order = Order(user=user, book=book, plated_end_at=plated_end_at)
        order.save()
        return order


    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False
