import yaml

# Generate an svg image which shows the timeline of a recipe

y_offset = 1.5  # em
y_spacing = 2.2 # em
x_offset = 5    # percent
x_spacing = 0   # percent, set in find_positions

class StepNode:
    # Each node has a timeline step (its x position) and a height (its y position)
    # All nodes in a line on the same height belong to the same group
    def __init__(self, id, depends_list, temp, step_type):
        self.x = id
        self.y = 0
        self.group = 0
        self.svg_x = 0
        self.svg_y = 0
        self.temp = temp
        self.step_type = step_type
        self.depends_on = depends_list

def find_positions(yaml):
    global x_spacing
    global y_offset
    global y_spacing

    nodes = []
    next_group = 1
    amount_of_steps = len(yaml['steps'])
    x_spacing = (90.0/amount_of_steps)

    for step in yaml['steps']:
        node = StepNode(step['id'], step['depends_on'], step['temp'], step['type'])
        if node.depends_on == []:
            node.group = next_group
            next_group += 1
        else:
            lowest_group = 1024
            for d in node.depends_on:
                if nodes[d].group < lowest_group:
                    lowest_group = nodes[d].group
            node.group = lowest_group
        nodes.append(node)


    done_node = StepNode(amount_of_steps, [amount_of_steps - 1], 'done', 'done')
    done_node.y = 1
    nodes.append(done_node)

    return nodes

def start_improve_positions(nodes):
    y_pos = 1
    current_group = 1
    safe_ys = [1]*len(nodes)

    for i,node in enumerate(nodes):
        if node.group == current_group:
            node.y = y_pos
            safe_ys[i] = y_pos+1
            safe_y = y_pos + 1
            if len(node.depends_on) > 1:
                for dep in node.depends_on:
                    dep_group = nodes[dep].group
                    if dep_group != current_group:
                        dep_y = improve_positions(nodes[:dep+1], dep_group, dep, safe_y, safe_ys[:i+1])
                        safe_y = dep_y + 1
                        safe_ys[i] = max(safe_ys[i], safe_y)

def improve_positions(nodes, current_group, cur_index, start_y, safe_ys):
    cur_node = nodes[cur_index]
    if cur_node.y > 0:
        return cur_node.y

    y_levels_taken = []
    first_in_group = 0
    for n in nodes:
        if n.group == current_group:
            break
        first_in_group += 1

    y_used = start_y
    for y in safe_ys[first_in_group:]:
        if y > y_used:
            y_used = y

    connected = len(cur_node.depends_on)
    if connected > 1:
        cur_node.y = y_used
        safe_y = y_used
        for dep in cur_node.depends_on:
            dep_group = nodes[dep].group
            dep_y = improve_positions(nodes[:cur_index], dep_group, dep, safe_y, safe_ys[:cur_index+1])
            safe_y = dep_y + 1
        safe_ys[cur_index] = max(safe_ys[cur_index], safe_y)
    elif connected == 1:
        y_used = improve_positions(nodes[:cur_index], current_group, cur_node.depends_on[0], y_used, safe_ys[:cur_index+1])
    cur_node.y = y_used
    safe_ys[cur_index] = max(safe_ys[cur_index], y_used+1)
    return y_used

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
    global y_offset
    global y_spacing
    nodes = find_positions(yaml)
    start_improve_positions(nodes)

    deepest_y = 0
    for n in nodes:
        if n.y > deepest_y:
            deepest_y = n.y
    yaml['timeline'] = {}
    yaml['timeline']['height'] = y_offset*2 + y_spacing*(deepest_y-1)

    add_svg_positions(nodes)
    add_timeline_to_yaml(yaml, nodes)
