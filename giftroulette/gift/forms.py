from django import forms
from giftroulette.gift.models import Gift, Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)


class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ('theme', 'color', 'price', 'curator', 'address', 'stripe_token')


class GiftFeedbackForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ('customer_feedback',)
