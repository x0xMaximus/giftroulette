from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import send_mail

from giftroulette.gift.models import Gift

import stripe
import sys


@receiver(post_save, sender=Gift)
def provider_post_save(sender, instance, **kwargs):
    gift = instance

    if 'test' not in sys.argv:

        if gift.stripe_token is not '[used]':
            stripe.api_key = settings.STRIPE_API_KEY
            try:
                stripe.Charge.create(
                    amount=gift.get_amount_cents(),
                    currency='usd',
                    card=gift.stripe_token,
                    description='Gift Roulette'
                )
                gift.stripe_token = '[used]'
                gift.save()

                send_mail('[Gift Roulette] New Order!',
                        '{gift}'.format(gift=gift),
                        settings.SERVER_EMAIL,
                        [email[1] for email in settings.MANAGERS])

            except stripe.CardError:
                pass
