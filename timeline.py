import yaml
from data import Step, StepSVG, Point, Line, Circle, Timeline, Recipe

# Generate an svg image which shows the timeline of a recipe

y_offset = 1.5  # em
y_spacing = 2.2 # em
x_offset = 5    # percent
x_spacing = 0   # percent, set in find_positions

def find_positions(recipe):
    global x_spacing
    global y_offset
    global y_spacing

    #nodes = []
    next_group = 1
    amount_of_steps = len(recipe.steps)
    x_spacing = (90.0/amount_of_steps)

    for step in recipe.steps:
        svg_node = StepSVG(step.id)
        if step.depends_on == []:
            svg_node.group = next_group
            next_group += 1
        else:
            lowest_group = 1024
            for d in step.depends_on:
                if recipe.steps[d].svg.group < lowest_group:
                    lowest_group = recipe.steps[d].svg.group
            svg_node.group = lowest_group
        step.svg = svg_node
        #nodes.append(svg_node)

    done_svg = StepSVG(amount_of_steps) #StepNode(amount_of_steps, [amount_of_steps - 1], 'done', 'done')
    done_svg.y = 1
    done_step = Step(amount_of_steps, 0, 'done', 'done', [], [], [amount_of_steps - 1])
    done_step.svg = done_svg
    recipe.steps.append(done_step)
    #nodes.append(done_svg)


def start_improve_positions(nodes):
    y_pos = 1
    current_group = 1
    safe_ys = [1]*len(nodes)

    for i,node in enumerate(nodes):
        if node.svg.group == current_group:
            node.svg.y = y_pos
            safe_ys[i] = y_pos+1
            safe_y = y_pos + 1
            if len(node.depends_on) > 1:
                for dep in node.depends_on:
                    dep_group = nodes[dep].svg.group
                    if dep_group != current_group:
                        dep_y = improve_positions(nodes[:dep+1], dep_group, dep, safe_y, safe_ys[:i+1])
                        safe_y = dep_y + 1
                        safe_ys[i] = max(safe_ys[i], safe_y)


def improve_positions(nodes, current_group, cur_index, start_y, safe_ys):
    cur_node = nodes[cur_index]
    if cur_node.svg.y > 0:
        return cur_node.svg.y

    y_levels_taken = []
    first_in_group = 0
    for n in nodes:
        if n.svg.group == current_group:
            break
        first_in_group += 1

    y_used = start_y
    for y in safe_ys[first_in_group:]:
        if y > y_used:
            y_used = y

    connected = len(cur_node.depends_on)
    if connected > 1:
        cur_node.svg.y = y_used
        safe_y = y_used
        for dep in cur_node.depends_on:
            dep_group = nodes[dep].group
            dep_y = improve_positions(nodes[:cur_index], dep_group, dep, safe_y, safe_ys[:cur_index+1])
            safe_y = dep_y + 1
        safe_ys[cur_index] = max(safe_ys[cur_index], safe_y)
    elif connected == 1:
        y_used = improve_positions(nodes[:cur_index], current_group, cur_node.depends_on[0], y_used, safe_ys[:cur_index+1])
    cur_node.svg.y = y_used
    safe_ys[cur_index] = max(safe_ys[cur_index], y_used+1)
    return y_used


def add_svg_positions(steps):
    global y_offset
    global y_spacing
    global x_offset
    global x_spacing

    for step in steps:
        step.svg.svg_x = (step.svg.x * x_spacing) + x_offset
        step.svg.svg_y = y_offset + (y_spacing * (step.svg.y-1))


def print_nodes(recipe):
    for n in recipe.steps:
        print('Node ', n.svg.x, '\ty: ', n.svg.y, '\tsvg_x: ', n.svg.svg_x, '%')

def add_timeline_to_yaml(recipe):
    global y_offset
    global y_spacing
    lines = []
    circles = []

    deepest_y = 0
    for step in recipe.steps:
        if step.svg.y > deepest_y:
            deepest_y = step.svg.y
    height = y_offset*2 + y_spacing*(deepest_y-1)
    recipe.timeline = Timeline([], [], 0)

    for s in recipe.steps:
        circle = Circle(s.temperature, Point(s.svg.x, s.svg.y), s.step_type)
        recipe.timeline.circles.append(circle)
        for d in s.depends_on:
            dep_step = recipe.steps[d]
            split_x = dep_step.svg.svg_x - x_spacing
            if dep_step.svg.svg_x >= split_x:
                color = dep_step.temperature
                start = Point(dep_step.svg.svg_x, dep_step.svg.svg_y)
                end = Point(s.svg.svg_x, s.svg.svg_y)
                line = Line(start, end, color)
                recipe.timeline.lines.append(line)
            else:
                color = dep_step.temperature
                start = Point(dep_step.svg.svg_x, dep_step.svg.svg_y)
                middle = Point(split_x, dep_step.svg.svg_y)
                end = Point(s.svg.svg_x, s.svg.svg_y)
                line1 = Line(start, middle, color)
                line2 = Line(middle, end, color)
                recipe.timeline.lines.append(line1)
                recipe.timeline.lines.append(line2)


def generate_svg(recipe):
    svg_nodes = find_positions(recipe)
    start_improve_positions(recipe.steps)
    add_svg_positions(recipe.steps)
    add_timeline_to_yaml(recipe)
