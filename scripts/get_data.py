import os, sys, json, datetime

import requests
from bs4 import BeautifulSoup
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as allowedcolors

extensions = ['uBlock Origin', "AdGuard AdBlocker", "Adblock Plus", "SponsorBlock", "Ghostery", "AdBlock for Firefox", "uBlock Origin Lite", "NoScript", "uMatrix", "uBO-Scope", "AdGuard Browser Assistant", "AdGuard VPN", "Unlock", "One Click Archive Today", "Archive Page", "archive-it-today"]
current_date = datetime.datetime.now().strftime("%d/%m/%Y")

def dict_as_arr(dic):
    """
    Return the items in a dict as a list (called an array here, don't sue me)
    I am sure there is a better way
    """
    arr = []
    for item in dic:
        arr.append(dic[item])
    return arr

try:
    os.mkdir("imgs")
except:
    pass
try:
    os.mkdir("data")
except:
    pass

try:
    usercountdata = json.loads(open('data/usercount.json').read())
except:
    usercountdata = {}

for extension in extensions:
    try:
        amourl = f"https://addons.mozilla.org/en-US/firefox/addon/{extension.lower().replace(" ", "-")}/"
        amoreq = requests.get(amourl)
        if amoreq.status_code == 404:
            continue
        reqtext = amoreq.text
        amosoup = BeautifulSoup(reqtext, 'html.parser')
        usercount_elm = amosoup.select("[data-testid=\"badge-user-fill\"] > .Badge-content--large")[0]
        usercount = int(usercount_elm.text.replace(",", "").replace(" Users", ""))
        if extension not in usercountdata:
            usercountdata[extension] = {}
        usercountdata[extension][current_date] = usercount
    except Exception as err:
        print(extension, err)

outcountfile = open('data/usercount.json', 'w')
outcountfile.write(json.dumps(usercountdata))
outcountfile.close()

# plot

for extension in extensions:
    formatted_extension_name = extension.lower().replace(" ", "-")
    if extension not in usercountdata:
        continue
    x = np.arange(1,len(usercountdata[extension]) + 1)
    y = np.array(dict_as_arr(usercountdata[extension]))
    plt.title(f"Number of users for {extension}")
    plt.xlabel("Time")
    plt.ylabel("Users")
    plt.plot(x, y, color = "green")
    plt.savefig(f"imgs/{extension}.png")
    plt.clf()



