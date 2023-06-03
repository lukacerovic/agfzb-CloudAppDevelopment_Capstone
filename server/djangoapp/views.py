from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'djangoapp/index.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # Handle invalid login credentials
            return render(request, 'djangoapp/login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'djangoapp/login.html')
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def signup(request):
    if request.method == 'POST':
        # Get the form data from the request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']

        # Create a new user object
        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name)

        # Log in the user
        login(request, user)

        # Redirect to the home page or any other page
        return redirect('djangoapp:index')

    # If the request method is GET, render the signup form template
    return render(request, 'djangoapp/registration.html')

# ...

def get_dealerships(request):
    if request.method == "GET":
        url = "your-cloud-function-domain/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    reviews = get_dealer_reviews_from_cf(dealer_id)

    context = {'reviews': reviews}
    return render(request, 'dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
@login_required
def add_review(request, dealer_id):
    class AddReviewForm(forms.Form):
        review = forms.CharField(widget=forms.Textarea)
        purchase = forms.BooleanField(required=False)
        
    if request.method == 'POST':
        # Create the review dictionary
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.user.username
        review["dealership"] = dealer_id
        review["review"] = request.POST.get('review_text', '')
        review["purchase"] = request.POST.get('purchase', False)

        # Create the JSON payload
        json_payload = {"review": review}

        # Call the post_request method
        url = "your_review_post_url"
        response = post_request(url, json_payload, dealerId=dealer_id)

        # Process the response
        if response.status_code == 200:
            # Review was successfully added
            return HttpResponse("Review added successfully!")
        else:
            # Failed to add review
            return HttpResponse("Failed to add review!")

    else:
        # Handle GET request
        # Render the form for adding a review
        return render(request, 'add_review.html')




