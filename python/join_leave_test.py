from smart_m3.m3_kp import *

kp1 = KP("test1")
kp2 = KP("test2")

ss = kp1.discover()

try:
    kp1.join(ss)
except M3Exception:
    print "KP1 1st JOIN failed"

try:
    kp1.join(ss)
except M3Exception:
    print "KP1 2nd JOIN failed"

try:
    kp2.join(ss)
except M3Exception:
    print "KP2 JOIN failed"

try:
    kp1.leave(ss)
except M3Exception:
    print "KP1 1st LEAVE failed"

try:
    kp1.leave(ss)
except M3Exception:
    print "KP1 2nd LEAVE failed"

try:
    kp2.leave(ss)
except M3Exception:
    print "KP2 LEAVE failed"


