from _apps.vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except TypeError:
        vendor = None

    return dict(vendor=vendor)