import yaml
from timeline_graph_data import Node, TimelineGraph

# Overview of approach:
# For each node/x:
# If previous node at this height/y-value has other node depending on it, and the other depending node has a higher x-value than this node:
# Increment y-value of this node by one and check again

# The above algorithm is flawed. There is a simple counterexample with <= 5 nodes, but I can't be bothered to draw it up now.

def find_number_of_crossing_edges(TimelineGraph):
    number_of_crossing_edges = 0
    # ToDo: Implement solution
    # Assumed prerequisites:
    # - Data structure where we can look up nodes based on their ID/x-position.
    # - Data structure where we can look up a y-level and get all associated nodes.

    # An edge is crossing from below if:
    # - A node node_source is connected to another node_sink.
    # - node_source.x < node_sink.x
    # - node_source.y <= node_sink.y
    # - Another node, disrupting_source_node, is connected to distrupting_target_node.
    # - disrupting_source_node.x < distrupting_target_node.x
    # - node_source.x < distrupting_target_node.x < node_sink.x
    # - disrupting_source_node.y < node_sink.y < distrupting_target_node.y

    # An edge is crossing from above if:
    # - A node node_source is connected to another node_sink.
    # - node_source.x < node_sink.x
    # - node_source.y >= node_sink.y
    # - Another node, disrupting_source_node, is connected to distrupting_target_node.
    # - disrupting_source_node.x < distrupting_target_node.x
    # - node_source.x < distrupting_target_node.x < node_sink.x
    # - disrupting_source_node.y > node_sink.y > distrupting_target_node.y
    return number_of_crossing_edges
