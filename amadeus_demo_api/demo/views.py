import os
from amadeus import Client, ResponseError
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight


amadeus = Client(
    client_id=os.environ.get('API_KEY'),
    client_secret=os.environ.get('API_SECRET'),
    hostname='production'
)


def demo(request):
    origin = request.POST.get('Origin')
    destination = request.POST.get('Destination')
    departureDate = request.POST.get('Departuredate')
    returnDate = request.POST.get('Returndate')
    adults = request.POST.get('Adults')

    kwargs = {'origin': request.POST.get('Origin'), 'destination': request.POST.get('Destination'),
              'departureDate': request.POST.get('Departuredate')}
    if adults:
        kwargs['adults'] = adults
    tripPurpose = ''
    if returnDate:
        kwargs['returnDate'] = returnDate
        try:
            trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(originLocationCode=origin,
                                                                                destinationLocationCode=destination,
                                                                                departureDate=departureDate,
                                                                                returnDate=returnDate).data
            tripPurpose = trip_purpose_response['result']
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/demo_form.html', {})

    if origin and destination and departureDate:
        try:
            low_fare_flights = amadeus.shopping.flight_offers.get(**kwargs)
            prediction_flights = amadeus.shopping.flight_offers.prediction.post(low_fare_flights.result)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/demo_form.html', {})
        low_fare_flights_returned = []
        for flight in low_fare_flights.data:
            offer = Flight(flight).construct_flights()
            low_fare_flights_returned.append(offer)
        low_fare_flights_returned_by_price = sorted(low_fare_flights_returned, key=lambda k: k['price'])

        prediction_flights_returned = []
        for flight in prediction_flights.data:
            offer = Flight(flight).construct_flights()
            prediction_flights_returned.append(offer)

        return render(request, 'demo/results.html', {'response': low_fare_flights_returned_by_price,
                                                     'prediction': prediction_flights_returned,
                                                     'origin': origin,
                                                     'destination': destination,
                                                     'departureDate': departureDate,
                                                     'returnDate': returnDate,
                                                     'tripPurpose': tripPurpose,
                                                     })
    return render(request, 'demo/demo_form.html', {})
