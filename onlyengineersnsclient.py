import requests
def tweet(text): #動作確認完了
    print("自分で書いてね！")
def fetchtext():
    r = requests.get("https://versatileapi.herokuapp.com/api/text/all?$orderby=_created_at desc&$limit=20",headers={"content-type":"applications/json"}).json()
    for x in range(0,len(r)):
        try:
            if r[x]['_user_id'] != "d9ecf9245defb6b07cb86fe92a6fde9e735fc9f9":
                print(r[x]['_user_id'])
                print(r[x]['id'])
                print(r[x]['text'])
                toreply = r[x]['in_reply_to_text_id']
                for k in range(-len(r)+1,0):
                    if r[-k]['id'] == toreply:
                        print("リプライ先:")
                        print("     " + r[-k]['_user_id'])
                        for j in range(0,len(r[-k]['text'].split("\n"))):
                            print("     "+ r[-k]['text'].split("\n")[j])
                        break
        except:
            pass
while True:
    a = input()
    if a == "tweet":
        tweet(input("テキストを送信:"))

    elif a == "sync":
        fetchtext()
    else:
        print("コマンドが違います")