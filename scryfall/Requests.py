import requests
import os
from dotenv import load_dotenv
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

class CardRequests():
    def __init__(self):
        self.scryfall_uri = 'https://api.scryfall.com/cards/named?'

    def submitRequest(self, search_type, card_name):
        r = requests.get(self.scryfall_uri, 
                        params = {
                            f'{search_type}' : f'{card_name}'
                        }
                        )
        return r.json()

    def getCard(self, card_name):
        logging.info(f"Getting card with name {card_name}")
        logging.info(f"Trying exact search first")
        card = self.submitRequest('exact', card_name)
        if card['object'] == 'error':
            logging.info("Trying fuzzy search now")
            card = self.submitRequest('fuzzy', card_name)
        elif card['object'] == 'card':
            card = card
        else:
            card['details'] = f"Sorry, I cannot find this card. Please check the spelling or ensure the proper name."
        self.card = card
        self.cardFaceBool()
        return card
    
    def cardFaceBool(self):
        try:
            if self.card['card_faces']:
                logging.info("Found card faces")
                self.card_face_bool = True
        except:
            logging.info("No card faces found")
            self.card_face_bool = False

    
    def handleCardFace(self, key):
        if self.card_face_bool:
            # return self.card['card_faces'][0][key]
            try:
                return self.card['card_faces'][0][key], self.card['card_faces'][1][key]
            except KeyError:
                return self.card['card_faces'][0][key]

    def getCardAttr(self, attr):
        exceptions = ['uri']
        if attr in exceptions:
            try:
                return self.card[attr]
            except KeyError as e:
                logging.info(e)
        elif self.card_face_bool == True:
            attr = self.handleCardFace(attr)
            try:
                logging.info("Returning both attrs")
                return attr[0], attr[1]
            except IndexError:
                logging.info("Only single attr exists - Returning single attr")
                return attr[0]
        else:
            try:
                logging.info("No card faces found.")
                return self.card[attr]
            except KeyError as e:
                logging.info(e)
        

# card_class = CardRequests()
# card_object = card_class.getCard('realmwalker')

# print(card_class.getCardAttr('image_uris'))
# # print(f"{card_class.getCardAttr('image_uris')[0]['normal']}")
