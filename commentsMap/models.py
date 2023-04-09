from django.db import models
from django.urls import reverse

class Comment(models.Model):
    # bank = models.TextField(blank=True, verbose_name='Банк')
    # department = models.TextField(blank=True, verbose_name='Отделение')
    # content = models.TextField(blank=True,verbose_name='Контент')
    # author = models.CharField(max_length=255,verbose_name='Автор')
    # date_comm = models.CharField(max_length=255,verbose_name='Дата публикации')
    # stars = models.CharField(max_length=255,verbose_name='Оценка')
    # url = models.CharField(max_length=255,verbose_name='Ссылка на статью')
    # time_create = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    # time_update = models.DateTimeField(auto_now=True,verbose_name='Дата изменения')

    content = models.TextField(blank=True, verbose_name='Контент')
    author = models.CharField(blank=True, max_length=255, verbose_name='Автор')
    date_comm = models.CharField(blank=True, max_length=255, verbose_name='Дата публикации')
    stars = models.CharField(blank=True, max_length=255, verbose_name='Оценка')
    url = models.CharField(blank=True, max_length=255, verbose_name='Ссылка на статью')
    bank = models.TextField(blank=True, verbose_name='Банк')
    department = models.TextField(blank=True, verbose_name='Отделение')

    def __str__(self):
        return self.bank

    def get_absolute_url(self):
        return reverse('post',kwargs={'post_id':self.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id']
