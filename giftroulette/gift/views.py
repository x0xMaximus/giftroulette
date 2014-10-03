from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail

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
            # If they give feedback let us know
            if gift.customer_feedback:
                send_mail('[Gift Roulette] New Feedback!',
                          '{comment} // {gift}'.format(comment=gift.customer_feedback, gift=gift),
                          settings.SERVER_EMAIL,
                          [email[1] for email in settings.MANAGERS])

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
