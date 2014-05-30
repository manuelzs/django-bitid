from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from djbitid.views import BitIdChallenge, BitIdCallback

urlpatterns = patterns('djbitid',

                       url('^challenge/$',
                           BitIdChallenge.as_view(),
                           name='djbitid_challenge'),

                       url('^callback/$',
                           csrf_exempt(BitIdCallback.as_view()),
                           name='djbitid_callback'),
)
