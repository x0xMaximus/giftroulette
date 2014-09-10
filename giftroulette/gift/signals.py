from django.dispatch import receiver
from django.db.models.signals import post_save
from giftroulette.gift.models import Gift
from django.conf import settings
from django.core.mail import send_mail

import stripe

@receiver(post_save, sender=Gift)
def provider_post_save(sender, instance, **kwargs):
    gift = instance

    if gift.stripe_token is not '[used]':
        stripe.api_key = settings.STRIPE_API_KEY
        try:
            charge = stripe.Charge.create(
                amount = gift.get_amount_cents(),
                currency = 'usd',
                card = gift.stripe_token,
                description = 'Gift Roulette'
            )
            gift.stripe_token = '[used]'
            gift.save()

            send_mail('[Gift Roulette] New Order!', '{gift} :: ${price}'.format(gift=gift, price=gift.get_price_display()), settings.SERVER_EMAIL, [email[1] for email in settings.MANAGERS])

        except stripe.CardError, e:
            pass

