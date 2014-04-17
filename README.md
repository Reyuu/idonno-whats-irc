##iWi framework   

**Created by Reyuu and maciej01.**    

No screenshot ATM.

Clients bulid on iWi:
* [iWi GUI](https://github.com/Reyuu/iwi-gui)
* [iWi CLI](https://github.com/Reyuu/iwi-cli)

###Commands:
| Command | Parameters  | Description |
| :------------: |:---------------:| :-----:|
| :j | [channel] | joins a specified channel |
| :q |  | quits the client |
| :ch | [channel] | changes the default output channel to a specified one|
|:l|[message]|sends the previous message, the parameter appends something to end - **optional param**|
|:p|[user/channel]|sends a private message to specified user or channel|
|:r|[raw data]|sends raw data to server, for ex. PRIVMSG #channel :hi|
|:ms|[id] [message]|predefinies a message to use later|
|:md|[id]|sends an already definied (by :ms) message|
|:vs|[variable] [content]|definies a variable to use later [without $ before variable]|
|:v|[message]|sends a message, but with variables replaced to their values [with $ before variables]|

###Predefinied variables:     
| Variable | Description |
| :------: | :---------: |
| $hl | last user that higlighted you |
| $lm | last message you sent|

###Requirements:    
* Python 2.7 - get it from [the official python website](https://www.python.org/download/releases/2.7.6/)

#Enjoy!
