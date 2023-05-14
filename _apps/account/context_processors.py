from _apps.vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Exception:
        vendor = None

    print(vendor)

    return dict(vendor=vendor)


def get_vendor_instance(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Exception:
        vendor = None

    return vendor
