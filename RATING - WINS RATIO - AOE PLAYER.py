import requests
import json
from datetime import datetime
from matplotlib import pyplot as plt

"""AGE OF EMPIRES 2 IS ONE OF THE MOST POPULAR STRATEGY GAMES EVER AND IT HAS A LOT OF DATA TO ANALIZE , IN THIS PROJECT 
WE WILL WORK WITH THE DATA OF THE RECENTS 1V1 RANKED MATCHES OF A PLAYER , THE INFORMATION WE USE IS THE RATING AND THE DATE OF THE MATCHES.
THE RESULT IS AN INSIGHT OF THE PERFORMANCE OF A PLAYER ALONG THE TIME AND WHAT PERCENT OF WIN GAMES ONE PLAYER NEEDS TO REACH A SPECIFIC RANK. """
#----------------REQUEST AND CREATION OF JSON FILE---------------

def json_file():

    global ratings
    global dates
    ratings = []
    dates = []
    request = requests.get("https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&steam_id=" + str(steam_id) + "&count=" + str(matches_quantity))
    request_text = request.text
    data = json.loads(request_text)
    json.dump(data,open("TEST2.json","w"),indent=4)

#-------------------------CLEANING DATA--------------------------  
"""The data requested is the match history of only one player, the data was simple , but the time of each match was 
in timestamp format , so i had converted this number into normal date format, after that i have deleted the keys that i will not use.
At the end i had made two lists of all the ratings and dates for ploting"""

def cleaning_data():
    with open("TEST2.json", "r+") as a:
        data = json.load(a)
        
        #-------------------SAVING FOR WIN RATE % PLOT---------------
        global wins
        global loses
        wins = data[0]["num_wins"]
        loses = data[0]["num_losses"]


        for game in data:
            #-----------------DATE CONVERTION------------------------

            time = game["timestamp"]
            fecha_real = str(datetime.fromtimestamp(time))
            fecha_real=fecha_real[0:10]
            game["Date"] = fecha_real
            del game["timestamp"]

            #---------------DELETE USELESS DATA----------------------

            del game["streak"]
            del game["drops"]
            del game["num_wins"]
            del game["num_losses"]

            #----------------DUMP OF DATA INTO JSON FILE-------------

            a.seek(0)
            json.dump(data,a, indent=4)
            a.truncate()
            
            #---------CREATION OF RATINGS AND DATES LISTS------------

            ratings.append(game["rating"])
            dates.append(game["Date"])

    #-----------------REVERSE LIST-----------------------------------
    ratings.reverse()
    dates.reverse()

#----------------------------PLOTS-------------------------------    

def plots():
    #----------WIN / LOSE RATIO PIE PLOT-------------------------

    plt.figure(1)
    plt.style.use("fivethirtyeight")
    labels = ["WINS","LOSES"]
    slices = [wins,loses]
    if wins>loses:
        explode = [0.1,0]
    else:
        explode = [0,0.1]
    
    plt.tight_layout()
    plt.pie(slices,labels=labels,wedgeprops={"edgecolor":"black"},explode=explode,shadow=True,startangle=90, autopct="%1.1f%%")
    
    # --------------RATING PLOT----------------------------------
    plt.figure(2)
    plt.style.use("fivethirtyeight")
    plt.plot(dates,ratings)
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.text(0,0,0,fontsize=2)
    plt.show()
    
#----------------FILTERS AND PARAMETERS OF SEARCH----------------
steam_id = 76561198011194433 #------------STEAM PLAYER ID
matches_quantity = 1000 #-----------------MAXIMUM NUMBER IS 1000, REPRESENT HOW MANY MATCHES YOU WANT TO USE AS DATA
json_file()
cleaning_data()
plots()


