from smart_m3.m3_kp import *
import time
import sys

CREATED = False

# Create a node instance
# Programmer can give any name 
# The infrastucture will assign unique names

node = KP("HelloWorld_aggregator")

# Discover Smart Spaces around you

ss_handle = node.discover()

# Connect to the selected smart space
# In this simple example we use localhost
#ss_handle = ("X", (Node.TCPConnector, ("127.0.0.1", 10011)))

print ss_handle

try:
    node.join(ss_handle)
except M3Exception:
    sys.exit('Could not join to Smart Space')

print "--- Member of SS:", node.member_of

# end connect

WorldCheckList = {"light":0, "sky":0, "land":0, "sea":0, "sun":0, "moon":0,
                  "stars":0, "animals":0, "man_and_woman":0} 

ConclusionAboutGodsAction = [Triple(URI("Space"),
                                    URI("isA"),
                                    Literal("World"))]

# Artificial intelligence to determine if the world exist in the smart space
# Jewish & Christian approach

def DoesWorldExist(WorldCheckList):
    global CREATED
    temp = 0
    temp = sum(WorldCheckList.values())
    if temp == 9:
        CREATED = True
        pro = node.CreateInsertTransaction(ss_handle)
        try:
            pro.send(ConclusionAboutGodsAction, confirm = True)
        except M3Exception:
            sys.exit("Insert failed")

        node.CloseInsertTransaction(pro)

    elif CREATED:
        CREATED = False
        rem = node.CreateRemoveTransaction(ss_handle)
        try:
            rem.remove(ConclusionAboutGodsAction, confirm = True)
        except M3Exception:
            sys.exit("Remove failed")

        node.CloseRemoveTransaction(rem)

        
# Class structure to be called when we receive a subscription indication
class MsgHandler:
    def __init__(self):
        self.results = []
    def handle(self, added, removed):
        for i in added:
           if str(i[2]) in WorldCheckList:
               WorldCheckList[str(i[2])] = 1
           else:
               continue
        for i in removed:
           if str(i[2]) in WorldCheckList:
               WorldCheckList[str(i[2])] = 0
           else:
               continue
        DoesWorldExist(WorldCheckList)


# Subscribe to all triples (Space, has, *) in the smart space

rs = node.CreateSubscribeTransaction(ss_handle)
result = rs.subscribe_rdf([Triple(URI('Space'), URI('has'), None)], 
                          MsgHandler())
if result != []:
    print "State of the space:", result
    for i in result:
        if str(i[2]) in WorldCheckList:
            WorldCheckList[str(i[2])]=1
        else:
            continue
    DoesWorldExist(WorldCheckList)
   
    
inp = raw_input("Press any key if you are bored to wait\n")

print "Unsubscribing..."
rs.close()
node.CloseSubscribeTransaction(rs)

print "Leaving"
node.leave(ss_handle)
sys.exit()
