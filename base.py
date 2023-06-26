# coding=utf-8
import sys
import os
import time
from time import sleep
from datetime import datetime
import pymongo
from pymongo import MongoClient
import csv, getopt, pprint
import json
import requests
from skyscanner.skyscanner import Flights
from skyscanner.skyscanner import FlightsCache
import random
import bson
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from operator import itemgetter

#class JSONEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, ObjectId):
#            return str(o)
#        return json.JSONEncoder.default(self, o)

class comeflywithme():

    def __init__(self):

        #Localhost mongoDB DB
        try:
          self.connection = MongoClient('localhost:27017')
          self.db = getattr(self.connection, "Flightship")
          #print ("mongodb: check")
        except pymongo.errors.ConnectionFailure:
          print ("Could not connect to MongoDB")
        self.collection=self.db["ComeFlighWithMe"]

        #Free API Key used for test purposes
        self.flights_cache_service = FlightsCache('prtl6749****86**38****96**98****')

        #Predefined list of airports available (10)
        self.destinations=['PARI-sky','LOND-sky','AMS-sky']

    #Input  : City[] Date1 Date2
    #Output : ID to call the display function
    def create(self, cities, outbounddate, inbounddate):
        url="http://127.0.0.1:5000/api/0.1/create"
        Push={}
        newID=self.collection.insert(Push)
        payload={"cities":cities,"outbounddate":outbounddate,"inbounddate":inbounddate,"mongoid":newID}
        requests.post(url,params=payload)
        return {"id":newID}

    def created(self, cities, outbounddate, inbounddate, mongoid):
        #We itarate through every input city and exclude the existing ones

        departurecities=[]
        for city in cities:

            #find the skyscanner airport-code according to the fact that we already have an airport city as an input
            url="http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/GER/EUR/en-GB?query="+city+"&apiKey=prtl6749387986743898559646983194"
            result=requests.get(url).json();
            #pprint.pprint(result)
            #[0] is corresponding to the "any" option if it exists
            departurecities.append(result["Places"][0]["PlaceId"])
            
        TopDestinations=[]
        for airport in self.destinations:
            if airport in departurecities:
                continue;
            TotalPrice=0;
            Quotes=[];
            for departurecity in departurecities:

                print(departurecity)
                print(airport)
                print("-----")
                result = self.flights_cache_service.get_cheapest_quotes(
                market='FR',
                currency='EUR',
                locale='fr-FR',
                originplace=departurecity,
                destinationplace=airport,
                outbounddate=outbounddate,
                inbounddate=inbounddate).parsed
                #pprint.pprint(result)
                cheapest_quote = {}
                for quote in result['Quotes']:
                    if "MinPrice" not in quote:
                        continue;
                    elif "MinPrice" not in cheapest_quote:
                        cheapest_quote = quote;
                    elif quote["MinPrice"] <= cheapest_quote["MinPrice"]:
                        cheapest_quote = quote;
                Quotes.append(cheapest_quote);
                pprint.pprint(cheapest_quote);
                if "MinPrice" not in cheapest_quote:
                    continue;
                TotalPrice=TotalPrice+cheapest_quote["MinPrice"]
            TopDestinations.append({"destination":airport,"TotalPrice":TotalPrice,"Quotes":Quotes})
        Push={"Destinations":TopDestinations}
        try:
            self.collection.update_one({"_id": ObjectId(mongoid)},{"$set": Push})

        except:
            print "error while adding "+Push+" in the DB"
        Push["_id"]="";

        #use return Push for a full response
        return Push
        #return {"id":newID}

    def display(self, id):
        #Export Top5 Destinations for this Group

        results=self.collection.find({"_id": ObjectId(id)})[0]["Destinations"]
        data = sorted(results, key=itemgetter('TotalPrice')) 
        #print results
        #return [data[0],data[1],data[2]]
        return data


    