def detect_user(user):
    redirect_url = "home"
    if user.role == 1:
        redirect_url = "accounts_vendor_dashboard"
    elif user.role == 2:
        redirect_url = "accounts_customer_dashboard"
    elif user.is_superuser:
        redirect_url = "admin"

    return redirect_url
