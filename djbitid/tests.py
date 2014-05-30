import pytz

from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from pybitid import bitid

from views import BitIdView
from models import Nonce
from backends import BitIdBackend

class BitIdChallengeTestCase(TestCase):
    """
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('djbitid_challenge')
        self.test_callback = 'https://example.com%s' % reverse('djbitid_callback')
        self.test_bituri = 'bitid://example.com%s?x=' % reverse('djbitid_callback')

    def test_get_challenge(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

        self.assertContains(response, self.test_callback)
        self.assertContains(response, self.test_bituri)


class BitIdCallbackTestCase(TestCase):
    """
    """

    TEST_ADDRESS = '1LdaaCXRebCx5VgrdFESNkHqWxWuVSVq9R'

    def setUp(self):
        self.client = Client()
        self.url = reverse('djbitid_callback')
        self.bid_uri = 'https://%s%s' % (BitIdView.DEFAULT_HOSTNAME, self.url)

    def test_bad_credentials(self):
        response = self.client.post(self.url, {
            'uri': '',
            'signature': '',
            'address': 'badaddress',
        })
        self.assertEquals(response.status_code, 401)


class BitIdBackendTestCase(TestCase):

    TEST_ADDRESS = '1LdaaCXRebCx5VgrdFESNkHqWxWuVSVq9R'

    def setUp(self):
        self.backend = BitIdBackend()

    def test_no_params(self):
        result = self.backend.authenticate()
        self.assertIsNone(result)

    def test_bad_address(self):
        result = self.backend.authenticate(
            bitid_uri='',
            callback_uri='',
            signature='',
            address='badaddress')

        self.assertIsNone(result)
        
    def test_bad_uri(self):
        result = self.backend.authenticate(
            bitid_uri='bad',
            callback_uri='',
            signature='bad',
            address=self.TEST_ADDRESS)

        self.assertIsNone(result)

    # TODO
    def _test_bad_signature(self):
        challenge = self._get_challenge()

        result = self.backend.authenticate(
            bitid_uri=challenge['bitid_uri'],
            callback_uri=challenge['callback_uri'],
            signature='bad',
            address=self.TEST_ADDRESS)

        self.assertIsNone(result)
            
    def test_bad_nonce(self):
        challenge = self._get_challenge()

        result = self.backend.authenticate(
            bitid_uri=challenge['bitid_uri'] + 'badnonce',
            callback_uri=challenge['callback_uri'],
            signature=self._get_signature(challenge['bitid_uri']),
            address=self.TEST_ADDRESS)

        self.assertIsNone(result)

    def test_expired_nonce(self):
        challenge = self._get_challenge()

        # expire nonce
        nid = bitid.extract_nonce(challenge['bitid_uri'])
        nonce = Nonce.objects.get(nid=nid)
        nonce.created = datetime(1900, 1, 1).replace(tzinfo = pytz.utc)
        nonce.save()

        result = self.backend.authenticate(
            bitid_uri=challenge['bitid_uri'],
            callback_uri=challenge['callback_uri'],
            signature=self._get_signature(challenge['bitid_uri']),
            address=self.TEST_ADDRESS)

        self.assertIsNone(result)

    def test_no_user(self):
        challenge = self._get_challenge()

        result = self.backend.authenticate(
            bitid_uri=challenge['bitid_uri'],
            callback_uri=challenge['callback_uri'],
            signature=self._get_signature(challenge['bitid_uri']),
            address=self.TEST_ADDRESS)

        self.assertTrue(hasattr(result, 'username'))
        self.assertEquals(result.username, self.TEST_ADDRESS)

    def test_nonce_model(self):
        challenge = self._get_challenge()
        n = Nonce.objects.latest()
        self.assertEquals(n.nid, n.__unicode__())

    def _get_challenge(self):
        response = self.client.get(reverse('djbitid_challenge'))
        return response.context

    def _get_signature(self, bitid_uri):
        return 'HGaGJuPjuw9n6KqI0ulOqMFGfwIvW4bGjNG7Ra9xNLqQNlUtTvJEx+QmszUGkhkiLZDCC2r5CSKbx6vkBGdM6R0='
