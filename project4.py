# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, json
from advanced_expiry_caching import Cache


FILENAME = "national_park_cache.json"

program_cache = Cache(FILENAME)


def url_generator():
    states = {"Alabama": "AL", "Alaska" : "AK", "Arizona" : "AZ"," Arkansas" : "AR", "California" : "CA", "Colorado" : "CO", "Connecticut" : "CT", "Delaware" : "DE", "Florida" : "FL", "Georgia" : "GA", "Hawaii" : "HI", "Idaho" : "ID", "Illinois" : "IL", "Indiana" : "IN", "Iowa" : "IA", "Kansas" : "KS", "Kentucky" : "KY", "Louisiana" : "LA", "Maine" : "ME", "Maryland" : "MD", "Massachusetts" : "MA", "Michigan" : "MI", "Minnesota" : "MN", "Mississippi" : "MS", "Missouri" : "MO", "Montana" : "MT", "Nebraska" :  "NE", "Nevada" : "NV", "New Hampshire" : "NH", "New Jersey" : "NJ", "New Mexico" : "NM", "New York" : "NY", "North, Carolina" : "NC", "North Dakota" : "ND", "Ohio" : "OH", "Oklahoma" : "OK", "Oregon" : "OR", "Pennsylvania" : "PA", "Rhode Island" : "RI", "South Carolina" : "SC", "South Dakota" : "SD", "Tennessee" : "TN", "Texas" : "TX", "Utah" : "UT", "Vermont" : "VT", "Virginia" : "VA", "Washington" : "WA", "West Virginia" : "WV", "Wisconsin" : "WI", "Wyoming" : "WY"}
    urllist = []
    for state in states:
        abbv = states[state].lower()
        url = "https://www.nps.gov/state/" + abbv + "/index.htm"
        print(url)
        urllist.append(url)
    return urllist

def get_data(url):
    data = program_cache.get(url)
    if not data:
        try:
            r = requests.get(url, timeout = 30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("good")
            data = r.text
            program_cache.set(url, data, expire_in_days=1)
        except:
            print("error")
            data = None
    return data

def process_data(r_object):
    soup = BeautifulSoup(r_object, "html.parser")
    list_park = soup.find(id="list_parks")
    park_info = list_park.findChildren("div",{ "class" : "col-md-9 col-sm-9 col-xs-12 table-cell list_left"}, recursive = True)
    with open("nationalpark.csv","a+",encoding = "utf-8") as f:
        for park in park_info:
            type = park.findChildren("h2", recursive = True)[0].text.replace("\n","").strip(" ")
            name = park.findChildren("h3", recursive = True)[0].text.replace("\n","").strip(" ")
            description = park.findChildren("p", recursive = True)[0].text.replace("\n","").replace("”",""").replace("“",""").strip(" ")
            location = park.findChildren("h4", recursive = True)[0].text.replace("\n","").strip(" ")
            result = type + "," + name + "," + "\"" + description +"\"" + "," + "\"" + location + "\"" + "\n"
            f.write(result)

states = url_generator()
with open("nationalpark.csv","w",encoding = "utf-8") as f:
    f.write("type,name,description,location\n")
for state_url in states:
    data_encoding = get_data(state_url)
    process_data(data_encoding)





# This assignment was done with Shi Lu together.
