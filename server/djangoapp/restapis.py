import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
     if api_key:
   # Basic authentication GET
        request.get(url, params=params, auth=, ...)
    else:
        # no authentication GET
        request.get(url, params=params)
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data                      auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
#

def get_dealer_reviews_from_cf(url, dealer_id):
    reviews = get_request(url, dealerId=dealer_id)
    dealer_reviews = []

    for review in reviews:
        review_obj = DealerReview(
            dealership=review['dealership'],
            name=review['name'],
            purchase=review['purchase'],
            review=review['review'],
            purchase_date=review['purchase_date'],
            car_make=review['car_make'],
            car_model=review['car_model'],
            car_year=review['car_year'],
            sentiment=None,  # Initialize sentiment as None
            id=review['id']
        )
        
        # Assign sentiment using the analyze_review_sentiments method
        review_obj.sentiment = analyze_review_sentiments(review_obj.review)

        dealer_reviews.append(review_obj)

    return dealer_reviews


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/<instance_id>/v1/analyze"

    # Set the parameters for the NLU API call
    params = {
        "text": dealerreview.review,  # Use the review text for sentiment analysis
        "version": "<version>",  # Specify the version of the NLU API
        "features": "sentiment",  # Request sentiment analysis feature
        "return_analyzed_text": True  # Request analyzed text to be returned
    }

    # Make the API call to analyze sentiment
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', '<api_key>'))

    # Process the response and extract the sentiment
    if response.status_code == 200:
        sentiment = response.json().get("sentiment").get("document").get("label")
        dealerreview.sentiment = sentiment
    else:
        # Handle error cases if the API call fails
        print("Error: Sentiment analysis request failed.")

    return dealerreview



