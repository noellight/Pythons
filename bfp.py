##########################
# brainfuck++ ver 1.0
# brainfuckインタプリタをPython上で実現し、更に拡張したものです。
# 従来のbfとの互換モードもあります。
# 標準的なbfの仕様は調べていただくとして、拡張したbrainfuckでは
# 1.メモリオーバーフローが事実上なくなる 2.;を使えば配列上の数字をそのまま出力可能 3.?で現在のポインタが指してる配列の値を格納 4.!で保存した値を復元(存在しない場合は0で初期化)
# といった仕様となっております。 また、最初のモード切替時にmemoryと入力することでbf実行完了時の配列を出力したり、あるいは無効化したりできます。
# 既存のbrainfuckバイナリとの互換性を維持(といってもこれを使う人間が何人いるのやら・・・)するために.bfファイルは互換モード、.bfpファイルは拡張bfを起動する仕様といたしました。
# 最後に・・・ちょっとでも遊んでくれると嬉しいですっ！！
##########################
#ファイルを開くか標準bfかbfpかをユーザーに決定してもらう関数
dir = ""
args = 0
def init():
    global args
    print("brainfuck++ ver.1.0")
    while True:
        global dir
        a=input("base:")
        if a[0:4] == "file":
            try:
                f = open(a[5:])
                Lines = f.read().replace("\n","")
                f.close()
                dir = a[5:]
                return Lines
            except:
                print("ファイルが存在しません。")
        elif a == "oldbf":
            return 0
        elif a == "bfp":
            return 1
        elif a == "exit":
            return 9
        elif a == "version":
            print("Brainfuck++ ver 1.0")
        elif a == "memory":
            if args == 0:
                print("メモリ出力を有効化")
                args = 1
            else:
                print("メモリ出力を無効化")
                args = 0
        else:
            print("正しくないコマンドです。")
#以下、標準bfと拡張bfの処理群をclassで定義、拡張bfについては
#親classを受け継いだ子classを作り、必要ならばメソッドの追加、及びオーバーライドで処理をしていく。
finished = False
class Motheroperands:
    landArray = [0]
    pointer = 0
    line = ""
    processed = 0
    loopstatus = 0
    current = ""
    def ArrayProcess(self): #互換モード時の配列のオーバーフロー(こちらも拡張モードでは無効化する)
        self.landArray[self.pointer] = self.landArray[self.pointer] % 256
    def IO(self): #入出力関数(後のbf拡張で書き換えるため分ける)
        if self.current == ".":
            print(chr(self.landArray[self.pointer]))
            self.processed += 1
            return 1
        elif self.current == ",":
            inp = input()
            self.landArray[self.pointer] = ord(inp[0])
            self.processed += 1
            return 1
        else:
            return 0
    def exe(self): #メモリのインクリメント、デクリメント、ポインタの移動を実行する。
        global finished
        if self.IO() == 0:
            if self.current == "+":
                self.landArray[self.pointer] += 1
                self.ArrayProcess()
                self.processed += 1
            elif self.current == "-":
                self.landArray[self.pointer] -= 1
                if self.landArray[self.pointer] < 0:
                    print("メモリの値が不正です！")
                    self.landArray[self.pointer] = 0
                    finished = True
                else:
                    self.ArrayProcess()
                    self.processed += 1
            elif self.current == "<":
                self.pointer -= 1
                self.processed += 1
            elif self.current == ">":
                self.pointer += 1
                self.processed += 1
                if self.pointer + 1 > len(self.landArray):
                    self.landArray.append(0)
            else:
                self.processed += 1
    def operateHandler(self): #場合によってパターン分けする関数。
        global finished
        if self.pointer < 0:
            print("ポインタが負の値を取りました！")
            finished = True
        else:
            try:
                if self.current == "[":
                    if self.landArray[self.pointer] !=0:
                        self.loop()
                    else:
                        print(self.current)
                        print(self.landArray[self.pointer])
                        while True: #ポインタが示す値が0だったとき、]の直後までジャンプするための処理
                            if self.line[self.processed] == "]":
                                self.processed += 1
                                self.current = self.line[self.processed]
                                break
                            else:
                                self.processed += 1
                else:
                    self.current = self.line[self.processed]
                    self.exe()
            except:
                finished = True
    def loop(self): #[]内の繰り返し処理
        global finished
        self.loopstatus = 1
        self.currentnow = self.processed
        while self.loopstatus == 1:
            self.current = self.line[self.processed]
            if self.line[self.processed] == "]":
                if self.landArray[self.pointer] != 0:
                    self.processed = self.currentnow
                    self.current = self.line[self.processed]
                    self.exe()
                else:
                    self.loopstatus = 0
                    self.processed += 1
            else:
                self.exe()
class Extend(Motheroperands): #拡張bfのclass、互換bfのclassに存在する一部メソッドをオーバーライドしている。
    backyardArray = [0]
    def ArrayProcess(self): #オーバーフローの無効化
        pass
    def IO(self): #入出力関数(bf拡張版)
        if self.current == ".":
            print(chr(self.landArray[self.pointer]))
            self.processed += 1
            return 1
        elif self.current == ",":
            inp = input()
            self.landArray[self.pointer] = ord(inp[0])
            self.processed += 1
            return 1
        elif self.current == "?": #メモリ内容のバックアップ
            if self.pointer + 1 > len(self.backyardArray):
                while self.pointer + 1 != len(self.backyardArray):
                    self.backyardArray.append(0)
                self.backyardArray[self.pointer] = self.landArray[self.pointer]
                self.processed += 1
                return 1
            else:
                print("ds")
                self.backyardArray[self.pointer] = self.landArray[self.pointer]
                print(self.backyardArray[self.pointer])
                self.processed += 1
                print(self.backyardArray)
                return 1
        elif self.current == ";": #メモリ上の数値をそのまま出力
            print(self.landArray[self.pointer])
            self.processed += 1
            return 1
        elif self.current == "!": #バックアップからの復元。バックアップがない場合は初期化する
            try:
                self.landArray[self.pointer] = self.backyardArray[self.pointer]
                self.processed += 1
                return 1
            except:
                self.landArray[self.pointer] = 0
                self.processed += 1
                return 1
        else:
            return 0
first = init() #ユーザーからの選択を待つ
if first == 0:
    cmd = input("brainfuck:")
    boot = Motheroperands()
    boot.line = cmd
    while finished == False:
        boot.operateHandler()
elif first == 1:
    cmd = input("brainfuck++:")
    boot = Extend()
    boot.line = cmd
    while finished == False:
        boot.operateHandler()
elif first == 9:
    pass
else:
    if dir[len(dir)-3:] == ".bf":
        boot = Motheroperands()
        boot.line = first
        while finished == False:
            boot.operateHandler()
    elif dir[len(dir) -4:] == ".bfp":
        boot = Extend()
        boot.line = first
        while finished == False:
            boot.operateHandler()
    else:
        print("ファイルエラー！")
if args == 1:
    print(boot.landArray)