from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author} from {self.date}'

    @classmethod
    def get_30_messages(cls):
        return cls.objects.order_by('-date').all()[:30]


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    
    def __str__(self) -> str:
        return self.name

class Office(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='office_of_city')
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Офис'
        verbose_name_plural = 'Офисы' 