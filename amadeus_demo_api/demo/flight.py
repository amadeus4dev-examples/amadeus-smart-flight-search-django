from datetime import datetime, timedelta


class Flight:
    def __init__(self, flight):
        self.flight = flight

    def construct_flights(self):
        offer = {}
        index = 0
        if 'choiceProbability' in self.flight:
            offer['probability'] = get_probability(self.flight['choiceProbability'])
        offer['price'] = int(round(float(self.flight['offerItems'][0]['price']['total'])))
        offer['id'] = self.flight['id']
        for f in self.flight['offerItems'][0]['services']:
            # Keys starting from 0 correspond to Outbound flights and the keys starting from 1 tp Return flights
            if len(self.flight['offerItems'][0]['services'][index]['segments']) == 2:  # one stop flight
                offer[str(index) + 'firstFlightDepartureAirport'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['departure'][
                        'iataCode']
                offer[str(index) + 'firstFlightAirlineLogo'] = \
                    get_airline_logo(
                        self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['carrierCode'])
                offer[str(index) + 'firstFlightAirline'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['carrierCode']
                offer[str(index) + 'firstFlightDepartureDate'] = \
                    get_hour(
                        self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['departure'][
                            'at'])
                offer[str(index) + 'firstFlightArrivalAirport'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['arrival'][
                        'iataCode']
                offer[str(index) + 'firstFlightArrivalDate'] = \
                    get_hour(self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['arrival'][
                                 'at'])
                offer[str(index) + 'firstFlightArrivalDuration'] = \
                    get_duration(
                        self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['duration'])
                offer[str(index) + 'secondFlightDepartureAirport'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['departure'][
                        'iataCode']
                offer[str(index) + 'secondFlightDepartureDate'] = \
                    get_hour(
                        self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['departure'][
                            'at'])
                offer[str(index) + 'secondFlightAirlineLogo'] = \
                    get_airline_logo(
                        self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['carrierCode'])
                offer[str(index) + 'secondFlightAirline'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['carrierCode']
                get_hour(
                    self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['departure']['at'])
                offer[str(index) + 'secondFlightArrivalAirport'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['arrival'][
                        'iataCode']
                offer[str(index) + 'secondFlightArrivalDate'] = \
                    get_hour(self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['arrival'][
                                 'at'])
                offer[str(index) + 'secondFlightArrivalDuration'] = \
                    get_duration(
                        self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['duration'])
                offer[str(index) + 'stop_time'] = get_stoptime(
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['arrival']['at'],
                    self.flight['offerItems'][0]['services'][index]['segments'][1]['flightSegment']['departure']['at'])
                offer[str(index) + 'FlightTotalDuration'] = get_total_duration_connecting_flights(
                    offer[str(index) + 'stop_time'], offer[
                        str(index) + 'firstFlightArrivalDuration'], offer[str(index) + 'secondFlightArrivalDuration'])

            elif len(self.flight['offerItems'][0]['services'][index]['segments']) == 1:  # direct flight
                offer[str(index) + 'price'] = self.flight['offerItems'][0]['price']['total']
                offer[str(index) + 'firstFlightDepartureAirport'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['departure'][
                        'iataCode']
                offer[str(index) + 'firstFlightAirlineLogo'] = \
                    get_airline_logo(
                        self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['carrierCode'])
                offer[str(index) + 'firstFlightAirline'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['carrierCode']
                offer[str(index) + 'firstFlightDepartureDate'] = \
                    get_hour(
                        self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['departure'][
                            'at'])
                offer[str(index) + 'firstFlightArrivalAirport'] = \
                    self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['arrival'][
                        'iataCode']
                offer[str(index) + 'firstFlightArrivalDate'] = \
                    get_hour(self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['arrival'][
                                 'at'])
                offer[str(index) + 'firstFlightArrivalDuration'] = \
                    get_duration(
                        self.flight['offerItems'][0]['services'][index]['segments'][0]['flightSegment']['duration'])
                offer[str(index) + 'FlightTotalDuration'] = get_total_duration_direct_flight(
                    offer[str(index) + 'firstFlightArrivalDuration'])
            index += 1

        return offer


def get_hour(date_time):
    return datetime.strptime(date_time[0:19], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")


def get_total_duration_direct_flight(flight_duration):
    hr = flight_duration[0:2]
    min = flight_duration[3:]
    if int(hr) == 0:
        return "%02dm" % (int(min))
    elif int(min) == 0:
        return "%dh" % (int(hr))
    return "%dh %02dm" % (int(hr), int(min))


def get_total_duration_connecting_flights(stop_time, first_flight_duration, second_flight_duration):
    timeList = [stop_time + ':00', first_flight_duration + ':00', second_flight_duration + ':00']
    totalSecs = 0
    for tm in timeList:
        timeParts = [int(s) for s in tm.split(':')]
        totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
    totalSecs, sec = divmod(totalSecs, 60)
    hr, min = divmod(totalSecs, 60)
    if hr == 0:
        return "%02dm" % min
    elif min == 0:
        return "%dh" % hr
    return "%dh %02dm" % (hr, min)


def get_duration(duration):
    res = datetime.strptime(duration, "%wDT%HH%MM")
    return res.strftime("%H:%M")


def get_stoptime(arrival_stop_time, departure_stop_time):
    arrival = datetime.strptime(arrival_stop_time[0:19], "%Y-%m-%dT%H:%M:%S")
    departure = datetime.strptime(departure_stop_time[0:19], "%Y-%m-%dT%H:%M:%S")
    stoptime = str(timedelta(seconds=(departure - arrival).seconds))
    if stoptime[1] == ':':
        stoptime = '0' + stoptime
    return stoptime[0:5]


def get_airline_logo(carrier_code):
    return "https://s1.apideeplink.com/images/airlines/" + carrier_code + ".png"


def get_probability(choice_probability):
    probability = float(choice_probability)
    if probability > 0.01:
        return '{0:.0f}% probability'.format(probability * 100)
    else:
        return 'really low probability'
