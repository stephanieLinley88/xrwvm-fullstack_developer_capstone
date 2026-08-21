from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {
            "userName": username,
            "status": "Authenticated"
        }

    return JsonResponse(data)


def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        User.objects.get(username=username)
        username_exists = True
    except User.DoesNotExist:
        username_exists = False

    if not username_exists:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated"
        }
    else:
        data = {
            "userName": username,
            "error": "Already Registered"
        }

    return JsonResponse(data)
