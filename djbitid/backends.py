from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django.contrib.auth.models import User

from pybitid import bitid

from models import Nonce


class BitIdBackend(object):

    USE_TESTNET_DEFAULT = False

    def authenticate(self, bitid_uri=None, callback_uri=None, 
                     signature=None, address=None, errors=[]):
        if bitid_uri is None or callback_uri is None or signature is None or address is None:
            errors.append('Invalid parameters')
            return None

        #
        # Let's start by a bunch of validations
        #

        use_testnet = getattr(settings, 'BITID_USE_TESTNET', self.USE_TESTNET_DEFAULT)
    
        # Checks the address
        if not bitid.address_valid(address, use_testnet):
            errors.append("Address is invalid or not legal")
            return None
        # Checks the bitid uri
        if not bitid.uri_valid(bitid_uri, callback_uri):
            errors.append("BitID URI is invalid or not legal")
            return None
        # Checks the signature
        if not bitid.signature_valid(address, signature, 
                                     bitid_uri, callback_uri,
                                     use_testnet):
            errors.append("Signature is incorrect")
            return None

        # Checks the nonce
        nid = bitid.extract_nonce(bitid_uri)
        # Tries to retrieve the nonce from db
        try:
            nonce = Nonce.objects.get(nid=nid)
        except ObjectDoesNotExist:
            errors.append("NONCE is illegal")
            return None

        if nonce.has_expired():
            nonce.delete()
            errors.append("NONCE has expired")
            return None
        
        #
        # So good so far, everything seems ok
        # It's time to check if we have a sign out or a sign in
        #


        # Checks if a user with the given address has already been registered in db (sign in)
        try:
            user = User.objects.get(username=address)
        except ObjectDoesNotExist:
            # Here, we have an important check to do in order to avoid flooding of the users db
            # Let's check for a proof of goodwill (@see pybitid_demo.services.fake_tx_db_service)
            if not self.goodwill_check(address):
                errors.append("Address is invalid or not legal")
                return None
            # Creates a new user and stores it in db
            user = User.objects.create_user(username=address)
            user.save()

        # To finalize the authentication, let's set the user id in the nonce and update it in db
        nonce.user = user
        nonce.save()

        return user

    def goodwill_check(self, address):
        """
        TODO Check to prevent flooding
        """

        return True

