from django.contrib import admin
from django.db import models

from giftroulette.gift.models import Gift, Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'gift', 'created_at')
    mymodel = models.ForeignKey(Image)


class GiftAdmin(admin.ModelAdmin):
    list_display = ('private_hash', 'status', 'theme',
                    'color', 'price' , 'curator',
                    'created', 'stripe_name', 'address',
                    'asin', 'customer_feedback', 'updated')

    readonly_fields = ( 'private_hash', 'theme', 'color',
                        'price', 'curator', 'stripe_token',
                        'stripe_id', 'stripe_name', 'customer_feedback')

    search_fields = ['private_hash', 'stripe_name', 'address',
                    'asin', 'customer_feedback']
    list_filter = ['status', 'theme', 'color',
                   'price', 'curator']

    mymodel = models.ForeignKey(Gift)


admin.site.register(Image, ImageAdmin)
admin.site.register(Gift, GiftAdmin)
