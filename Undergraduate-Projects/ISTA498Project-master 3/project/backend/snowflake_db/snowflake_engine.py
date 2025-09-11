from datetime import datetime
from time import time
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.insert(0, '../')
from tutorial.tutorial import Tutorial
import schedule



SNOWFLAKE_USER = os.environ.get("SNOWFLAKE_USER")
SNOWFLAKE_PASSORD= os.environ.get("SNOWFLAKE_PASSORD")
SNOWFLAKE_ACCOUNT= os.environ.get("SNOWFLAKE_ACCOUNT")

ctx = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSORD,
    account=SNOWFLAKE_ACCOUNT
)

def insert_user(id,password):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    if 'test' not in id:
        cs.execute('''INSERT INTO "NUSKILL"."NUSKILL_MASTER"."USER_DATA"(USER_ID,HASHED_PASSWORD, TOTAL_DEPOSITED, CURRENT_BALANCE)
                        VALUES(\''''+str(id)+"','"+ str(password)+ "','"+ str(0)+ "','"+ str(0)+ "');")
    else:
        cs.execute('''INSERT INTO "NUSKILL"."NUSKILL_MASTER"."USER_DATA"(USER_ID,HASHED_PASSWORD, TOTAL_DEPOSITED, CURRENT_BALANCE)
                        VALUES(\''''+str(id)+"','"+ str(password)+ "','"+ str(0)+ "','"+ str(200)+ "');")
def get_user(id):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''SELECT * FROM "NUSKILL"."NUSKILL_MASTER"."USER_DATA" WHERE USER_ID =\'''' + str(id) + "';")
 
    cs.get_results_from_sfqid(cs.sfqid)
    try:
        results=cs.fetchall() 
    except:
        results=[]
    return results

def get_user_password(id):
    res = get_user(id)
    print(res)

    res = res[0]
    password = res[1]
    print(password)
    return password

def get_user_balance(id):
    res = get_user(id)
    res = res[0]
    user_id, password, total_deposited, current_balance = res
    return current_balance


  
        
def insert_user_deposited(id,amt):
    amt = float(amt)
    if amt <= 5.00 and  amt > 0.00:
        checks = 5
    elif amt <= 10.00:
        checks = 11
    elif amt <= 20.00:
        checks = 24
    elif amt <= 50.00:
        checks = 52
    elif amt <= 100.00:
        checks = 112
    
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''INSERT INTO "NUSKILL"."NUSKILL_MASTER"."DAILY_DEPOSITED"(USER_ID,AMT,AMT_EARNED_BACK,TOTAL_CHECKS_ALLWD)
                        VALUES(\''''+id+"','"+ str(amt)+ "','0','"+ str(checks)+"');")


        
def get_user_deposited(id=None):
    print(id)
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    if id:
        cs.execute('''SELECT * FROM "NUSKILL"."NUSKILL_MASTER"."DAILY_DEPOSITED" WHERE USER_ID =\'''' + id + "';")
    else:
        cs.execute('''SELECT * FROM "NUSKILL"."NUSKILL_MASTER"."DAILY_DEPOSITED";''')
        
    cs.get_results_from_sfqid(cs.sfqid)
    results=cs.fetchall() 
    return(results)
 
def insert_video_to_genre(genre, vid):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    videos = get_genre_videos(genre)
    videos.append(vid)
    videos = str(videos).replace('[','').replace(']','')
    print(videos)
    cs.execute('''UPDATE "NUSKILL"."NUSKILL_MASTER"."GENRE_VIDEOS" SET VID_LIST = ARRAY_CONSTRUCT(''' + videos +") WHERE GENRE = '" +genre +"';")
    
def insert_genre(genre, list_string=''):
    genre_map = get_genre_map()
    if genre in genre_map.keys():
        return 'Genre exists'
    else:
        cs = ctx.cursor()
        cs.execute('USE DATABASE "NUSKILL";')
        cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
        cs.execute('''INSERT INTO
                        "NUSKILL"."NUSKILL_MASTER"."GENRE_VIDEOS"(GENRE,VID_LIST)
                        SELECT $1, ARRAY_CONSTRUCT('''+list_string+''') FROM VALUES ''' + "('"+genre+"');")
        
def get_genre_map():
    genre_map = {}
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''SELECT GENRE FROM
                    "NUSKILL"."NUSKILL_MASTER"."GENRE_VIDEOS";''') 
    cs.get_results_from_sfqid(cs.sfqid)
    results=cs.fetchall() 
    for genre in results:
        curr_genre = genre[0]
        genre_map[curr_genre] = get_genre_videos(curr_genre)     
    return genre_map

def get_genre_videos(genre):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''SELECT VID_LIST FROM
                    "NUSKILL"."NUSKILL_MASTER"."GENRE_VIDEOS" WHERE GENRE = \'''' +genre +"';") 
    cs.get_results_from_sfqid(cs.sfqid)
    try:
        results=cs.fetchall() 
        data =  results[0]
        urls = data[0].replace('\n','')
        urls = urls.replace(' ','')
        urls = urls.replace('"','')
        urls = urls[1:-1]
        urls = urls.split(',')
        return(urls)
    except:
        results=[]
        return results
    
