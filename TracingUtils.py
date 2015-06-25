"""
This is TracingUtils.py
This script offers functions for network setup used by Tracing.py.
Especially reading network from file, which has a specifiv structure

Last modified 25.6.2015

"""
__author__ = 'TOSS'

import networkx as nx
from datetime import datetime, timedelta

def read_attr_edgelist(fn,first_recod=False):
    '''
    This function reads attributed edgelist from file and returns a relabelled MultiDiGraph.

    Input:
    -------

    **fn**: filename i.e. file containing the edgelist with attributes. The input file needs to have the following structure
    "source","destination","id","t","n","category"
    1,8184,"00001",2005-10-18,1,"Cattle"
    2,3478,"00002",2005-09-16,1,"Cattle"
    3,8184,"00003",2005-10-25,1,"Cattle"
    3,8184,"00004",2005-10-25,1,"Cattle"
    4,3478,"00005",2005-09-15,1,"Cattle"
    5,3478,"00006",2005-08-28,1,"Cattle"
    6,3478,"00007",2005-09-15,1,"Cattle"
    7,8185,"00008",2005-09-09,1,"Cattle"
    8,8186,"00009",2005-09-27,1,"Cattle"

    Output:
    -------
    G: (relabelled) MultiDiGraph as a networkx object
    '''

    with open(fn) as f:
        f.next()
        elines = [str.replace(line, '\n','') for line in f]


    felines = [str.replace(l,',',' ') for l in elines]


    Go = nx.parse_edgelist(felines, create_using=nx.MultiDiGraph(),
                           data=(('id', str),
                                 ('D', str),
                                 ('n',int),
                                 ('Species', str)))

    if first_recod:
        nGo = nx.convert_node_labels_to_integers(Go, label_attribute="BNR")
        for s,t,a in nGo.edges(data=True):
            a['D'] = datetime.strptime(a.get('D'),"%Y-%m-%d").date()
        return nGo, nx.get_node_attributes(nGo,'BNR')
    else:
        for s,t,a in Go.edges(data=True):
            a['D'] = datetime.strptime(a.get('D'),"%Y-%m-%d").date()
        return Go
