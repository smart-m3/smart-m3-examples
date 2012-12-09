# coding: utf-8
from smart_m3.m3_kp import *
# from pyrple import Node, URI, Literal, bNode, Triple
import time
import sys

# Create a node instance
# One can also subclass ParticipantNode
# Constructor argument: String representing node id
# Node id can be anything, not restricted by the system

# URI = node.URI
# Literal = node.Literal
# bNode = node.bNode
# Triple = triple.Triple

node = KP("SIB Tester")
# ss_handle = node.discover(method = "mDNS")
ss_handle = node.discover()
print ss_handle

if not node.join(ss_handle):
    sys.exit('Could not join to Smart Space')

print "--- Member of SS:", node.member_of

class RdfMsgHandler:
    def handle(self, added, removed):
        print "Subscription:"
        for i in added:
            print "Added:", i
        for i in removed:
            print "Removed:", i

class NodeMsgHandler:
    def handle(self, added, removed):
        print "Subscription:"
        for i in added:
            print "Added: x1 drinks", i
        for i in removed:
            print "Removed: x1 drinks", i

# Create a proactive (sending) session with the
# smart space



# Put information to smart space using the session
# created earlier
# Parameters: string containing the information
#             string containing the information type
# Information and type can be any string, they are
# not restricted by the system
# 


def convert(triples):
    tl = []
    for t in triples:
        tr, stype, otype = t
        _s, _p, _o = tr
        if stype.lower() == "uri":
            s = URI(_s)
        elif stype.lower() == "literal":
            s = Literal(_s)
        else:
            s = bNode(_s)
        p = URI(_p)
        if otype.lower() == "uri":
            o = URI(_o)
        else:
            o = Literal(_o)
        tl.append(Triple(s, p, o))
    return tl

_init_triples = [(("x1", "rdf:type", "person"), "uri", "uri"),
                (("x1", "lives", "Espoo"), "uri", "literal"),
                (("x1", "name", "Timo"), "uri", "literal"),
                (("x1", "knows", "x2"), "uri", "uri"),
                (("x2", "rdf:type", "person"), "uri", "uri"), 
                (("x2", "lives", "Espoo"), "uri", "literal"),
                (("x2", "name", "Risto"), "uri", "literal"),
                (("person","rdfs:subClassOf","thing"), "uri", "uri")]
_insert = [(("x1", "drinks", "beer"), "uri", "literal")]
_update_rem = [(("x1", "drinks", "beer"), "uri", "literal")]
_update_ins = [(("x1", "drinks", "water"), "uri", "literal")]

bNode_triples = [Triple(bNode('1'), URI('drinks'), Literal('water')),
                 Triple(bNode('1'), URI('lives'), Literal('Vantaa'))]

init_triples = convert(_init_triples)
insert = convert(_insert)        
update_rem = convert(_update_rem)
update_ins = convert(_update_ins)

#print init_triples

rs1 = node.CreateSubscribeTransaction(ss_handle)
try:
    result_rdf = rs1.subscribe_rdf([Triple(None, URI('lives'), None)], 
                                   RdfMsgHandler())
    print "RDF Subscribe initial result:", result_rdf
except M3Exception:
    print "RDF subscription failed:", M3Exception

rs2 = node.CreateSubscribeTransaction(ss_handle)

try:
    result_wql = rs2.subscribe_wql_values(URI('x1'), 
                                          ['seq', 'drinks'], 
                                          NodeMsgHandler())
    print "WQL values subscribe initial result:", result_wql
except M3Exception:
    print "WQL values subscription failed:", M3Exception

pro = node.CreateInsertTransaction(ss_handle)

try:
    pro.send(init_triples, confirm = True)
except M3Exception:
    print "Insert (init triples) failed:", M3Exception

try:
    pro.send(insert, confirm = True)
except M3Exception:
    print "Insert failed:", M3Exception

try:
    bn = pro.send(bNode_triples, confirm = True)
    print "Blank node URIs", bn
except M3Exception:
    print "Blank node insert failed:", M3Exception


node.CloseInsertTransaction(pro)

upd = node.CreateUpdateTransaction(ss_handle)
try:
    upd.update(update_ins, "RDF-M3", update_rem, "RDF-M3", confirm = True)
except M3Exception:
    print "Update failed:", M3Exception

node.CloseUpdateTransaction(upd)

print "Querying what is being drunk"
qs = node.CreateQueryTransaction(ss_handle)
try:
    result = qs.rdf_query([Triple(None, URI("drinks"), None)])
    for item in result:
        print "QUERY: Got triple(s): ", item
except M3Exception:
    print "RDF query (*, drinks, *) failed:", M3Exception

print "Querying: type of x1"
try:
    result = qs.wql_nodetypes_query(URI('x1'))
    for item in result:
        print "QUERY: x1 is of type: ", item
except M3Exception:
    print "WQL nodetypes query for x1 failed:", M3Exception

print

print "Querying: is person a subtype of thing"
try:
    result = qs.wql_issubtype_query(URI('person'), URI('thing'))
    print "QUERY: person is a subtype of thing is: ", result
except M3Exception:
    print "WQL issubtype query for person->thing failed:", M3Exception

print

print "Querying: x1 and x2 related via 'knows' property"
try:
    result = qs.wql_related_query(URI('x1'), URI('x2'),['seq', 'knows'])
    print "QUERY: x1 knows x2 is", result
except M3Exception:
    print "WQL related query for x1-knows->x2 failed:", M3Exception

print

print "Querying: is x1 a person"
try:
    result = qs.wql_istype_query(URI('x1'), URI('person'))
    print "QUERY: 'x1 is a person' is ", result
except M3Exception:
    print "WQL istype query for 'is x1 a person' failed:", M3Exception

print

print "Querying: which persons live in Espoo"
try:
    result = qs.wql_values_query(Literal('Espoo'), ['inv', 'lives'])
    print "QUERY: persons living in Espoo:", result
except M3Exception:
    print "WQL values query for x1, [inv, lives] failed:", M3Exception

print

print "Querying: all triples"
try:
    result = qs.rdf_query([Triple(None, None, None)])
    for item in result:
        print "QUERY: Got triple: ", item
except M3Exception:
    print "RDF query for (*, *, *) failed:", M3Exception


node.CloseQueryTransaction(qs)

delete = [Triple(URI('x2'), URI('lives'), Literal('Espoo'))]
ds = node.CreateRemoveTransaction(ss_handle)
ds.remove(delete, confirm = "True")
node.CloseRemoveTransaction(ds)

node.CloseSubscribeTransaction(rs1)
print "Unsubscribing RDF subscription"
node.CloseSubscribeTransaction(rs2)
print "Unsubscribing WQL subscription"
#time.sleep(3)
node.leave(ss_handle)
print "Left smart space"
