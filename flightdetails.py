class FlightDetails():
    """A class to contain the details of start and end flights"""

    def __init__(self, start_flight, end_flight, start_places, end_places, start_carriers, end_carriers):
        self.start_flight_date = start_flight['OutboundLeg']['DepartureDate']
        self.start_flight_price = start_flight['MinPrice']
        self.start_flight_direct = start_flight['Direct']
        self.start_flight_origin = 'YYZ-Toronto'
        self.start_flight_destination = self.getFlightDestination(start_flight, start_places)
        self.start_flight_carrier = self.getFlightCarrier(start_flight, start_carriers)

        self.end_flight_date = end_flight['OutboundLeg']['DepartureDate']
        self.end_flight_price = end_flight['MinPrice']
        self.end_flight_direct = end_flight['Direct']
        self.end_flight_origin = self.getFlightOrigin(end_flight, end_places)
        self.end_flight_destination = 'YYZ-Toronto'
        self.end_flight_carrier = self.getFlightCarrier(end_flight, end_carriers)

        self.total_cost = start_flight['MinPrice'] + end_flight['MinPrice']
        print("Flight Created")

    def printFlight(self):
        begin = self.start_flight_origin + '  -->  ' + self.start_flight_destination + ' (' + self.start_flight_date + ')  Price: ' + \
        str(self.start_flight_price) + '  ' + self.start_flight_carrier
        end = self.end_flight_origin + '  -->  ' + self.end_flight_destination + ' (' + self.end_flight_date + ')  Price: ' + \
        str(self.end_flight_price) + '  ' + self.end_flight_carrier
        print(begin)
        print(end)
        print("Total Cost: " + str(self.total_cost))

    def getFlightCarrier(self, flight, carriers):
        carriers_id = flight['OutboundLeg']['CarrierIds'][0]
        for element in carriers:
            if (element['CarrierId'] == carriers_id):
                return element['Name']
        return 'Error'
    def getFlightDestination(self, flight, places):
        place_id = flight['OutboundLeg']['DestinationId']
        for element in places:
            if (element['PlaceId'] == place_id):
                return element['SkyscannerCode'] + '-' + element['Name']
        return 'Error'

    def getFlightOrigin(self, flight, places):
        place_id = flight['OutboundLeg']['OriginId']
        for element in places:
            if (element['PlaceId'] == place_id):
                return element['SkyscannerCode'] + '-' + element['Name']
        return 'Error'
