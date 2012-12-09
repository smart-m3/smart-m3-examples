from smart_m3.m3_kp import *
import time
import sys

# Create a node instance
# Programmer can give any name 
# The infrastucture will assign unique names
node = KP("SS_HelloWorld_creator_observer")

# Connect to the selected smart space
# In this simple example we use localhost

#ss_handle = ("X", (Node.TCPConnector, ("127.0.0.1", 10011)))

ss_handle = node.discover()

print ss_handle
try:
    node.join(ss_handle)
except M3Exception:
    sys.exit('Could not join to Smart Space')

print "--- Member of SS:", node.member_of

# end connecting 

# Define the triples and commonly used URIs
SPACE_URI = URI("Space")
HAS_URI = URI("has")
InformationAboutActions = [Triple(SPACE_URI,HAS_URI,Literal("light")),
                           Triple(SPACE_URI,HAS_URI,Literal("land")),
                           Triple(SPACE_URI,HAS_URI,Literal("animals")),
                           Triple(SPACE_URI,HAS_URI,Literal("stars")),
                           Triple(SPACE_URI,HAS_URI,Literal("man_and_woman")),
                           Triple(SPACE_URI,HAS_URI,Literal("sky")),
                           Triple(SPACE_URI,HAS_URI,Literal("moon")),
                           Triple(SPACE_URI,HAS_URI,Literal("sea")),
                           Triple(SPACE_URI,HAS_URI,Literal("sun"))]

# Create Insert transaction with the
# smart space

pro = node.CreateInsertTransaction(ss_handle)
print "Starting insert"

# Insert
# Could also insert the whole list at once
for i in InformationAboutActions:
    try:
        pro.send(i, confirm = True)
    except M3Exception:
        sys.exit("Insert failed, exiting.")
    print "%s appeared!"%str(i[2])
    time.sleep(0.5)
node.CloseInsertTransaction(pro)

time.sleep(2)

rem = node.CreateRemoveTransaction(ss_handle)
try:
    rem.remove(Triple(SPACE_URI, HAS_URI,Literal("stars")))
except M3Exception:
    sys.exit('Remove failed, exiting.')
node.CloseRemoveTransaction(rem)
print "Stars have been removed"

time.sleep(2)

pro = node.CreateInsertTransaction(ss_handle)
try:
    pro.send(Triple(SPACE_URI, HAS_URI, Literal("stars")))
except M3Exception:
    sys.exit('Insert failed, exiting.')
node.CloseInsertTransaction(pro)
print "Stars have appeared again"

# Disconnect from the smart space
# The information is not removed from the smart space
node.leave(ss_handle)
sys.exit()
