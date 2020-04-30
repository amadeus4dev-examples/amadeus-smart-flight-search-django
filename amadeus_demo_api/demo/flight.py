import re
from datetime import datetime


class Flight:
    def __init__(self, flight):
        self.flight = flight

    def construct_flights(self):
        offer = {}
        index = 0
        offer['price'] = self.flight['price']['total']
        offer['id'] = self.flight['id']
        if 'choiceProbability' in self.flight:
            offer['probability'] = get_probability(self.flight['choiceProbability'])

        for f in self.flight['itineraries']:
            # Keys starting from 0 correspond to Outbound flights and the keys starting from 1 to Return flights
            if len(self.flight['itineraries'][index]['segments']) == 2:  # one stop flight
                offer[f'{index}firstFlightDepartureAirport'] = self.flight['itineraries'][index]['segments'][0]['departure']['iataCode']
                offer[f'{index}firstFlightAirlineLogo'] = get_airline_logo(self.flight['itineraries'][index]['segments'][0]['carrierCode'])
                offer[f'{index}firstFlightAirline'] = self.flight['itineraries'][index]['segments'][0]['carrierCode']
                offer[f'{index}firstFlightDepartureDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['departure']['at'])
                offer[f'{index}firstFlightArrivalAirport'] = self.flight['itineraries'][index]['segments'][0]['arrival']['iataCode']
                offer[f'{index}firstFlightArrivalDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['arrival']['at'])
                offer[f'{index}firstFlightArrivalDuration'] = self.flight['itineraries'][index]['segments'][0]['duration']
                offer[f'{index}secondFlightDepartureAirport'] = self.flight['itineraries'][index]['segments'][1]['departure']['iataCode']
                offer[f'{index}secondFlightDepartureDate'] = get_hour(self.flight['itineraries'][index]['segments'][1]['departure']['at'])
                offer[f'{index}secondFlightAirlineLogo'] = get_airline_logo(self.flight['itineraries'][index]['segments'][1]['carrierCode'])
                offer[f'{index}secondFlightAirline'] = self.flight['itineraries'][index]['segments'][1]['carrierCode']
                offer[f'{index}secondFlightArrivalAirport'] = self.flight['itineraries'][index]['segments'][1]['arrival']['iataCode']
                offer[f'{index}secondFlightArrivalDate'] = get_hour(self.flight['itineraries'][index]['segments'][1]['arrival']['at'])
                offer[f'{index}secondFlightArrivalDuration'] = self.flight['itineraries'][index]['segments'][1]['duration']
                offer[f'{index}FlightTotalDuration'] = self.flight['itineraries'][index]['duration'][2:]
                offer[f'{index}stop_time'] = get_stoptime(self.flight['itineraries'][index]['duration'],
                                                               offer[f'{index}firstFlightArrivalDuration'],
                                                               offer[f'{index}secondFlightArrivalDuration'])

            elif len(self.flight['itineraries'][index]['segments']) == 1:  # direct flight
                offer[f'{index}firstFlightDepartureAirport'] = self.flight['itineraries'][index]['segments'][0]['departure']['iataCode']
                offer[f'{index}firstFlightAirlineLogo'] = get_airline_logo(self.flight['itineraries'][index]['segments'][0]['carrierCode'])
                offer[f'{index}firstFlightAirline'] = self.flight['itineraries'][index]['segments'][0]['carrierCode']
                offer[f'{index}firstFlightDepartureDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['departure']['at'])
                offer[f'{index}firstFlightArrivalAirport'] = self.flight['itineraries'][index]['segments'][0]['arrival']['iataCode']
                offer[f'{index}firstFlightArrivalDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['arrival']['at'])
                offer[f'{index}firstFlightArrivalDuration'] = self.flight['itineraries'][index]['segments'][0]['duration']
                offer[f'{index}FlightTotalDuration'] = self.flight['itineraries'][index]['duration'][2:]

            index += 1
        return offer


def get_airline_logo(carrier_code):
    return f'https://s1.apideeplink.com/images/airlines/{carrier_code}.png'


# returns the hour:minutes from a datetime
def get_hour(date_time):
    return datetime.strptime(date_time[0:19], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")


# calculates the layover duration
def get_stoptime(total_duration, first_flight_duration, second_flight_duration):
    if re.search('PT(.*)H', total_duration) is None:
        total_duration_hours = 0
    else:
        total_duration_hours = int(re.search('PT(.*)H', total_duration).group(1))
    if re.search('H(.*)M', total_duration) is None:
        total_duration_minutes = 0
    else:
        total_duration_minutes = int(re.search('H(.*)M', total_duration).group(1))

    if re.search('PT(.*)H', first_flight_duration) is None:
        first_flight_hours = 0
    else:
        first_flight_hours = int(re.search('PT(.*)H', first_flight_duration).group(1))
    if re.search('H(.*)M', first_flight_duration) is None:
        first_flight_minutes = 0
    else:
        first_flight_minutes = int(re.search('H(.*)M', first_flight_duration).group(1))

    if re.search('PT(.*)H', second_flight_duration) is None:
        second_flight_hours = 0
    else:
        second_flight_hours = int(re.search('PT(.*)H', second_flight_duration).group(1))
    if re.search('H(.*)M', second_flight_duration) is None:
        second_flight_minutes = 0
    else:
        second_flight_minutes = int(re.search('H(.*)M', second_flight_duration).group(1))

    connection_minutes = (total_duration_hours*60+total_duration_minutes) - (first_flight_hours*60 + first_flight_minutes + second_flight_hours*60 + second_flight_minutes)
    hours = connection_minutes // 60
    minutes = connection_minutes % 60
    return str(hours)+':'+str(minutes)


def get_probability(choice_probability):
    probability = float(choice_probability)
    if probability > 0.01:
        return '{0:.0f}% probability'.format(probability * 100)
    else:
        return 'really low probability'
