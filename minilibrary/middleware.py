import time
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


BLOCKED_IPS = []
EXCEPT_URLS = ['/login/', '/admin/', '/welcome/', '/register/', '/hello/']


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()

        response = self.get_response(request)
        duration = time.time() - start
        print(f"Request to {request.path} took {duration:.2f} seconds.")
        return response


class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        print(f"Request from IP: {ip}")

        if ip in BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is blocked.")

        return self.get_response(request)


class OfficeHoursMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = time.localtime().tm_hour
        print(f"Current hour: {current_hour}")
        if 9 <= current_hour < 18:
            return self.get_response(request)
        else:
            return HttpResponseForbidden(
                "This site is only accessible during "
                "office hours (9 AM - 6 PM)."
            )


class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.user.is_authenticated
            and not any(
                request.path.startswith(url) for url in EXCEPT_URLS
            )
        ):
            print(
                f"Unauthenticated access attempt to {request.path}. "
                "Redirecting to login."
            )
            return redirect('/admin/')

        return self.get_response(request)
