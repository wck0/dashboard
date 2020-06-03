import datetime
from vita.models import Menu_item, Home_page
from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from siteconfig.models import HeroImage

import logging
logger = logging.getLogger(__name__)

def Index(request):
    menu = Menu_item.objects.order_by('order')
    home = Home_page.objects.order_by('-publish_date')[0]
    try:
        hero = HeroImage.objects.get(app='default')
    except:
        hero = None
    return render(request, 'base.html', {'pagename':'Welcome',
              'hero': hero,
              'menu': menu,
              'home': home,
        } 
    )
