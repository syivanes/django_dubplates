from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from multiselectfield import MultiSelectField

highlighted = models.TextField()

class Track(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    download_url = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='track_author', on_delete=models.CASCADE, default=1)

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
        print('calling save() in models.py')
        super(User, self).save(*args, **kwargs)

class UserTrackRelationship(models.Model):
    REALTIONSHIP_CHOICES = (('user_owns_track', 'This User Owns This Track'),
                            ('user_watching_track', 'This User Is Watching This Track'),
                            ('user_purchased_copy', 'This User Has Purchased a Copy of This Track'))

    user = models.ForeignKey(User, related_name='usertrackrel_user', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name='usertrackrel_track', on_delete=models.CASCADE)
    relationship_type = MultiSelectField(choices=REALTIONSHIP_CHOICES, max_choices=1)

    def save(self, *args, **kwargs):
        print(self)
        super(Watchlist, self).save(*args, **kwargs)