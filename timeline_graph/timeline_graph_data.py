import yaml
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

@dataclass
class Node:
    x: int # Is also the ID
    y: int = 0
    depends_on: List[int] = field(default_factory=lambda: []) # The integers represent the x-values/IDs of the other nodes which this node depends on.
    other_nodes_that_depend_on_this: List[int] = field(default_factory=lambda: []) # The integers represent the x-values/IDs of the nodes that depend on this node.

@dataclass
class TimelineGraph:
    nodes: List[Node] = field(default_factory=lambda: []) # Note that position in this list should correspond to the x-value/ID of each node.
    ys: List[List[int]] = field(default_factory=lambda: [[]]) # For each y-level of the graph, contains a list of IDs(/x-values) of the nodes that are in this y-level. Perhaps not strictly neccessary (or optimally performant), but makes lookups on "whcih nodes are at this depth" easier to reason about.
