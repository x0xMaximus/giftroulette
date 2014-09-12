from django.test import TestCase
from django.test.client import Client as WebClient

from giftroulette.gift.models import Gift

import random
import os


class GiftTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.client = WebClient()

    def testFormSubmission(self):
        test_iterations = 100
        self.assertEquals(Gift.objects.count(), 0)

        for i in range(test_iterations):
            fake_payment_token = os.urandom(15).encode('hex')
            payload = {'theme': random.choice(Gift.THEME_CHOICES)[0],
                        'color': random.choice(Gift.COLOR_CHOICES)[0],
                        'price': random.choice(Gift.PRICE_CHOICES)[0],
                        'curator': random.choice(Gift.CURATOR_CHOICES)[0],
                        'address': '123 foo st San Diego, CA 92101',
                        'stripe_token': fake_payment_token}
            r = self.client.post('/', payload)
            self.assertEquals(r.status_code, 302)

        self.assertEquals(Gift.objects.count(), test_iterations)
