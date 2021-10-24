# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from rasa_sdk.events import AllSlotsReset

from typing import Any, Text, Dict, List
from pymongo.database import Database
from pymongo import MongoClient
from rasa_sdk import Action, Tracker, FormValidationAction 
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.MongoConnect import getProductDetailsFromMongo 
from actions.MongoConnect import setClientInfoFromMongo
import pymongo
# url="http://localhost:3000/api"
# class refAction(Action):
#     def name(self):
#         return "refAction"
#     def run(self, dispatcher, tracker, domain):
#         client = pymongo.MongoClient("localhost", 27017)
#         db=client.sample
#         res = db.datas.find({'action':'refAction'})
#         print(type(res))
#         for i in res:
#             dispatcher.utter_button_message(i['text'],i['buttons'])
#         return []

         

class ValidateFormCommand(FormValidationAction):
    def name(self):
        return "validate_form_command"
    def validate_sku(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"le code du produit {slot_value} validé")
        return {"sku": slot_value}

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"el commande b esm {slot_value} est enregistré")
        return {"name": slot_value}

    def validate_adres(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"touslek el commande lil adresse {slot_value}")
        return {"adres": slot_value}

    def validate_tel(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"el numero {slot_value} bch ykalmouk 3lih el service client")
        return {"tel": slot_value}

#enregistrer dans mongo
class StoreDataOfCommand(Action):

    def name(self) -> Text:
        return "store_data_of_command"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["sku","name","adres","tel"] 
    def slot_mapping(self):
        return {"sku": self.from_entity(entity="sku",
                                        intent="ref_produit"),
                "name": self.from_entity(entity="name",
                                        intent="nom_client"),
                "adres": self.from_entity(entity="adres",
                                        intent="adresse"),
                "tel": self.from_entity(entity="tel",
                                        intent="tel"),                                                                                
                }
    def run(self,
               dispatcher:CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any])-> List[Dict]:
        sku = tracker.get_slot('sku')
        name = tracker.get_slot('name')
        adres = tracker.get_slot('adres')
        tel = tracker.get_slot('tel')
        commande = {}
        commande = { "name": name, "address": adres, "mobile_phone": tel, "sku_product": sku}
        result = setClientInfoFromMongo(commande)
        dispatcher.utter_message(template="utter_cmd")#template="utter_cmd"
        AllSlotsReset
        return[]
############################################################################################
class AskForSkuAction(Action):
    def name(self) -> Text:
        return "action_ask_sku"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        dispatcher.utter_message(template="utter_ask_sku")
        return []
class AskForNameAction(Action):
    def name(self) -> Text:
        return "action_ask_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        dispatcher.utter_message(template="utter_ask_name")
        return []

class AskForAdresAction(Action):
    def name(self) -> Text:
        return "action_ask_adres"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        dispatcher.utter_message(template="utter_ask_adres")
        return []

class AskForTelAction(Action):
    def name(self) -> Text:
        return "action_ask_tel"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        dispatcher.utter_message(template="utter_ask_tel")
        return []


############################################################################################
# class ActionSaveComDetails(sku, name, adres, tel):

#     def name(self) -> Text:
#         return "action_save_com_details"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         commande= { "name:" name, "adresse:" adres, "tel:" tel, "sku_product:" sku}
#         result = setClientInfoFromMongo(commande)
#         dispatcher.utter_message("client ajouté")
#         return []


# class ActionProductPrice(Action):

#     def name(self) -> Text:
#         return "action_product_price"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         product_price = (getProductDetailsFromMongo()['product_price']) 
#         dispatcher.utter_message(template="utter_ref_dispo", product_price=product_price)
#         return []
# class Actionproductname(Action):

#     def name(self) -> Text:
#         return "action_product_name"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         product_name = (getProductDetailsFromMongo()['product_name']) 
#         dispatcher.utter_message(template="utter_ref_dispo", product_name=product_name)
#         return []

# class action_product_name(Action):

#     def name(self) -> Text:
#         return "action_product_name"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="utter_ref_dispo")
#         return []
        
class Actionproductdetails(Action):

    def name(self) -> Text:
        return "action_product_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sku = tracker.get_slot("sku")
        product_sku = (getProductDetailsFromMongo(sku)['product_sku']) 
        product_name = (getProductDetailsFromMongo(sku)['product_name']) 
        product_price = (getProductDetailsFromMongo(sku)['product_price']) 
        total_qty_available = (getProductDetailsFromMongo(sku)['total_qty_available']) 
        dispatcher.utter_message(template="utter_ref_dispo", product_sku=product_sku ,product_name=product_name , product_price=product_price, total_qty_available=total_qty_available)
        return [AllSlotsReset()]
