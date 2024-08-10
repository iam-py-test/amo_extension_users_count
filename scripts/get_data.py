import os, sys, json

import requests
from bs4 import BeautifulSoup
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as allowedcolors

extensions = ['uBlock Origin']
current_date = datetime.datetime.now().strftime("%d/%m/%Y")

try:
    usercountdata = json.loads(open('data/usercount.json').read())
except:
    usercountdata = {}

for extension in extensions:
    try:
        amourl = f"https://addons.mozilla.org/en-US/firefox/addon/{extension.lower().replace(" ", "-")}/"
        amoreq = requests.get(amourl)
        reqtext = amoreq.text
        amosoup = BeautifulSoup(reqtext, 'html.parser')
        usercount_elm = amosup.select(".MetadataCard-content")
        usercount = int(usercount_elm.text.replace(","))
        if extension not in usercountdata:
            usercountdata[extension] = {}
        usercountdata[extension][current_date] = usercount
    except:
        pass

outcountfile = open('data/usercount.json', 'w')
outcountfile.write(json.dumps(usercountdata))
outcountfile.close()

# plot

for extension in extensions:
    formatted_extension_name = extension.lower().replace(" ", "-")
    if formatted_extension_name not in usercountdata:
        continue
    x = np.arange(1,len(usercountdata[formatted_extension_name]))
    y = np.array(usercountdata[formatted_extension_name])
    plt.title(f"Number of users for {extension}")
    plt.xlabel("Time")
    plt.ylabel("Users")
    plt.plot(x, y, color = "green")
    plt.savefig(f"imgs/{extension}")
    plt.clf()
