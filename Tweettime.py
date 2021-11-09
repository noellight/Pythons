import tweepy
import datetime
import time

try:
    f = open(file="last_fetched_status.txt",mode="r",encoding="UTF-8")
    executed = int(f.readline())
    f.close()
except Exception as e:
    print(e)
    f=open(file="last_fetched_status.txt",mode="w",encoding="UTF-8")
    executed = 99999999
    print(9999999,file=f)
    f.close()
AK = ""
ASK = ""
AT = ""
ATS = ""
auth = tweepy.OAuthHandler(AK, ASK)
auth.set_access_token(AT, ATS)
ex_Arr = []
print(executed)
while True:
    time.sleep(15)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweets = api.mentions_timeline(since_id=executed)
    print(tweets)
    for x in tweets:
        try:
            if "checktime" in x.text:
                print("Yes")
                print(type(x.in_reply_to_status_id))
                if str(type(x.in_reply_to_status_id)) == "<class 'int'>":
                    print(x.in_reply_to_status_id)
                    id = x.in_reply_to_status_id
                    id = id >> 22
                    id += 1288834974657
                    id /= 1000
                    id = datetime.datetime.fromtimestamp(id)
                    api.update_status(status="@"+x.user.screen_name+"\nツイート時刻:"+str(id),in_reply_to_status_id=x.id)
                    ex_Arr.append(x.id)
            else:
                print("No")
        except tweepy.error.TweepError as e:
            api.update_status(status="@ 【tweettime_debuger】Warning:"+e.reason+str(datetime.datetime.now()))
            ex_Arr.append(x.id)
    try:
        s = max(ex_Arr)
        print(s)
        f = open(file="last_fetched_status.txt",mode="w",encoding="UTF-8")
        print(s,file=f)
        f.close()
        executed = s
        ex_Arr = []
    except ValueError:
        pass
    except tweepy.error.TweepError as e:
        api.update_status(status="@【tweettime_debuger】Warning:"+e.reason+str(datetime.datetime.now()))
