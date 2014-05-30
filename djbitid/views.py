import uuid

from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.urlresolvers import reverse
from django import http
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS

from pybitid import bitid

from models import Nonce
from forms import BitIdForm

class BitIdView(View):
    DEFAULT_HOSTNAME = 'example.com'

    def get_callback_uri(self, request):
        hostname = request.META.get('HTTP_HOST', self.DEFAULT_HOSTNAME)

        return 'https://%s%s' % (hostname, reverse('djbitid_callback'))
    

class BitIdChallenge(BitIdView):
    template_name = 'djbitid/challenge.html'

    def get(self, request):
        """
        This function initializes the authentication process 
        It builds a challenge which is sent to the client
        """

        # Creates a new nonce associated to this session
        nonce = Nonce()
        nonce.save()

        # Gets the callback uri
        callback_uri = self.get_callback_uri(request)

        # Builds the challenge (bitid uri) 
        bitid_uri = bitid.build_uri(callback_uri, nonce.nid)

        # Gets the qrcode uri
        qrcode = bitid.qrcode(bitid_uri)

        context = {
            "callback_uri": callback_uri,
            "bitid_uri": bitid_uri,
            "qrcode": qrcode
        }

        return render(request, self.template_name, context)


class BitIdCallback(BitIdView):
    template_name = 'djbitid/callback.html'

    def get(self, request):
        form = BitIdForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        This function validates the response sent by the client about the challenge
        This is the route called by the bitcoin wallet when the challenge has been signed
        """

        # Retrieves the callback uri
        callback_uri = self.get_callback_uri(request)
        
        # Extracts data from the posted request
        bitid_uri = request.POST.get("uri")
        signature = request.POST.get("signature")
        address   = request.POST.get("address")
        errors = []

        user = authenticate(bitid_uri=bitid_uri, callback_uri=callback_uri,
                            signature=signature, address=address, errors=errors)

        if user is not None:
            login(request, user)
            return render(request, self.template_name, {'user': user })
        else:
            form = BitIdForm(request.POST)
            form.full_clean()
            for error in errors:
                form._errors[NON_FIELD_ERRORS] = form.error_class([error])
            return render(request, self.template_name, {'form': form })
