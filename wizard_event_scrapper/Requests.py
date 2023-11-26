import requests
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

class EventRequests():
    def __init__(self):
        self.location_uri = "https://api.tabletop.wizards.com/event-reservations-service/Organizations/by-location?"
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_api_uri = f"https://maps.googleapis.com/maps/api/geocode/json?"
        self.event_uri = "https://api.tabletop.wizards.com/event-reservations-service/events/search?"

    def getLatLongFromZip(self, zip):
        logging.info("Making request to google maps api")
        r =requests.get(self.google_api_uri,
                                params = {
                                    "address" : zip,
                                    "key" : self.google_api_key
                                }
                            ).json()['results'][0]['geometry']['location']
        logging.info("Successfully retrieved lat and longs")
        return r['lat'], r['lng']
    
    def getLocations(self, zip_code):
        logging.info(f"Finding lat and long for {zip_code}")
        lat, long = self.getLatLongFromZip(zip_code)
        r = requests.get(self.location_uri, 
                         params= {
                            'lat' : f'{lat}',
                            'lng' : f'{long}',
                            'maxMeters' : '15000',
                            'pageSize' : '10000',
                            'isPremium' : 'false'
                         }
                         )
        return r.json()['results']
    
    def getLocationIds(self, zip_code):
        ids = [i['id'] for i in self.getLocations(zip_code)]
        return ids
    
    def getLocationNames(self, zip_code):
        names = [i['name'] for i in self.getLocations(zip_code)]
        return names
    
    def getLocationId(self, location_name, zip_code):
        locations = self.getLocations(zip_code)
        for name in locations:
            if location_name in name['name'].lower():
                return name['id']
    
    def getAllEvents(self, zip_code):
        logging.info(f"Finding lat and long for {zip_code}")
        lat, long = self.getLatLongFromZip(zip_code)
        r = requests.get(self.event_uri, 
                         params = {
                            'lat' : f'{lat}',
                            'lng' : f'{long}', 
                            'isPremium' : 'false',
                            'tag' : 'magic:_the_gathering',
                            'searchType' : 'magic-events',
                            'maxMeters' : '100000',
                            'pageSize' : '100',
                            'page' : '0', 
                            'sort' : 'date', 
                            'sortDirection' : 'asc'
                         }
                         )
        return r.json()['results']

    def formatDatetime(self, timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y %H:%M:%S')
    
    def getLocationEvents(self, location_id, zip_code):
        logging.info(f"Getting event information for {location_id}")
        all_events = self.getAllEvents(zip_code)
        location_events = [[i['name'], i['description'], self.formatDatetime(i['startDatetime'])] for i in all_events if i['organizationId'] == location_id]
        logging.info(f"Retreieved the following events {location_events}")
        return location_events