from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden

from giftroulette.gift.models import Gift
from giftroulette.gift.forms import GiftForm, GiftFeedbackForm, ImageForm


def home(request):
    if request.method == 'POST':
        form = GiftForm(request.POST)
        if form.is_valid():
            gift = form.save()
            return redirect('giftroulette.gift.views.thankyou', gift.private_hash)
    else:
        form = GiftForm()

    return render_to_response('gift/home.jade',
            {'form': form, 'stripe_js_key': settings.STRIPE_JS_KEY},
                              context_instance=RequestContext(request))


def gift_read(request, gift_hash):
    gift = get_object_or_404(Gift, private_hash=gift_hash)

    if request.method == 'POST':
        form = GiftFeedbackForm(request.POST, instance=gift)
        if form.is_valid():
            gift = form.save()
            return redirect('giftroulette.gift.views.gift_read', gift.private_hash)
    else:
        form = GiftFeedbackForm(instance=gift)

    return render_to_response('gift/gift_read.jade',
                              {'gift': gift, 'form': form},
                              context_instance=RequestContext(request))


def upload(request, gift_hash):
    gift = get_object_or_404(Gift, private_hash=gift_hash)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.gift = gift
            model.save()
            request.session['image_id'] = model.id
            return HttpResponse('image upload success')
        return HttpResponseForbidden('allowed only via POST')


def thankyou(request, gift_hash):
    gift = get_object_or_404(Gift, private_hash=gift_hash)
    return render_to_response('gift/thankyou.jade',
                              {'gift': gift},
                              context_instance=RequestContext(request))

def email(request, gift_hash):
    gift = get_object_or_404(Gift, private_hash=gift_hash)
    message = """Email: {email}

Subject: How was your Gift Roulette Experience?

Body:

Hi!

Your gift recipient should have received {story} at {address} by now.

We spent a lot of time stalking online and figuring out a persona to take while selecting this gift. If you have time, please follow the unique link below to upload a some pictures of how the object has become part of the recipient's life for us to show off. Additionally, we'd love any feedback about the curation process from your point of view and what we can do in the future to make the experience better.

http://giftroulette.me/gift/{private_hash}/

Thank you for playing Gift Roulette!
    - The Gift Roulette team!

http://www.giftroulette.me
Ordering the craziest shit online just for you since 2014.""".format(email=gift.stripe_name, story=gift.get_description_text(), address=gift.address, private_hash=gift.private_hash)
    return HttpResponse(message, content_type="text/plain")
