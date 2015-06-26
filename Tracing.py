"""
This is Tracing.py
This script offers functions for Contact Tracing.
Tracing is based on Depth first search algorithms described in networkx

Last modified 25.6.2015
"""
__author__ = 'TOSS'

import networkx as nx
import TracingUtils as tu
from datetime import datetime
from collections import defaultdict


def date_in_range(start, end, x):
    """
    Returns True if start <= x <= end on condition that start <= end (see else).


    Parameters:
    ------------

    :param start: datetime date start date
    :param end: datetime date end date
    :param x: datetime date actual date

    Returns:

    :return: True if start <= x <= end on condition that start <= end
    :rtype : boolean
    """

    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def valid_contact(G, index_node, parent, child, t):
    """
    Checks the validity of the contact between parent and child
    :type child: str
    :type index_node: str
    :type G: G is a networkx DiMultiGraph
    :param G: The network we are working on.
    :param index_node: is the node where infection started
    :param parent: The contact parent -> child is considered. This is node parent
    :param child: The conatct parent chil is considered: This is node child
    :param t: the end of the observational period
    
    :return: :rtype boolean. Retruns t True, if the conact between parent and child is valid.
    
    The following conditions are checked:
    1.) Does the time of contact between parent and child take place between the Date of infection of parent and the 
        end of the observational period t?
    2.) If child has attributes 'Infektor' and 'DoI', then it must have been visited before:
        Check whether the 'Infektor' is identical, AND if DoI of child is identical to time of contact.
    3.) Check if child is start. 
        In this case we would loop back to the source of infection (start) which is not possible
    4.) Check for loop parent -> child -> parent, which is not possible

    """
    #
    # Check condition 1
    # returns True if contact is within specified date range
    c1 = date_in_range(G.node[parent]['DoI'], t, G[parent][child][0]['cdate'])
    #
    # Check condition 2
    if ('Infektor' in G.node[child]) and ('DoI' in G.node[child]):
        c2 = G[parent][child][0]["cdate"] != G.node[child]["DoI"]
    else:
        c2 = True
    
    #
    # Check condition 3
    assert isinstance(index_node, str)
    c3 = child != index_node
    #
    # Check condition 4
    # Infektor of parent is unequal child
    c4 = G.node[parent]['Infektor'] != child

    return (c1 and c2 and c3 and c4)

    

def CTracing(G, tstart, tend, source=None):
    """
    This is an adaption of tracing_dfs_edges from networkx version 1.9.1.
    Additional condotion are added to perform a chronological contact tracing

    Parameters:
    ---------------
    :param G: networkx Graph

    :param source: the source node if not set, the first node of the network G[0] is used
    :param tstart: datetime.date object representing the start of the time window
    :param tend: datetime.date object representing the end of the time window

    Returns:
     ---------------
    :return: edges: generator
        A generator of edges in the depth-first-search

    Notes:
    -----------
    Nodes and Edges of Graph G are decorated with attributes:
    a) date (datetime object) when edge is active. This is important to get the correct chronology of contacts
    b) Graph nodes are decorated with the earliest time of infection

    """
    #
    # FIXME: Example to be provided in the description of this routine
    # FIXME: boolean variable required to change between foreward and backward tracing
    # FIXME: reject loops

    if source is None:
        nodes = G[0]
    else:
        nodes = [source]

    for start in nodes:
        stack = [(start, iter(G[start]))]
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)
                if valid_contact(G,source,parent, child, tend):
                    G.node[child]['DoI'] = G[parent][child][0]['cdate']
                    G.node[child]['Infektor'] = parent
                    print "relevant contact : ", parent, " -> ", child, " at date: ", G.node[child][
                        'DoI'], " Infektors ", G.node[child]['Infektor'], G.node[parent]['Infektor'], child
                    stack.append((child, iter(G[child])))
                #
                # # Contact date (cdate) will be considered when cdate in (G.node[parent&%'DoI'],tend)
                # if date_in_range(G.node[parent]['DoI'], tend, G[parent][child][0]['cdate']):
                #     if ('Infektor' in G.node[child]) and ('DoI' in G.node[child]) and (
                #                     G[parent][child][0]["cdate"] == G.node[child]["DoI"] or child == start):
                #         print "===> rejected contact : ", parent, " -> ", child, " at date: ", G.node[child][
                #             'DoI'], " Infektor 4 child and parent. child and parent ID", G.node[child]['Infektor'], \
                #             G.node[parent]['Infektor'], child, parent
                #     else:
                #         G.node[child]['DoI'] = G[parent][child][0]['cdate']
                #         G.node[child]['Infektor'] = parent
                #         print "relevant contact : ", parent, " -> ", child, " at date: ", G.node[child][
                #             'DoI'], " Infektors ", G.node[child]['Infektor'], G.node[parent]['Infektor'], child
                #         stack.append((child, iter(G[child])))
            except StopIteration:
                stack.pop()

# This perfoems tracing with a test data set
#
if __name__ == "__main__":
    fn = "/Users/TOSS/Documents/Projects/R/IOCC/data/ctrans.csv"
    #
    # create a networkx MultiDiGraph
    G = tu.read_attr_edgelist(fn)
    #
    # Create some output
    print G.number_of_nodes()
    print G.number_of_edges()
    #
    # settings to run CTracing
    i_node = '2645'
    sdate = "2005-08-02"
    edate = "2005-10-31"
    dformat = "%Y-%m-%d"

    s_date = datetime.strptime(sdate, dformat).date()
    e_date = datetime.strptime(edate, dformat).date()
    #
    # set attributes of first infected node
    G.node[i_node]['DoI'] = s_date
    G.node[i_node]['Infektor'] = i_node
    #
    # start dfs Tracing
    CTracing(G, s_date, e_date, i_node)

