from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_requests = dict()

    @staticmethod
    def get_user_ip(request: HttpRequest):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            ip = forwarded_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        return ip

    def __call__(self, request: HttpRequest):
        user_ip = self.get_user_ip(request)
        time_delay = 1  # in seconds

        if user_ip in self.user_requests:
            if (datetime.now().timestamp() - self.user_requests[user_ip]) < time_delay:
                return render(request, 'requestdataapp/access-denied.html')

        self.user_requests[user_ip] = datetime.now().timestamp()
        response = self.get_response(request)

        return response
