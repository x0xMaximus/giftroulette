from django import forms
from giftroulette.gift.models import Gift


class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ('theme', 'color', 'price', 'curator', 'address', 'stripe_token')
