import requests
import json
from flightdetails import FlightDetails

headers = {
'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
'x-rapidapi-key': "60293be8a8msh1eb6473839ccfe4p1e4146jsn8c81195c0179"
}

origin = {'Toronto': "YYZ-sky"}

def getPlace(location, country):
    '''
    (str, str) => json
    Uses skyscanner api to return the placeId of the selected city/country
    '''
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/CA/CAD/en-US/"
    querystring = {"query":location}
    response = requests.request("GET", url, headers=headers, params=querystring)
    info = json.loads(response.text)
    for element in info['Places']:
        if element['CountryName'] == country and location in element['PlaceName']:
            return element['PlaceId']
    return ''

def getQuoteInBound(destination, date):
    '''
    (str, str) => json
    Uses skyscanner api to return all flights details to a certain location
    '''
    url_ending = 'YYZ-sky/' + destination + '/' + date
    url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsedates/v1.0/CA/CAD/en-US/' + url_ending
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)

def getQuoteOutBound(destination, date):
    '''
    (str, str) => json
    Uses skyscanner api to return all flights details from a certain location
    '''
    url_ending = destination + '/YYZ-sky/' + date
    url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsedates/v1.0/CA/CAD/en-US/' + url_ending
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)

def getBestPrice(destination, start_date, end_date, min_duration, max_duration):
    '''
    (str, str, str, int, int) => json
    returns a collection of flights in sorted order by cheapest price
    '''
    in_bound = getQuoteInBound(getPlace('London', 'United Kingdom'), start_date)
    out_bound = getQuoteOutBound(getPlace('London', 'United Kingdom'), end_date)
    carriers_in = in_bound['Carriers']
    carriers_out = out_bound['Carriers']
    places_in = in_bound['Places']
    places_out = out_bound['Places']
    sorted_trips = []
    second_counter = 0
    for in_trip in in_bound['Quotes']:
        count = 0 + second_counter
        for out_trip in out_bound['Quotes']:
            count += 1
            if min_duration <= count and max_duration >= count:
                flight = FlightDetails(in_trip, out_trip, places_in, places_out, carriers_in, carriers_out)
                sorted_trips.append(flight)
        min_duration += 1
        max_duration += 1
    return sorted_trips

def getCost(element):
    return element.total_cost

sorted_flights = getBestPrice('London', '2020-05', '2020-05', 7, 9)
sorted_flights.sort(key=getCost)

for x in sorted_flights:
    x.printFlight()
