import pytz

from datetime import datetime

from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

from pybitid import bitid


class Nonce(models.Model):
    """
    """

    DEFAULT_EXPIRATION_DELAY = 600

    sid = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, related_name='nonces')
    nid = models.CharField(max_length=256)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created'

    def save(self, *args, **kwargs):

        if self.pk is None:
            self.nid = bitid.generate_nonce()

        super(Nonce, self).save(*args, **kwargs)


    def has_expired(self):
        '''
        Checks if nonce has expired
        '''
        delta = datetime.now().replace(tzinfo = pytz.utc) - self.created
        delay = getattr(settings, 'BITID_CHALLENGE_EXPIRATION_DELAY', 
                        self.DEFAULT_EXPIRATION_DELAY)
        return delta.total_seconds() > delay


    def __unicode__(self):
        return self.nid
