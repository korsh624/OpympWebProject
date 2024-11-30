from django.db import models


class Order(models.Model):
    title = models.CharField(max_length=128)
    customer_name = models.CharField(max_length=128)
    technical_task_short = models.TextField()
    technical_task_full = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    budget = models.PositiveIntegerField(default=0)
    deadline = models.TimeField()

    def __str__(self):
        return f'Заказ {self.title}'
    
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class Comment(models.Model):
    customer_name = models.CharField(max_length=128)
    comment = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.customer_name}'
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'