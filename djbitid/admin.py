from django.contrib import admin
from models import Nonce


class NonceAdmin(admin.ModelAdmin):
    """
    """

    model = Nonce


admin.site.register(Nonce, NonceAdmin)
