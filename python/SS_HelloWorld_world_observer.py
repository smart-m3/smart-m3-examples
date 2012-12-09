from smart_m3.m3_kp import *
import time
import sys


# Create a node instance
# Programmer can give any name 
# The infrastucture will assign unique names
node = KP("HelloWorld_world_observer")

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

# Class structure to be called when we receive subscription ind
SPACE_IS_WORLD_TRIPLE = Triple(URI('Space'), URI('isA'), Literal('World'))
class MsgHandler:
    def __init__(self):
        self.results = []
    def handle(self, added, removed):
        if SPACE_IS_WORLD_TRIPLE in added:
            print "Hello World!"
        elif SPACE_IS_WORLD_TRIPLE in removed:
            print "Hasta la vista World!"

# Create a subscription in smart space


rs = node.CreateSubscribeTransaction(ss_handle)
result = rs.subscribe_rdf(SPACE_IS_WORLD_TRIPLE, MsgHandler())


if result != []:
    print "It seems that the world has already been created"
    print "Hello World!"
else:
    print "Waiting for the world to be created"
    
inp = raw_input("Press any key if you are bored to wait\n")
rs.close()
node.CloseSubscribeTransaction(rs)
print "Unsubscribed"
node.leave(ss_handle)
sys.exit()
