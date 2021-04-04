import requests
import json
from matplotlib import pyplot as plt

"""AGE OF EMPIRES 2 IS ONE OF THE MOST POPULAR STRATEGY GAMES EVER AND IT HAS A LOT OF DATA TO ANALIZE , 
IN THIS PROJECT i'M GOING TO WORK WITH THE INFORMATION OF THE RECENT MATCHES OF A PLAYER , ANALYZING WHAT ARE THE 
MOST USED CIVILIZATIONS CURRENTLY , SO WE CAN ASSUME THAT THIS CIVILIZATIONS ARE THE MOST COMMON OR THE MOST 
POWERFUL IN THE GAME , AND WITH THIS INFORMATION A NEW PLAYER CAN HAVE SOME INDICATION BEFORE PLAYING."""

#------------------------DEFINING VARIABLES-------------------------
"""Every civilization has a code so i have analyzed multiple matches before making this program and at the end i have
realized it was a alphabetic order so i made a dictionary with all the key/values - civ/code ."""
def initialization():

        global slices
        global explode
        global civ_used
        global civ_code

        slices = []
        explode = []
        civ_used = {}
        civ_code = {
                0:"Aztecs",1:"Berbers",2:"Britons",3:"Bulgarians",4:"Burgundians",5:"Burmese",
                6:"Byzantines",7:"Celts",8:"Chinese",9:"Cumans",10:"Ethyopians",11:"Franks",
                12:"Goths",13:"Huns",14:"Incas",15:"Indians",16:"Italians",17:"Japanese",
                18:"Khmer",19:"Koreans",20:"Lithuanians",21:"Magyars",22:"Malay",23:"Malians",
                24:"Mayans",25:"Mongols",26:"Persians",27:"Portuguese",28:"Saracens",29:"Sicilians",
                30:"Slavs",31:"Spanish",32:"Tatars",33:"Teutons",34:"Turks",35:"Vietnamese",36:"Vikings"}
            
#---------------REQUEST AND CREATION OF JSON FILE------------------

def file_request():

        request = requests.get("https://aoe2.net/api/player/matches?game=aoe2de&steam_id="+ str(steam_id) + "&count=" + str(matches_quantity))
        request_text = request.text
        data = json.loads(request_text)
        json.dump(data,open("TEST.json","w"),indent=4)

#-------------------------CLEANING DATA----------------------------
"""In the cleaning process i wanted to see only ranked and 1v1 matches, so the program clear all the data if the ranked 
key was equal to "false" or the number of players was higher than 2 , the purpose was to make the data more manageable
focusing on the player and plot his most used civilizations."""

def cleaning_data():
        with open("TEST.json","r+") as file_json:
                data = json.load(file_json)

                for game in data:
                        
                        #----------RANKED , 2 PLAYERS AND CLEANING CORRUPTED GAMES-------
                        
                        if str(game["ranked"]) == "False" or game["num_players"] > 2 or str(game["players"][0]["civ"]) == "None":
                                game.clear()
                                continue
                        
                        #----------------PLAYER FOCUS----------------------
                        
                        if game["players"][0]["name"] == player_selected: #----PLAYER SELECTED
                                del game["players"][1]
                        else:
                                del game["players"][0]

                        #--------------DELETE USELESS DATA-----------------
                        
                        data_copy = game["players"]
                        game.clear()
                        game["players"] = data_copy
                        
                        #---------------DUMP OF DATA INTO JSON FILE--------
                        
                        file_json.seek(0)
                        json.dump(data,file_json, indent=4)
                        file_json.truncate()

#----------------------DATA EXPLORATION----------------------------
"""The function searchs for the used civilizations of the player selected , 
if the game/match information is empty the program continues to the next game/match.
It stores the code in a variable , and then compares if the name of that civilizations exist in 
a new dictionary called "civ_used", if the civilization exist it adds 1 , if not , it creates the key
with a value of 1 """

def data_exploration():
        with open("TEST.json","r+") as file_json:
                data = json.load(file_json)
                for game in data:
                        if game:
                                code = int(game["players"][0]["civ"])
                                if civ_code[code] in civ_used:
                                        civ_used[civ_code[code]] += 1
                                else:
                                        civ_used[civ_code[code]] = 1
                        else:
                                continue

#-------------------------PIE PLOT---------------------------------

def pie_plot():
        global labels

        plt.style.use("fivethirtyeight")
        labels = list(civ_used.keys())
        for item in civ_used:
                slices.append(civ_used.get(str(item)))

#---------------ISOLATION OF BIGGEST SLICE FROM PLOT------------------
"""Copy "slices"( LIST ) into "explode"( Empty List ) , then it selects the maximum number in the new created list.
Then it stores the index of the most used civilization into a variable for later use.
After that it change all the values of the list "explode" to 0 and the most used to 0.2."""

def explode_slice():
        #---------------------------------------------------------------------------------------------------------------------------------------
        explode = slices[:]
        most_used_civilization = max(explode)
        index_most_used_civilization = explode.index(most_used_civilization)
        for x in range(0,len(explode)):
                explode[x] = 0
        explode[index_most_used_civilization] = 0.1
        #---------------------------------------------------------------------------------------------------------------------------------------
        plt.tight_layout()
        plt.pie(slices,labels=labels,wedgeprops={"edgecolor":"black"},shadow=True,startangle=90,explode=explode,autopct="%1.1f%%",rotatelabels=5)
        plt.show()

#------------------------FILTERS AND PARAMETERS OF SEARCH-------------------------------
steam_id = 76561198011194433 #------------------STEAM PLAYER ID
matches_quantity = 25 #-------------( 500+ TAKES AROUND 40 secs )--- MAXIMUM NUMBER IS 1000, REPRESENT HOW MANY MATCHES YOU WANT TO USE AS DATA                                            
player_selected = "[TuKn] Cepitaxx" #--------------ISOLATES PLAYER IN DATA , BY DEFAULT THE PLAYER IS THE SAME OF THE ID
#---------------------------------------------------------------------------------------
initialization()
file_request()
cleaning_data()
data_exploration()
pie_plot()
explode_slice()
#---------------------------------------------------------------------------------------
