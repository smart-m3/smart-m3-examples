from smart_m3 import Node
import random
import sys
import time
import uuid



try:
    Node.CURRENT_TR_ID = int(sys.argv[1])
except:
    print "Usage: python stress_test_sub.py X"
    print "Where X is the number where transaction id generation should start"
    sys.exit()

ss_handle = ("X", (Node.TCPConnector, ("127.0.0.1",10010)))

node = Node.ParticipantNode("SubTester")

if not node.join(ss_handle):
    sys.exit('Could not join to Smart Space')

class RdfMsgHandler:
    def handle(self, added, removed):
        print "Subscription:"
        for i in added:
            print "Added:", str(i)
        for i in removed:
            print "Removed:", str(i)

class NodeMsgHandler:
    def handle(self, added, removed):
        print "Subscription:"
        for i in added:
            print "Added: value", str(i)
        for i in removed:
            print "Removed: value", str(i)

rs1 = node.CreateSubscribeTransaction(ss_handle)
result_rdf = rs1.subscribe_rdf([((None, 'value', None), 'uri')], RdfMsgHandler())

rs2 = node.CreateSubscribeTransaction(ss_handle)
result_wql = rs2.subscribe_wql_values(('GeneratedValue', False), ['inv', 'rdf:type',['seq', 'value']], NodeMsgHandler(), True)

print "Got RDF subscribe initial result"#, result_rdf
print "Got WQL values subscribe initial result"#, result_wql

for i in xrange(10):
    time.sleep(2)
    node.CloseSubscribeTransaction(rs1)
    rs1 = node.CreateSubscribeTransaction(ss_handle)
    result_rdf = rs1.subscribe_rdf([((None, 'value', None), 'uri')], RdfMsgHandler())
    print "Got RDF subscribe initial result" #, result_rdf

    time.sleep(2)
    node.CloseSubscribeTransaction(rs2)
    rs2 = node.CreateSubscribeTransaction(ss_handle)
    result_wql = rs2.subscribe_wql_values(('GeneratedValue', False), ['inv', 'rdf:type',['seq', 'value']], NodeMsgHandler(), True)
    print "Got WQL values subscribe initial result" #, result_wql
    

node.CloseSubscribeTransaction(rs1)
node.CloseSubscribeTransaction(rs2)
node.leave(ss_handle)
