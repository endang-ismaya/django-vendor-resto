# import logging
from django.shortcuts import render

from _apps.vendor.models import Vendor

# logger = logging.getLogger(__name__)
# logapp = logging.getLogger("app")


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {"vendors": vendors}
    return render(request, "home.html", context)
