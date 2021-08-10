import requests
import json
from matplotlib import pyplot as plt
import seaborn as sns

def request_and_plot(all_players):
    x,y=0,0
    count=0
    global ratings
    global dates
    sns.set_style("darkgrid")
    fig,axes = plt.subplots(nrows=4,ncols=2)
    for name in all_players.keys():
        ratings=[]
        dates=[]
        #----------------SHOW PROGRESS--------------    
        print("\033[H\033[J") 
        print(str(count) + " /"+str(len(all_players)))
        #----------------GET API REQUESTS-----------
        player_profile_id = all_players.get(name)
        if player_profile_id == 76561198133575502:
            request = requests.get("https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&steam_id=" + str(player_profile_id) + "&count=" + str(matches_quantity))
        else:
            request = requests.get("https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&profile_id=" + str(player_profile_id) + "&count=" + str(matches_quantity))
        request_text = request.text
        data = json.loads(request_text)
        json.dump(data,open("RATINGS_TOURNAMENT.json","w"),indent=4) 

        with open("RATINGS_TOURNAMENT.json", "r+") as a:
            data = json.load(a)
            for game in data:

                #---------CREATION OF RATINGS AND DATES LISTS------------

                ratings.append(game["rating"])
                dates.append(game["timestamp"])

        #-----------------REVERSE LIST-----------------------------------
        maximum_rank = max(ratings)
        ratings.reverse()
        dates.reverse()
        #-------------------------PLOT-----------------------------------
        sns.lineplot(ax=axes[x][y], x=dates, y=ratings,sizes=(10, 10),dashes=True,palette=None)
        axes[x][y].set_title(name + " - max: " + str(maximum_rank),color="c")
        axes[x][y].set_xticks([])
        if y==1:
            x+=1
            y=0
        else:
            y+=1
        count+=1
    plt.tight_layout()
    fig.subplots_adjust(wspace = 0.6,hspace = 0.8)
    fig.set_figheight(15)
    fig.set_figwidth(15)
    plt.show()

all_players = {
    "cdplayer":2664055,"dodgers":1238373,"El jabali":473031,"Asjjw":2883411,"Phalanx7572":2408911,"amypotato":240023,
    "Canel":702109,"HistoryNerd":27155}
    

"""all_players = {
    "ZachGC1":76561198133575502,"weasol":375902,"Disgruntled Goat":1205387,"[TAW] Krinski":2722551,"[TAW] Freager":3301525,"JIKredible1":254032,"cdplayer":2664055,
    "[ConF]FloFlo":844402,"BoesBoes":2010525,"RTSLife":3248054,"[TdBar] MagJeju":1339545,"[TdBar] kobukguille":2846058,"Yodha":4843062,"mitchandchickens":2276567,
    "NoobMaster69":1916433,"TheLastBender":2034401,"angelmc32":2258992,"[TdBar] Bronn 08":1944193,"Stagger Lee":1051803,"TinyTriss":236934,"ccpatriots":2621699,
    "dodgers":1238373,"[TabA] Scramble":2588553,"LAV XIV":2636308,"DrAntani":4623818,"Majestic":60857,"[SDG]Джимми Тонк":2369816,"Mi amado Poio™":1677127,
    "Grizzly Bob8584":1571960,"The Serge":901032,"El jabali de hierro":473031,"Uncle_Iroh":1989677,"HistoryNerd":27155,"Baybars8391":3953556,"Bitt3R":2133658,
    "francesco_solidoro":2661925,"BOB LOBLAW":3202592,"Jaw7811":3422855,"Griza":1714081,"Escipión":1958022,"Deathstyxx":525627,"Asjjw":2883411,"Phalanx7572":2408911,
    "PaPa_PeReZ":2783032,"Sensja":2279562,"PabloN":2143941,"Livi":2885693,"hardwiredlegend":3366033,"[BLKN] Tomo":2061303,"amypotato":240023,"F R E D || 弗雷德":753057,
    "Beefy":1731728,"$©!p!0 @%€L©a|\|u§":2399938,"Canuck":1783740,"Hisoka":271046,"Pray4Harambe":1935974,"joetay_us":315042,"Steve":2622856,"Counterpunch Hot Rod":2037640
    ,"Genghis Tron":896897,"Chosen of Hashut":5024075,"gomeso":2051818,"Soye de la tezeul":4324942,"Жулик":4090604}"""

matches_quantity = 600
request_and_plot(all_players=all_players)