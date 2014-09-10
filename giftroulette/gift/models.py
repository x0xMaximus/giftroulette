from django.db import models


class Gift(models.Model):
    WHATEVER = 0
    CUTE = 1
    TERRIFYING = 2
    FUN = 3
    SLUTTY = 4
    DUMB = 5
    TINY = 6
    SEASONAL = 7
    THEME_TYPE_CHOICE = (
        (WHATEVER, 'Whatever'),
        (CUTE, 'Cute'),
        (TERRIFYING, 'Terrifying'),
        (FUN, 'Fun'),
        (SLUTTY, 'Slutty'),
        (DUMB, 'Dumb'),
        (TINY, 'Tiny'),
        (SEASONAL, 'Seasonal')
    )
    theme = models.IntegerField(choices=THEME_TYPE_CHOICE, default=WHATEVER)

    BLACK = 0
    WHITE = 1
    YELLOW = 2
    BLUE = 3
    RED = 4
    COLOR_TYPE_CHOICES = (
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (YELLOW, 'Yellow'),
        (BLUE, 'Blue'),
        (RED, 'Red')
    )
    color = models.IntegerField(choices=COLOR_TYPE_CHOICES, default=BLACK)

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
    CURATOR_TYPE_CHOICES = (
        (HUMAN, 'Human'),
        (PARENT, 'Parent'),
        (ARTIST, 'Artist'),
        (BUSINESS, 'Business Man'),
        (STONER, 'Stoner'),
        (ROMANTIC, 'Romantic'),
        (KID, 'Kid'),
        (ELDERLY, 'Elder')
    )
    curator = models.IntegerField(choices=CURATOR_TYPE_CHOICES, default=HUMAN)


    NEW = 0
    PROCESSING = 1
    SHIPPED = 2
    STATUS_CHOICES = (
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)

    address = models.CharField(max_length=200)
    stripe_token = models.CharField(max_length=40)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[{status}] {theme} {color} {price} {curator}'.format(
                status=self.get_status_display(),
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
