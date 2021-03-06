#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, socket, random, string, time, logging, threading, ConfigParser
from time import gmtime, strftime
global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NoticeMsgOnChannelJoin, NoticeMsgOnChannelJoinOn, HighLight

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
counter = 0
def fetchSettings():
    config = ConfigParser.ConfigParser()
    config.read('configirc.ini')
    try:
        global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NoticeMsgOnChannelJoin, NoticeMsgOnChannelJoinOn, HighLight
        HOST = config.get('Server', 'Server')
        PORT = int(config.get('Server', 'Port'))
        CHAN = config.get('Server', 'Channel')

        NICK = config.get('Bot', 'Nick')
        IDENT = config.get('Bot', 'Ident')
        REALNAME = config.get('Bot', 'RealName')

        NoticeMsgOnChannelJoin = config.get('Messages', 'WelcomeMsg')
        NoticeMsgOnChannelJoinOn = config.get('Messages', 'WelcomeMsgActive')
        PING = config.get('Messages', 'OutputPing')
        HighLight = config.get('Messages', 'HighlightPhrases').split(',')

        TIMEOUTTIME = float(config.get('Settings', 'SocketDelay'))
        PLUGINFILE = config.get('Settings', 'PluginFile')
        TrueMaster = config.get('Settings', 'BotOwner')
        MASTERS = config.get('Settings', 'Masters').replace(' ', '').split(',')


    except:
            print "[!] Error have happened while fetching settings from configirc.ini!"
            sys.exit(1)
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def multi_detect(string, inputArray):
    for item in inputArray:
        if item in string:
            print '\a'
            return 1
    return 0

def print_date(msg, colour=YELLOW):
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + strftime("[*] [%H:%M:%S] ",gmtime()) + "\x1b[0m"
        print seq+msg
    else:
        print strftime("[*] [%H:%M:%S] "+msg, gmtime()) 

class Irc:
    def __init__(self):
        self.onChannelMsg = 'Sup cunts.'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lastHL = 'Null'
    def send(self, msg):
        self.socket.send(msg + "\r\n")
    def sendMsg(self, chan, msg):
        self.socket.send('PRIVMSG '+chan+' :'+msg+'\r\n')
        print_date('[%s] to <%s>: %s' % (NICK, chan, msg), colour=BLUE)

    def connect(self):
        #config_fetch()# just couldn't get it to work
        #logging section
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler('socket.log')
        self.formatter = logging.Formatter('[*] [%(asctime)s] %(message)s', datefmt='%H:%M:%S')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr) 
        self.logger.setLevel(logging.INFO)

        self.socket.connect((HOST, PORT))
        self.send("NICK %s" % NICK)
        self.send("USER %s %s bla :%s" % (IDENT, HOST, REALNAME))
        time.sleep(5)
        self.send("JOIN %s" % (CHAN))
        self.socket.settimeout(TIMEOUTTIME)
        time.sleep(2)
        self.send("PRIVMSG #polish :Joined. Hi.")
    def whileSection(self):
        while True:
            try:
                readbuffer = self.socket.recv(1024)
            except:
                readbuffer = ""
            temp = string.split(readbuffer, "\n")
            for line in temp:
                try:
                    if not line:
                        break
                    line = string.rstrip(line)
                    self.logger.info(str(line))
                    line = string.split(line)
                    if line[0] == "PING":
                        self.send("PONG %s" % line[1])
                        if PING:
                            print_date("Pinged and ponged.", colour=CYAN)
                        else:
                            pass
                    if line[1] == "PRIVMSG":
                        channel = line[2]
                        message = (' '.join(line[3:]))[1:]
                        username = (line[0].split('!')[0])[1:]
                        hld = multi_detect(message, HighLight)
                        if hld:
                            self.lastHL = username
                        colour = {0:YELLOW, 1:RED}[(hld == True) or (channel == TrueMaster)]
                        print_date("[%s] to <%s>: %s" % (username, channel, message), colour=colour)
                        execfile(PLUGINFILE)
                    elif line[1] == "JOIN":
                        username = (line[0].split('!')[0])[1:]
                        if NoticeMsgOnChannelJoinOn == 1:
                            self.send("NOTICE "+username+" :"+NoticeMsgOnChannelJoin)
                        print_date("[%s] joined the channel <%s>" % (username, ' '.join(line[2:])[1:]), colour=MAGENTA)
                    elif line[1] == "QUIT":
                        username = (line[0].split('!')[0])[1:]
                        print_date("[%s] has quit: %s" % (username, ' '.join(line[2:])[1:]), colour=MAGENTA)
                    elif line[1] == "PART":
                        username = (line[0].split('!')[0])[1:]
                        channel = line[2]
                        print_date("[%s] leaves from <%s>" % (username, channel), colour=MAGENTA)
                    else:
                        print ' '.join(line)
                except IndexError:
                    pass

fetchSettings()


