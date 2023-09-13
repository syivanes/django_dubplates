from django.db import models
from multiselectfield import MultiSelectField

highlighted = models.TextField()

class Track(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    download_url = models.TextField()
    stripe_price_id = models.CharField(max_length=120, blank=True, default='')
    track_user_relationships = models.ManyToManyField(
        'auth.User',
        through='UserTrackRelationship',
        through_fields=('track', 'user'),
    )

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        super(Track, self).save(*args, **kwargs)


class UserTrackRelationship(models.Model):
    REALTIONSHIP_CHOICES = (('user_owns_track', 'This User Owns This Track'),
                            ('user_watching_track', 'This User Is Watching This Track'),
                            ('user_purchased_copy', 'This User Has Purchased a Copy of This Track'))

    user = models.ForeignKey('auth.User', related_name='usertrackrel_user', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name='usertrackrel_track', on_delete=models.CASCADE)
    relationship_type = MultiSelectField(choices=REALTIONSHIP_CHOICES, max_choices=1, max_length=19)
    stripe_transaction_id = models.CharField(max_length=50, blank=True, default='')

    def save(self, *args, **kwargs):
        super(UserTrackRelationship, self).save(*args, **kwargs)