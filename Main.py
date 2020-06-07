  
import os
import __init__
import accupass
import datetime
import time
import String_process
import SQL_connect
import socket
import MySQLdb
import threading

def index():
    """做出還未結束活動的index表，依時間排序"""
    conn = MySQLdb.connect(host="db-testing.csvceebtmmcx.ap-northeast-1.rds.amazonaws.com", 
                       user="admin",
                       passwd="321password",
                       db="activity",
                       charset="utf8")
    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    query = "select activityID, activityType from ActivityMain where endDate >= \""+ date +"\" order by startDate;"
    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query)
    tuple_result = cursor.fetchall()
    #print(tuple_result)
    type_index_dic={"noType":[], "Learning":[], "Arts":[], 'CategoryEnum.Investm':[], 'Sports':[], 'Family':[], 'Health':[], 'Business':[], 
                    "Outdoor":[], "Other":[], 'CategoryEnum.Startup':[], 'Photography':[], 'CategoryEnum.Handmad':[],'CategoryEnum.Design':[]}
    for i in tuple_result:
        type_index_dic[i[1]].append(i[0]);
    #print(type_index_dic)
    return type_index_dic

def delete():
    """刪除過期的資料"""
    conn = MySQLdb.connect(host="db-testing.csvceebtmmcx.ap-northeast-1.rds.amazonaws.com", 
                       user="admin",
                       passwd="321password",
                       db="activity",
                       charset="utf8")
    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    query = "DELETE from ActivityMain where endDate < \""+ date +"\" ;"
    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query)
    tuple_result = cursor.fetchall()
    print(tuple_result)
    
def select_type_data( act_type, type_index_dic):
    """"""
    conn = MySQLdb.connect(host="db-testing.csvceebtmmcx.ap-northeast-1.rds.amazonaws.com", 
                       user="admin",
                       passwd="321password",
                       db="activity",
                       charset="utf8")
    
    total_result=[]
    calculate=0
    for i in type_index_dic[act_type]:
        if calculate==5: break    
        query = "select * from totalview where activityID = "+ i 
        # 執行查詢
        cursor = conn.cursor()
        cursor.execute(query)
        result = list(cursor.fetchall()[0])
        #print(result)
        #時間格式轉換
        result[7] = str((result[7].seconds//3600)%24) + ":" + str((result[7].seconds//60)%60) + ":" + str(result[7].seconds%60)
        result[8] = str((result[8].seconds//3600)%24) + ":" + str((result[8].seconds//60)%60) + ":" + str(result[8].seconds%60)
        #日期格式轉換
        result[9] = str(result[9].year) + "-" + str(result[9].month) + "-" + str(result[9].day)
        result[10] = str(result[10].year) + "-" + str(result[10].month) + "-" + str(result[10].day) 
        result[16] = str(result[16].year) + "-" + str(result[16].month) + "-" + str(result[16].day)
        result[17] = str(result[17].year) + "-" + str(result[17].month) + "-" + str(result[17].day)
        total_result.append(result)
        calculate+=1
    conn.close
    print(total_result)
    return total_result

def update():
    print("test")
    global global_type_index_dic
    while 1:
        timenow = datetime.datetime.now()
        date = " "
        #print(timenow)
        date = date + str(timenow.year) + "/" + str(timenow.month) + "/" + str(timenow.day)
        updatedata = timenow.hour
        #print(updatedata)
        #print(date)
        if updatedata == 23:
            print("start update")
            #__init__.taichanggov(date)
            accupass.accupassget()
            delete()
            global_type_index_dic=index()
            #SQL_connect.select('Address')
            #gg = locate.loc('卓越商務中心')
            #print(gg.get('latitude'))
            #print(gg.get('longitude'))
            #re = String_process.date_and_time("2020-06-13T14:00:00")
            #gg = String_process.address_where("台灣台中市台灣大道二段二號16樓之2")
            #print(gg)
            print("zzzzzzzzzz") 
        else:
            print("no update")
        time.sleep(3500)
     
global_type_index_dic=index()
total_col =  ("activityID", "addressID", "bookingID", "name", "activityType", "activityPicture", "activityURL",
              "opentime", "closeTime", "startDate", "endDate",
               "eastLongitude", "northLatitude", "city", "district",
               "bookingURL", "bookingStartDate", "bookingEndDate", "price")
threading1 = threading.Thread(target=update)
threading1.start()
HOST = ''   #ipv4
PORT = 8001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立soket物件
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((HOST, PORT)) 
server.listen(10) #允許幾個人同時進入
#type_index_dic=index()
while True:
    print("連線中")
    conn, addr = server.accept()
    print("連線人數+1")
    #print ("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))
    clientMessage = str(conn.recv(1024), encoding='utf-8')
    result = select_type_data( clientMessage, global_type_index_dic )    
    #print('Client message is:', clientMessage)
    print(result)
    #傳送有幾筆資料
    conn.sendall(str(len(result)).encode())
    #傳送所有欄位
    for colunm in total_col:
        conn.sendall(colunm.encode())
        time.sleep(0.1)
    #傳送所有data
    for datalist in result:
        for data in datalist:
            conn.sendall(str(data).encode())
    conn.close()
    
    time.sleep(1)
    break

#type_index_dic=index()
#print(global_type_index_dic["Arts"])
#select_type_data("Arts",global_type_index_dic)

"""
result = select_type_data( "Arts", global_type_index_dic )
print(result)
"""