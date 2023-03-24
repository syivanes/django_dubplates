from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

owner = models.ForeignKey('auth.User', related_name='django_dubplates', on_delete=models.CASCADE)
highlighted = models.TextField()

class Track(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    url = models.TextField()

    class Meta:
        ordering = ['created']