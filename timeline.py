import yaml

# Generate an image (svg?) which shows the timeline of a recipe
# Should use the for now non-existing timeline.svg template

class StepNode:
    # Each node has a timeline step (its x position)
    # and a height (its y position)
    def __init__(self, id, depends_list, temp):
        self.x = id
        self.y = 0
        self.svg_x = 0
        self.svg_y = 0
        self.temp = temp
        self.depends_on = depends_list

def find_positions(yaml):
    nodes = []
    next_y = 1
    amount_of_steps = len(yaml['steps'])
    for step in yaml['steps']:
        node = StepNode(step['id'], step['depends_on'], step['temp'])
        if node.depends_on == []:
            node.y = next_y
            next_y += 1
        else:
            lowest_y = 1024
            for d in node.depends_on:
                if nodes[d].y < lowest_y:
                    lowest_y = nodes[d].y
            node.y = lowest_y
        node.svg_x = round(node.x * (90.0/amount_of_steps)) +5 # 5% offset on each side?
        nodes.append(node)
    # Add a "done" node, with svg_x = 95
    return nodes
    # Iterate through all nodes?
    # Is the initial y good enough, or do I need to reorder them?
    # I think I need to reorder based on first merge into the "main" branch on top
    # Do I create a mapping table?
    # Remember to also account for merges in other branches
    # Create a function that updates values based on a "main branch" parameter?
    # Can create a recursive function that updates one branch at a time
    # It should "understand" when a certain y becomes available again, and can be used

    # For now: x * (1/amount_of_steps) = position in %
    # Later: While looping: find the highest and total amount of time

def print_nodes(nodes):
    for n in nodes:
        print('Node ', n.x, '\ty: ', n.y, '\tsvg_x: ', n.svg_x, '%')


def generate_svg(yaml):
    nodes = find_positions(yaml)
    print_nodes(nodes)
