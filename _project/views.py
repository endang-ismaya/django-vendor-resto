import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)
logger_info = logging.getLogger("app")


def home(request):
    logger_info.info("Homepage was accessed")
    return render(request, "home.html")
