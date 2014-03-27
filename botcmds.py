if counter == 0:
    self.sendMsg(CHAN, "Loaded "+PLUGINFILE)
    counter += 1
else:
    pass
if message[0] == '!':
    commandMsg = (message.split(' ')[0])
    argMsg = (message.split(' ')[1:])
    argMsg2 = (message.split(' ')[1])

    if(commandMsg == "!test" and username in MASTERS):
        self.sendMsg(CHAN, "testing")

    elif(commandMsg == "!roll" and argMsg2 == "big" and username in MASTERS):
        x1 = int(strftime("%S", gmtime()))
        x2 = int(strftime("%Y", gmtime()))
        x = random.randint(1, x1*x2)
        self.sendMsg(CHAN, "Rolled "+str(x))

    elif(commandMsg == "!roll" and argMsg2 == "small" and username in MASTERS):
        x1 = int(strftime("%S", gmtime()))
        x = random.randint(1, x1)
        self.sendMsg(CHAN, "Rolled "+str(x))

    elif(commandMsg == "!kick" or commandMsg == "!kill" and username in MASTERS):
        sayMsg = ' '.join(argMsg)
        self.send("KICK "+CHAN+" "+sayMsg)

    elif(commandMsg == "!mode" and username == TrueMaster):
        self.send("MODE "+CHAN+" "+argMsg)

    elif(commandMsg == "!say" and username in MASTERS):
        sayMsg = ' '.join(argMsg)
        self.sendMsg(CHAN, sayMsg)

    elif(commandMsg == "!losujhelp"):
        self.sendMsg(CHAN, "Usage !losuj <1stitem>, <2nditem>...")
        self.sendMsg(CHAN, "Do not put space at end of the !losuj")

    elif(commandMsg == "!losuj"):
        sayMsg = ' '.join(argMsg)
        y = random.choice(sayMsg.split(','))
        self.sendMsg(CHAN, y)

    elif(commandMsg == "!exec" and username == TrueMaster):
        sayMsg = ' '.join(argMsg)
        if sayMsg == "sys.exit()":
            self.sendMsg(CHAN, "Bye")
            pass
        else:
            pass
        exec(sayMsg)
    else:
        pass
