import tweepy
import datetime
import time
import os


def appendrequests():
    global timing
    global text
    global reqpath
    g = open(reqpath, mode="r+", encoding="UTF-8")
    requests = g.readlines()
    todo = ""
    for o in range(2, len(text)):
        todo += "" + str(text[o])
    user = tweets[s].user.screen_name
    requested = str(timing) + ";" + todo + ";" + user
    print(requested, file=g)
    requests.append(requested)
    g.close()


path = os.getcwd().replace("\\", "/")
fpath = path + "/sended.txt"
reqpath = path + "/requests.txt"
endedpath = path + "/finishrequests.txt"
AK = ""
ASK = ""
AT = ""
ATS = ""
auth = tweepy.OAuthHandler(AK, ASK)
auth.set_access_token(AT, ATS)
while True:
    time.sleep(7)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweets = api.search(q="", count=50)
    f = open(fpath, mode="r+", encoding="UTF-8")
    replyed = f.readlines()
    since = max(replyed)
    print(since)
    kotosi = datetime.datetime.now().year
    kongetu = datetime.datetime.now().month
    kyou = datetime.datetime.now().day
    for s in range(len(tweets)):
        if int(tweets[s].id) <= int(since):
            pass
        else:
            text = tweets[s].text.rsplit("\n")
            if len(text) <= 2:
                reply = "@" + str(tweets[s].user.screen_name) + "時間か要件入れ忘れてない？？"
                api.update_status(status=reply, in_reply_to_status_id=tweets[s].id)
                print(tweets[s].id, file = f)
            else:
                try: #OK
                    timing = datetime.datetime.strptime(text[1], "%H:%M")
                    print(timing.time())
                    print(datetime.datetime.now().time())
                    if timing.time().hour*60+timing.time().minute - datetime.datetime.now().time().hour*60 - datetime.datetime.now().time().minute <= 0:
                        timing = str(timing)
                        if kyou+1 <= 10:
                            timing = timing.replace("1900", str(kotosi)).replace("-01-", "-"+str(kongetu)+"-").replace("-01", "-0"+str(kyou+1))
                        else:
                            timing = timing.replace("1900", str(kotosi)).replace("-01-", "-" + str(kongetu) + "-").replace("-01 " , "-"+str(kyou+1)+" ")
                    else:
                        timing = str(timing)
                        timing = timing.replace("1900", str(kotosi)).replace("-01-", "-"+str(kongetu)+"-").replace("-01", "-"+str(kyou))
                    appendrequests()
                    reply = "@" + str(tweets[s].user.screen_name) + " リマインダーのセットできたよ！" + str(datetime.datetime.now())
                    api.update_status(status=reply, in_reply_to_status_id=tweets[s].id)
                    print(tweets[s].id, file=f)
                except: #OK
                    y = -1
                    m = -1
                    d = -1
                    texted = text[1]
                    for b in range(len(texted)):
                        if texted[b] == "年":
                            y = b
                        elif texted[b] == "月":
                            m = b
                        elif texted[b] == "日":
                            d = b
                        else:
                            pass
                    if m-y == 2:
                        texted = texted.replace(texted[y+1:y+2]+"月","0"+texted[y+1:y+2]+"月")
                    else:
                        pass
                    if d-m == 2:
                        texted = texted.replace(texted[m+1:m+2]+"日","0"+texted[m+1:m+2]+"日")
                    else:
                        pass
                    try:
                        timing = datetime.datetime.strptime(texted, "%Y年%m月%d日 %H:%M")
                        appendrequests()
                        reply = "@" + str(tweets[s].user.screen_name) + " Y年のほうでリマインダーのセットできたよ！" +str(datetime.datetime.now())
                        api.update_status(status=reply, in_reply_to_status_id=tweets[s].id)
                        print(tweets[s].id, file=f)
                    except: # OK
                        try:
                            timing = datetime.datetime.strptime(texted, "%m月%d日 %H:%M")
                            timing = str(timing)
                            if int(timing[5:7]) < kongetu:
                                timing = timing.replace("1900", str(kotosi+1))
                            else:
                                timing = timing.replace("1900", str(kotosi))
                            appendrequests()
                            if int(timing[8:10]) < kyou:
                                timing = timing.replace("1900",str(kotosi+1))
                            else:
                                pass
                            reply = "@" + str(tweets[s].user.screen_name) + " m月始まりの方でリマインダーのセットできたよ！" + str(datetime.datetime.now())
                            api.update_status(status=reply, in_reply_to_status_id=tweets[s].id)
                            print(tweets[s].id, file=f)
                        except : #OK
                            try:
                                timing = datetime.datetime.strptime(texted, "%d日 %H:%M")
                                timing = str(timing)
                                print(int(timing[8:10]))
                                if int(timing[8:10]) < kyou:
                                    if kongetu +1 >12:
                                        timing = timing.replace("1900", str(kotosi+1))
                                    else:
                                        if kongetu+1 <10:
                                            timing = timing.replace("1900-01-", str(kotosi)+"-0"+str(kongetu+1)+"-")
                                        else:
                                            timing = timing.replace("1900-01-", str(kotosi)+"-"+str(kongetu+1)+"-")
                                else:
                                    if kongetu <= 10:
                                        timing = timing.replace("1900-01",str(kotosi)+"-"+"0"+str(kongetu))
                                    else:
                                        timing = timing.replace("1900-01" , str(kotosi)+"-"+str(kongetu))
                                appendrequests()
                                reply = "@" + str(tweets[s].user.screen_name) + " d日始まりの方でリマインダーのセットできたよ！" + str(datetime.datetime.now())
                                api.update_status(status=reply, in_reply_to_status_id=tweets[s].id)
                                print(tweets[s].id, file=f)
                            except:
                                now = datetime.datetime.now()
                                reply = "@" + str(tweets[s].user.screen_name) + "時間は" + now.strftime("%Y年%#m月%#d日 %H:%M") + "または" + now.strftime("%m月%#d日 %H:%M") + "または" + now.strftime("%#d日 %H:%M") + "または" + now.strftime("%H:%M") + "みたいに書いてね！"
                                api.update_status(status=reply, in_reply_to_status_id=tweets[s].id)
                                print(tweets[s].id, file=f)
    f.close()
    h = open(reqpath, mode="r+", encoding="UTF-8")
    karifile = h.readlines()
    h.close()
    x = open(endedpath, mode="r+", encoding="cp932")
    finished = x.readlines()
    accepted=[]
    checker=0
    print(karifile)
    for s in range(0, len(karifile)):
        for w in range(0, len(finished)):
            if karifile[s] == finished[w]:
                checker = 1
            else:
                pass
        print(checker)
        if checker == 0:
            accepted.append(karifile[s])
        else:
            pass
        checker=0
    for v in range(0,len(accepted)):
        kari = accepted[v].split(";")[0]
        times = datetime.datetime.strptime(kari, "%Y-%m-%d %H:%M:%S")
        if times - datetime.datetime.now() <= datetime.timedelta(0):
            reply = "@" + str(accepted[v].split(";")[2]) + " " + str(accepted[v].split(";")[1])+"の時間だよ！！"
            api.update_status(status=reply)
            print(accepted[v], file=x)
        else:
            pass
    x.close()