__author__ = 'madevyatov'
from lxml import etree
from functions import *



f = open('sample.xml', 'r')
rpc_reply_list = parse_file(f)
f.close()


if __name__ == "__main__":
    for tree in rpc_reply_list:
        print "Chassis XXX"
        for fpc, utilization in fpc_ram_utilization(tree).iteritems():
            print 'FPC:', fpc, '   RAM usage:', utilization

