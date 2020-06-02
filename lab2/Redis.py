
import random

import redis
import logging
import threading
import time

from pip._vendor.distlib.compat import raw_input



def Check(message, name, forWhom):
    time.sleep(10)
    mes = message.split(" ")
    count = 0
    for word in mes:
        if isSpam(word):
            count += 1
    if count > 5:
        worker.base.zrem(name, message)
        worker.base.zadd(name, message, 3)
        worker.base.zincrby("spamers", name, 1)
    else:
        worker.base.zrem(name, message)
        worker.base.zadd(name, message, 2)
    worker.base.zadd(forWhom + '_get', message, 1.0)

def checkforspam(messages, name, forWhom):

    thread = threading.Thread(target=Check, args=(messages, name, forWhom))
    thread.start()

def Spam(message):
    list = worker.base.lrange('spam', 0, -1)
    for item in list:
        if message == str(item):
            return True
    return False

def simpleUsers(name):
    list = worker.base.smembers("Users")
    for names in list:
        if name == names:
            return True
    return False

def Admin(name):
    list = worker.base.smembers("Administrators")
    for names in list:
        if name == names:
            return True
    return False


class Worker:
    base = redis.Redis()

def Messagesinbox(name):
    messages = worker.base.zrange(name, 0, -1, withscores=True)
    for message in messages:
        print(message)

def GotMessages(name):
    messages = worker.base.zrange(name + '_get', 0, -1, withscores=True)
    for message in messages:
        print(message)

def ifOnline():
    print(worker.base.hgetall(online))

def Spamers():
    print(worker.base.zrange("spamers", 0, -1, withscores=True))

def emulate():
    i = 0
    while(i < 40):
        name1 = 'User'
        rand = random.uniform(0, 2)
        if int(rand) == 0:
            name1 = name1
        elif int(rand) == 1:
            name1 = name1 + '1'
        elif int(rand) == 2:
            name1 = name1 + '2'
        name2 = 'User'

        rand = random.uniform(0, 2)
        if int(rand) == 0:
            name2 = name2
        elif int(rand) == 1:
            name2 = name2 + '1'
        elif int(rand) == 2:
            name2 = name2 + '2'
        tag = tags[int(random.uniform(0, len(tags)))]

        worker.base.zadd(name1, 'Message ' + tag, 1.0)
        checkSpam('Message ' + tag, name1, name2)
        i = i + 1

worker = Worker()
worker.base.sadd("Admis", "Lider")
worker.base.sadd("Users", "User")
worker.base.sadd("Users", "User1")
worker.base.sadd("Users", "User2")



online = "online"

tags = ["#institute", '#db', '#session', '#mark', 'action']
pubsub = worker.base.pubsub()
for tag in tags:
    worker.base.lpush('spam', tag)
list = worker.base.lrange('spam', 0, -1)
print(list)
print("sign as: 1 - simple user, 2 - admin")
if(raw_input()) == "1":
    print("login")
    name = raw_input()
    if matchUsers(name):
       worker.base.hset(online, name, "true")
       print("welcome")
       while True:
            print("OPTIONS: 1 - MAIL, 2 - MAILS SENT, "
                  "3 - GOT Messages\n, 4 - sign for/out, 5 - publication, 6 - escape")
            choice = int(input())
            if choice == 1:
                print("YOUR MAIL: \n")
                messageSend = raw_input()
                print("Reciever: ")
                forWhom = raw_input()
                worker.base.zadd(name, messageSend, 1.0)
                checkSpam(messageSend, name, forWhom)
            if choice == 2:
                showMessages(name)
            if choice == 3:
                showGotMessages(name)
            if choice == 4:



                print("1 - sign, others - get publication")
                choice = int(input())
                if choice == 1:
                    print("login ")
                    pub = raw_input()
                    pubsub.subscribe(pub)
                else:
                    try:

                        print(pubsub.get_message()['data'])
                    except Exception:
                        print()


            if choice == 5:
                worker.base.publish(name
                                    , raw_input())
            if choice == 6:
                worker.base.hset(online, name, "false")
                break
else:
    print("ADMIN ")


    name = raw_input()
    if matchHead(name):
        print("Welcome")
        print("OPTIONS: 1 -isonline, 2 -ammount of spam, 3 - emulation")
        choice = int(raw_input())
        if choice == 1:
            showOnline()
        if choice == 2:
            showSpamers()
        if choice == 3:
            emulate()



