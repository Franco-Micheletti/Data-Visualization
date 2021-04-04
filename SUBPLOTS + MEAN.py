from numpy.core.fromnumeric import mean
import requests
import json
from datetime import datetime
from matplotlib import pyplot as plt




def request(compared_players):
    global ratings
    global dates
    global ratings_player1
    global ratings_player2
    global ratings_player3
    global dates_player1
    global dates_player2
    global dates_player3
    ratings = []
    dates = []
    ratings_player1 = []
    ratings_player2 = []
    ratings_player3 = []
    dates_player1 = []
    dates_player2 = []
    dates_player3 = []

    for code in compared_players:
        ratings = []
        dates = [] 
        request = requests.get("https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&steam_id=" + str(code) + "&count=" + str(matches_quantity))
        request_text = request.text
        data = json.loads(request_text)
        json.dump(data,open("RATINGS.json","w"),indent=4)

        with open("RATINGS.json", "r+") as a:
            data = json.load(a)
            for game in data:
                #-----------------DATE CONVERTION------------------------

                time = game["timestamp"]
                fecha_real = str(datetime.fromtimestamp(time))
                fecha_real=fecha_real[0:10]
                game["Date"] = fecha_real
                del game["timestamp"]

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

        if compared_players.index(code) == 0:
            ratings_player1 = ratings[:]
            dates_player1 = dates[:]
        elif compared_players.index(code) == 1:
            ratings_player2 = ratings[:]
            dates_player2 = dates[:]
        elif compared_players.index(code) == 2:
            ratings_player3 = ratings[:]
            dates_player3 = dates[:]
        
def mean_plotting(ratings):
    global average
    sum = 0
    for x in ratings:
        sum+=x
    average = sum / len(ratings)

def plot(names):
    
    fig,axes = plt.subplots(nrows=3,ncols=1)
 
    for x in range(3):

        #-----------------------RATINGS-----------------------------------
        axes[x].set_title("  RATING - " + str(names[x]))
        
        if x == 0:
            axes[0].plot(dates_player1,ratings_player1,color="#05aafc")
            mean_plotting(ratings_player1)
        elif x == 1:
            axes[1].plot(dates_player2,ratings_player2,color="#05aafc")
            mean_plotting(ratings_player2)
        elif x == 2:
            axes[2].plot(dates_player3,ratings_player3,color="#05aafc")
            mean_plotting(ratings_player3)

        axes[x].grid(True)
        axes[x].set_xticklabels([])
        average_line = axes[x].axhline(y=average,linestyle='dashed',color="#f00aec")
        axes[x].legend([average_line],['Average rank'],loc=2)



    #-------------------------------------------------------------------
    fig.subplots_adjust(wspace=0.2,hspace=0.2)
    plt.figure(1,figsize=(9.1,9.1),edgecolor="#05aafc")
    plt.tight_layout()
    plt.show()

#----------------------------NUMBER OF MATCHES-----------------------------
matches_quantity = 300
#---------------------------------EXAMPLES---------------------------------
#                       PLAYER 1      -    PLAYER 2    -      PLAYER 3
compared_players = [76561198011194433,76561198202025889,76561198006335392]
names            = [ "[Tukn]Cepitaxx", "Technotronic"  ,  "[TuKn]idclip" ]

#---------------------------------EXAMPLES---------------------------------
#                       PLAYER 1      -    PLAYER 2    -      PLAYER 3
#compared_players = [76561198088251629,76561198044559189,76561198449406083]
#names            = [     "TATOH"     ,      "DAUT"     ,     "HERA"      ]
#--------------------------------------------------------------------------
"""     TATOH           = 76561198088251629
        DAUT            = 76561198044559189
        BACT            = 76561198272641645
        MBL             = 76561197996386232  
        MR_YO           = 76561198179087382
        HERA            = 76561198449406083
        JORDAN          = 76561198400058723
        LIERREY         = 76561198362219694
        NICOV           = 76561198027378107
        VIPER           = 76561197984749679
        DOGAO           = 76561197992981071
        ACCM            = 76561198364718180
        [Tukn]Cepitaxx  = 76561198011194433
        Technotronic    = 76561198202025889
        [TuKn]idclip    = 76561198006335392
"""
#--------------------------------------------------------------------------
request(compared_players)
plot(names=names)
#--------------------------------------------------------------------------

