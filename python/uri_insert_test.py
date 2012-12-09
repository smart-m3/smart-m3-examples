from smart_m3.m3_kp import *
# from pyrple import Node, URI, Literal, bNode, Triple
import time
import sys

node = KP("Insert Tester")
# ss_handle = node.discover(method = "mDNS")
ss_handle = node.discover()
print ss_handle

if not node.join(ss_handle):
    sys.exit('Could not join to Smart Space')

print "--- Member of SS:", node.member_of

triples = [Triple(URI('x1'), URI('email_address'), URI('mailto:a@b.com')),
           Triple(URI('x1'), URI('fax_number'), URI('fax:+3581234567')),
           Triple(URI('x1'), URI('profile'), URI('file:///home/a/.profile'))]

pro = node.CreateInsertTransaction(ss_handle)

try:
    pro.send(triples, confirm = True)
except M3Exception:
    print "Insert failed:", M3Exception

node.CloseInsertTransaction(pro)

qs = node.CreateQueryTransaction(ss_handle)

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
