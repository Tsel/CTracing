"""
This is Tracing.py
This script offers functions for Contact Tracing.
Tracing is based on Depth first search algorithms described in networkx

Last modified 25.6.2015
"""
__author__ = 'TOSS'

import networkx as nx
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
    """

    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


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

    if source is None:
        nodes = G[0]
    else:
        nodes = [source]

    for start in nodes:
        stack = [(start,iter(G[start]))]
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)
                #
                # Contact date (cdate) will be considered when cdate in (tstart,tend)
                # FIXME: check if it is possible to write
                # if date_in_range(G[parent]['DoI'], tend, G[parent][child]['cdate']):
                if date_in_range(tstart, tend, G[parent][child]['cdate']):
                    G[child]['DoI'] = G[parent][child]['cdate']
                    stack.append((child,iter(G[child])))
            except StopIteration:
                stack.pop()

# This perfoems tracing with a test data set
#
if __name__ == "__main__":
    fn = "/Users/TOSS/Documents/Projects/R/IOCC/data/ctrans.csv"