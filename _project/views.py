import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)
logapp = logging.getLogger("app")


def home(request):
    logapp.debug("This is a debug message")
    logapp.info("This is an info message")
    logapp.warning("This is a warning message")
    logapp.error("This is an error message")
    logapp.critical("This is a critical message")
    return render(request, "home.html")
