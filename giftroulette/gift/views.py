from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from giftroulette.gift.models import Gift
from giftroulette.gift.forms import GiftForm


def home(request):
    if request.method == 'POST':
        form = GiftForm(request.POST)
        if form.is_valid():
            gift = form.save()
            return redirect('giftroulette.gift.views.thankyou', gift.pk)
    else:
        form = GiftForm()

    return render_to_response('gift/home.jade',
            {'form': form, 'stripe_js_key': settings.STRIPE_JS_KEY},
                              context_instance=RequestContext(request))


def thankyou(request, gift_id):
    gift = get_object_or_404(Gift, pk=gift_id)
    return render_to_response('gift/thankyou.jade',
                              {'gift': gift},
                              context_instance=RequestContext(request))
