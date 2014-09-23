from django.test import TestCase, LiveServerTestCase
from django.test.client import Client as WebClient

from selenium.webdriver.firefox.webdriver import WebDriver

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


class FunctionalCardTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(FunctionalCardTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(FunctionalCardTests, cls).tearDownClass()

    def test_login(self):
        self.selenium.get(self.live_server_url)

        address_input = self.selenium.find_element_by_id('id_address')
        address_input.send_keys('123 Sunnyvale Drive, Happy City, CA 92101')

        giftroulette_button = self.selenium.find_element_by_id('id_submit_gift')
        giftroulette_button.click()

        # self.selenium.switchTo().frame('stripe_checkout_app')
        # stripe_email = self.selenium.find_element_by_id('email')
        # stripe_email.send_keys('john.doe@gmail.com')
        # stripe_card_number = self.selenium.find_element_by_id('card_number')
        # stripe_card_number.send_keys('4242 4242 4242 4242')
        # self.selenium.switchTo().defaultContent()
