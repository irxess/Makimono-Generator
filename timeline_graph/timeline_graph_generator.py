import yaml
from timeline_graph_data import Node, TimelineGraph

# Overview of approach:
# For each node/x:
# If previous node at this height/y-value has other node depending on it, and the other depending node has a higher x-value than this node:
# Increment y-value of this node by one and check again
