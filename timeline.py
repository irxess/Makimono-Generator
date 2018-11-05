import yaml

# Generate an svg image which shows the timeline of a recipe

y_offset = 25   # pixels
y_spacing = 40  # pixels
x_offset = 5    # percent
x_spacing = 0   # percent, set in find_positions

class StepNode:
    # Each node has a timeline step (its x position)
    # and a height (its y position)
    def __init__(self, id, depends_list, temp, step_type):
        self.x = id
        self.y = 0
        self.svg_x = 0
        self.svg_y = 0
        self.temp = temp
        self.step_type = step_type
        self.depends_on = depends_list

def find_positions(yaml):
    global y_offset
    global y_spacing
    global x_spacing
    nodes = []
    next_y = 1
    deepest_y = 1
    amount_of_steps = len(yaml['steps'])
    x_spacing = (90.0/amount_of_steps)

    for step in yaml['steps']:
        node = StepNode(step['id'], step['depends_on'], step['temp'], step['type'])
        if node.depends_on == []:
            node.y = next_y
            next_y += 1
            if(next_y > deepest_y):
                deepest_y = next_y
        else:
            lowest_y = 1024
            for d in node.depends_on:
                if nodes[d].y < lowest_y:
                    lowest_y = nodes[d].y
            node.y = lowest_y
            next_y = 2
        nodes.append(node)


    done_node = StepNode(amount_of_steps, [amount_of_steps - 1], 'done', 'done')
    done_node.y = 1
    nodes.append(done_node)

    yaml['timeline'] = {}
    yaml['timeline']['height'] = y_offset*2 + y_spacing*(deepest_y-2)

    return nodes

def improve_positions(nodes):
    global x_offset
    global x_spacing

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

def add_svg_positions(nodes):
    global y_offset
    global y_spacing
    global x_offset
    global x_spacing

    for node in nodes:
        node.svg_x = (node.x * x_spacing) + x_offset
        node.svg_y = y_offset + (y_spacing * (node.y-1))

    return nodes

def print_nodes(nodes):
    for n in nodes:
        print('Node ', n.x, '\ty: ', n.y, '\tsvg_x: ', n.svg_x, '%')

def add_timeline_to_yaml(yaml, nodes):
    global y_spacing
    lines = []
    circles = []

    yaml['timeline']['lines'] = []
    yaml['timeline']['circles'] = []
    for n in nodes:
        circle = {}
        circle['color'] = n.temp
        circle['center'] = {'x': n.svg_x, 'y': n.svg_y}
        circle['type'] = n.step_type
        yaml['timeline']['circles'].append(circle)
        for d in n.depends_on:
            split_x = n.svg_x - x_spacing
            m = nodes[d]
            if m.svg_x >= split_x:
                line = {}
                line['color'] = m.temp
                line['start'] = {'x': m.svg_x, 'y': m.svg_y}
                line['end'] = {'x': n.svg_x, 'y': n.svg_y}
                yaml['timeline']['lines'].append(line)
            else:
                line1 = {}
                line1['color'] = m.temp
                line1['start'] = {'x': m.svg_x, 'y': m.svg_y}
                line1['end'] = {'x': split_x, 'y': m.svg_y}
                yaml['timeline']['lines'].append(line1)
                line2 = {}
                line2['color'] = m.temp
                line2['start'] = {'x': split_x, 'y': m.svg_y}
                line2['end'] = {'x': n.svg_x, 'y': n.svg_y}
                yaml['timeline']['lines'].append(line2)


def generate_svg(yaml):
    nodes = find_positions(yaml)
    improve_positions(nodes)
    add_svg_positions(nodes)
    add_timeline_to_yaml(yaml, nodes)
