from django.db import models

import os


def _createHash():
    return os.urandom(10).encode('hex')


def _content_file_name(instance, filename):
    name = _createHash() + os.path.splitext(filename)[1]
    return '/'.join(['images', name])


class Gift(models.Model):
    private_hash = models.CharField(max_length=20, default=_createHash, unique=True)

    WHATEVER = 0
    CUTE = 1
    TERRIFYING = 2
    FUN = 3
    SLUTTY = 4
    DUMB = 5
    TINY = 6
    SEASONAL = 7
    THEME_CHOICES = (
        (WHATEVER, 'Whatever'),
        (CUTE, 'Cute'),
        (TERRIFYING, 'Terrifying'),
        (FUN, 'Fun'),
        (SLUTTY, 'Slutty'),
        (DUMB, 'Dumb'),
        (TINY, 'Tiny'),
        (SEASONAL, 'Seasonal')
    )
    theme = models.IntegerField(choices=THEME_CHOICES, default=WHATEVER)

    BLACK = 0
    WHITE = 1
    YELLOW = 2
    BLUE = 3
    RED = 4
    COLOR_CHOICES = (
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (YELLOW, 'Yellow'),
        (BLUE, 'Blue'),
        (RED, 'Red')
    )
    color = models.IntegerField(choices=COLOR_CHOICES, default=BLACK)

    TWENTY = 0
    FIFTY = 1
    HUNDRED = 2
    TWO_HUNDRED = 3
    PRICE_CHOICES = (
        (TWENTY, '$20'),
        (FIFTY, '$50'),
        (HUNDRED, '$100'),
        (TWO_HUNDRED, '$200')
    )
    price = models.IntegerField(choices=PRICE_CHOICES, default=TWENTY)

    HUMAN = 0
    PARENT = 1
    ARTIST = 2
    BUSINESS = 3
    STONER = 4
    ROMANTIC = 5
    KID = 6
    ELDERLY = 7
    CURATOR_CHOICES = (
        (HUMAN, 'Human'),
        (PARENT, 'Parent'),
        (ARTIST, 'Artist'),
        (BUSINESS, 'Business Man'),
        (STONER, 'Stoner'),
        (ROMANTIC, 'Romantic'),
        (KID, 'Kid'),
        (ELDERLY, 'Elder')
    )
    curator = models.IntegerField(choices=CURATOR_CHOICES, default=HUMAN)

    NEW = 0
    PROCESSING = 1
    SHIPPED = 2
    STATUS_CHOICES = (
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)
    asin = models.CharField(max_length=10, blank=True)

    address = models.CharField(max_length=200)

    stripe_token = models.CharField(max_length=40)
    stripe_id = models.CharField(max_length=40, blank=True)
    stripe_name = models.CharField(max_length=200, blank=True)

    customer_feedback = models.TextField(blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[{status}] {theme} {color} {price} {curator}'.format(
            status=self.get_status_display(),
            theme=self.get_theme_display(),
            color=self.get_color_display(),
            price=self.get_price_display(),
            curator=self.get_curator_display())

    def get_story_text(self):
        return u"I just bought something {theme}, that's {color}, costs about {price} and chosen by a {curator}".format(
            theme=self.get_theme_display(),
            color=self.get_color_display(),
            price=self.get_price_display(),
            curator=self.get_curator_display())

    def get_description_text(self):
        return u"something {theme}, that's {color}, costs about {price} and chosen by a {curator}".format(
            theme=self.get_theme_display(),
            color=self.get_color_display(),
            price=self.get_price_display(),
            curator=self.get_curator_display())


    def get_amount_cents(self):
        if self.price == 0:
            return 2000

        if self.price == 1:
            return 5000

        if self.price == 2:
            return 10000

        if self.price == 3:
            return 20000


class Image(models.Model):
    image = models.ImageField(upload_to = _content_file_name, default = 'images/logo.jpg')
    gift = models.ForeignKey(Gift, null=True, blank=True, default = None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'#{image_id} for {gift}'.format(image_id=self.id, gift=self.gift)
