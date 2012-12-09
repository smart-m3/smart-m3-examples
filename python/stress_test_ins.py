from smart_m3.m3_kp import *
import random
import sys
import time
import uuid

ss = ("X", (TCPConnector, ("127.0.0.1",10010)))

ERR_COUNTER = 0

# URI = node.URI
# Literal = node.Literal
# bNode = node.bNode
# Triple = triple.Triple

try:
    CURRENT_TR_ID = int(sys.argv[1])
except:
    print "Usage: python stress_test_ins.py X"
    print "Where X is the number where transaction id generation should start"
    sys.exit()

node = KP("InsertTester")

node.join(ss)

ps = node.CreateInsertTransaction(ss)
rs = node.CreateRemoveTransaction(ss)
query_list = []
ont = [Triple(URI('GeneratedValue'), 
              URI('rdfs:subClassOf'), 
              URI('DummyValue'))]

try:
    ps.send(ont)
except M3Exception:
    print "Sending ontology failed, exiting"
    sys.exit()

rdf_type = URI('rdf:type')
value_prop = URI('value')
gen_value_t = URI('GeneratedValue')

for i in xrange(100):
    triple_list = []
    for j in xrange(4):
        subj = URI(str(uuid.uuid1()))
        triple_list.append(Triple(subj, value_prop,
                                  Literal('o%s'%str(random.randint(1,100000)))))
        triple_list.append(Triple(subj, rdf_type, gen_value_t))
    # Append the third generated triple for querying
    query_list.append(triple_list[2])
    try:
        ps.send(triple_list)
        print "Sent 8 triples"
    except M3Exception:
        print "Sending generated triples failed"
        ERR_COUNTER += 1
        if ERR_COUNTER > 10:
            print "Too many errors, exiting"
            sys.exit()
    try:
        rs.remove([triple_list[0]])
        print "Removed triple %s"%str(triple_list[0])
    except M3Exception:
        print "Removing triple %s failed"%str(triple_list[0])
        ERR_COUNTER += 1
        if ERR_COUNTER > 10:
            print "Too many errors, exiting"
            sys.exit()
    try:
        rs.remove([triple_list[1]])
        print "Removed triple %s"%str(triple_list[1])
    except M3Exception:
        print "Removing triple %s failed"%str(triple_list[1])
        ERR_COUNTER += 1
        if ERR_COUNTER > 10:
            print "Too many errors, exiting"
            sys.exit()
print "Inserted all triples, now querying."

qt = node.CreateQueryTransaction(ss)
try:
    instances = qt.wql_values_query(gen_value_t, ['inv', str(rdf_type)])
    print "All instances of GeneratedValue:"
    print instances
except M3Exception:
    print 'Querying for instances of GeneratedValue failed'
    ERR_COUNTER += 1
    if ERR_COUNTER > 10:
        print "Too many errors, exiting"
        sys.exit()

type_path = ['seq', str(rdf_type), ['rep*', 'rdfs:subClassOf']]

for i in instances:
    try:
        print "Types of node %s are %s"%(i, qt.wql_values_query(i, type_path))
        print
    except M3Exception:
        print 'Querying for types of GeneratedValue instance %s failed'%i
        ERR_COUNTER += 1
        if ERR_COUNTER > 10:
            print "Too many errors, exiting"
            sys.exit()
   
result = []
for q in query_list:
    try:
        result.extend(qt.rdf_query(q))
    except M3Exception:
        print 'Querying for triple %s failed'%q
        ERR_COUNTER += 1
        if ERR_COUNTER > 10:
            print "Too many errors, exiting"
            sys.exit()
    

n = 1
for i in result:
    print "Triple found:", i, n
    n = n + 1


