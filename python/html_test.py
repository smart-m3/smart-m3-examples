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

node = KP("HTML_Tester")
# ss_handle = node.discover(method = "mDNS")
ss_handle = node.discover()
print ss_handle

if not node.join(ss_handle):
    sys.exit('Could not join to Smart Space')

print "--- Member of SS:", node.member_of

html_str = '<html><head></head><body>foo</body></html>'
bracket_str = '<foo>'

triples_init = [Triple(URI('1'), URI('content'), Literal(bracket_str))]
triples = [Triple(URI('1'), URI('content'), Literal(html_str))]


#print init_triples

pro = node.CreateInsertTransaction(ss_handle)
print "Trying to insert <foo> literal"
try:
    bn = pro.send(triples_init, confirm = True)
    print "Blank node URIs for 1st insert", bn
except M3Exception:
    print "Blank node insert failed:", M3Exception
    sys.exit(1)

print "Trying to insert html literal"
try:
    bn = pro.send(triples, confirm = True)
    print "Blank node URIs for 2nd insert", bn
except M3Exception:
    print "Blank node insert failed:", M3Exception
    sys.exit(1)

node.CloseInsertTransaction(pro)

print "Querying for *, content, *"
qs = node.CreateQueryTransaction(ss_handle)
try:
    result = qs.rdf_query([Triple(None, URI("content"), None)])
    for item in result:
        print "QUERY: Got triple(s): ", item
except M3Exception:
    print "RDF query (*, content, *) failed:", M3Exception

print "Querying: what is the content"
try:
    result = qs.wql_values_query(URI('1'), ['seq', 'content'])
    print "QUERY: content with WQL values query", result
except M3Exception:
    print "WQL values query for uri, [seq, content] failed:", M3Exception

print

print "Querying: all triples"
try:
    result = qs.rdf_query([Triple(None, None, None)])
    for item in result:
        print "QUERY: Got triple(s): ", item
except M3Exception:
    print "RDF query for (*, *, *) failed:", M3Exception

node.CloseQueryTransaction(qs)

node.leave(ss_handle)
print "Left smart space"