def insert_new_video(name,url,checks,series,genre):
    insert_genre(genre)
    insert_video_to_genre(genre=genre,vid=url)
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''INSERT INTO
                    "NUSKILL"."NUSKILL_MASTER"."VIDEO_OBJECTS"(NAME,URL, CHECKS, SERIES, GENRE)
                    ''' + "VALUES('"+ name+"','"+ url+"','"+ str(checks)+"','"+ str(series)+"','"+ genre + "');")
    
def get_video_object(url):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''SELECT * FROM "NUSKILL"."NUSKILL_MASTER"."VIDEO_OBJECTS" WHERE URL =\'''' + str(url) + "';")
    cs.get_results_from_sfqid(cs.sfqid)
    results=cs.fetchall() 
    name,url,checks,series,genre = results[0]
    return Tutorial(name,url,int(checks),series,genre)

def add_user_video_status(user_obj,url, genre):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''INSERT INTO
                    "NUSKILL"."NUSKILL_MASTER"."USER_VIDEO_STATUS"(ID,URL, GENRE IN_PROGRESS, COMPLETED)
                    ''' + "VALUES('"+ str(user_obj.getWalletId())+"','"+ url+"','"+ "','"+ genre+"','"+str(True)+"','"+ str(False)+ "');")
    
def update_user_video_status_completed(user_obj,url):
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('''UPDATE
                    "NUSKILL"."NUSKILL_MASTER"."USER_VIDEO_STATUS"
                    ''' + "SET IN_PROGRESS = 'FALSE', COMPLETED = 'TRUE' WHERE ID ='"+ str(user_obj)+"' AND URL= '"+ url+"';")
    
def delete_daily_deposited():
    cs = ctx.cursor()
    cs.execute('USE DATABASE "NUSKILL";')
    cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
    cs.execute('DELETE FROM "NUSKILL"."NUSKILL_MASTER"."DAILY_DEPOSITED"')

# schedule.every().day.at("00:00").do(delete_daily_deposited) 
# cs = ctx.cursor()
# cs.execute('USE DATABASE "NUSKILL";')
# cs.execute('USE WAREHOUSE "ISTA498WAREHOUSE";')
# cs.execute('DELETE FROM "NUSKILL"."NUSKILL_MASTER"."GENRE_VIDEOS"')
# cs.execute('DELETE FROM "NUSKILL"."NUSKILL_MASTER"."VIDEO_OBJECTS"')

# print(insert_genre('Snapchat'))
# print(insert_genre('Dog Training'))
# print(insert_genre('Sports Betting'))
# print(insert_genre('Something1'))
# print(insert_genre('Something2'))
# insert_video_to_genre('Snapchat','https://youtu.be/FD4hqhlc3Aw')
# insert_new_video('Snapchat 1','https://youtu.be/FD4hqhlc3Aw',5,True,'Snapchat')
# insert_video_to_genre('Snapchat','https://youtu.be/9-NDblKPNfg')
# insert_new_video('Snapchat 2','https://youtu.be/9-NDblKPNfg',5,True,'Snapchat')
# insert_video_to_genre('Snapchat','https://youtu.be/xFdu-WDfEPk')
# insert_new_video('Snapchat 3','https://youtu.be/xFdu-WDfEPk',5,True,'Snapchat')
# insert_video_to_genre('Snapchat','https://youtu.be/fM433qZ5iic')
# insert_new_video('Snapchat 4','https://youtu.be/fM433qZ5iic',5,True,'Snapchat')
# insert_video_to_genre('Snapchat','https://youtu.be/sQWN_MW5g5E')
# insert_new_video('Snapchat 5','https://youtu.be/sQWN_MW5g5E',5,True,'Snapchat')
# insert_video_to_genre('Snapchat','https://youtu.be/FD4hqhlc3Aw')
# insert_new_video('Dog Training 1','https://youtu.be/f_X-0VJJUL8',5,True,'Dog Training')
# insert_video_to_genre('Dog Training','https://youtu.be/f_X-0VJJUL8')
# insert_new_video('Dog Training 2','https://youtu.be/ng58pNPDDW4',5,True,'Dog Training')
# insert_video_to_genre('Dog Training','https://youtu.be/ng58pNPDDW4')
# insert_new_video('Dog Training 3','https://youtu.be/EBoJym_wQ2M',5,True,'Dog Training')
# insert_video_to_genre('Dog Training','https://youtu.be/EBoJym_wQ2M')
# insert_new_video('Dog Training 4','https://youtu.be/6WgALg1jajY',5,True,'Dog Training')
# insert_video_to_genre('Dog Training','https://youtu.be/6WgALg1jajY')
# insert_new_video('Dog Training 5','https://youtu.be/2A1ezr0is_c',5,True,'Dog Training')
# insert_video_to_genre('Dog Training','https://youtu.be/2A1ezr0is_c')

# print(get_genre_videos('Dog Training 6'))
#print(get_genre_map())
# insert_video_to_genre('Dog Training 6','https://www.76765bgtw9')
# insert_new_video('TEST VIDEO 1','https://www.youtube.com/watch?v=dQw4w9WgXcQ',4,False,'Dog Training 6')
# insert_new_video('TEST VIDEO 2','https://www.youtube.com/watch?v=dQw5636dbsdWgXcQ',6,False,'Beauty Tutorial')
#print(get_video_object('https://www.youtube.com/watch?v=dQw5636dbsdWgXcQ'))
#update_user_video_status_completed('239040242','youtube.com/324234efwe')
#delete_daily_deposited()

#add_user_video_status('83597304509843','youtube.com/watch?480u5903u543', 'Dog Training')
#insert vid/genre to user

