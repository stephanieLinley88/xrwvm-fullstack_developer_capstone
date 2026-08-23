from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path
import json


# ---------------------------------------------------------
# Local dealership data
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DEALERS_FILE = BASE_DIR / "database" / "data" / "dealerships.json"


def load_dealers():
    with open(DEALERS_FILE, "r") as file:
        return json.load(file)["dealerships"]


# Keep a sample review so the dealer-details screenshot has
# something visible immediately.
reviews_store = [
    {
        "id": 1,
        "dealership": 5,
        "name": "Course Reviewer",
        "review": "Excellent dealership. Highly recommended.",
        "purchase": True,
        "purchase_date": "2023-01-12",
        "car_make": "NISSAN",
        "car_model": "XTRAIL",
        "car_year": "2023",
        "sentiment": "positive",
    }
]


# ---------------------------------------------------------
# Login / logout / registration
# ---------------------------------------------------------

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)

    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)

    response = {"userName": username}

    if user is not None:
        login(request, user)
        response = {
            "userName": username,
            "status": "Authenticated",
            "firstName": user.first_name,
            "lastName": user.last_name,
        }

    return JsonResponse(response)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "userName": username,
            "error": "Already Registered"
        })

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )

    login(request, user)

    return JsonResponse({
        "userName": username,
        "status": "Authenticated",
        "firstName": first_name,
        "lastName": last_name,
    })


# ---------------------------------------------------------
# Dealers
# ---------------------------------------------------------

def get_dealerships(request, state=None):
    dealers = load_dealers()

    if state and state != "All":
        dealers = [
            dealer for dealer in dealers
            if dealer["state"] == state
        ]

    return JsonResponse({
        "status": 200,
        "dealers": dealers
    })


def get_dealer_details(request, dealer_id):
    dealers = load_dealers()

    dealer = [
        item for item in dealers
        if item["id"] == int(dealer_id)
    ]

    return JsonResponse({
        "status": 200,
        "dealer": dealer
    })


def get_dealer_reviews(request, dealer_id):
    dealer_reviews = [
        review for review in reviews_store
        if int(review["dealership"]) == int(dealer_id)
    ]

    return JsonResponse({
        "status": 200,
        "reviews": dealer_reviews
    })


# ---------------------------------------------------------
# Review submission
# ---------------------------------------------------------

@csrf_exempt
def add_review(request):
    data = json.loads(request.body)

    text = data.get("review", "").lower()

    negative_words = ["bad", "poor", "terrible", "awful", "worst"]
    positive_words = [
        "good", "great", "excellent", "fantastic",
        "amazing", "recommend", "happy"
    ]

    if any(word in text for word in negative_words):
        sentiment = "negative"
    elif any(word in text for word in positive_words):
        sentiment = "positive"
    else:
        sentiment = "neutral"

    data["id"] = len(reviews_store) + 1
    data["dealership"] = int(data["dealership"])
    data["sentiment"] = sentiment

    reviews_store.append(data)

    return JsonResponse({
        "status": 200,
        "review": data
    })


# ---------------------------------------------------------
# Cars for review dropdown
# ---------------------------------------------------------

def get_cars(request):
    cars = [
        {"CarMake": "NISSAN", "CarModel": "XTRAIL"},
        {"CarMake": "Toyota", "CarModel": "Camry"},
        {"CarMake": "Audi", "CarModel": "A4"},
        {"CarMake": "Mercedes", "CarModel": "C-Class"},
    ]

    return JsonResponse({
        "CarModels": cars
    })
