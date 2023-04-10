from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

highlighted = models.TextField()

class Track(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    download_url = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='tracks_author', on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        super(Track, self).save(*args, **kwargs)

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length = 254, blank=False)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        print(args)
        print('*************')
        print(kwargs)
        # super(User, self).save(*args, **kwargs)