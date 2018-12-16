import yaml
from data import Step, StepSVG, Point, Line, Circle, Timeline, Recipe

# Generate an svg image which shows the timeline of a recipe

y_offset  = 1.5 # em
y_spacing = 2.2 # em
x_offset  = 5   # percent
x_spacing = 0   # percent, set in find_positions

def find_positions(recipe):
    global x_spacing

    next_group = 1
    amount_of_steps = len(recipe.steps)
    x_spacing = (90.0/amount_of_steps)

    for step in recipe.steps:
        svg_node = StepSVG(x=step.id)
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

def append_done_node_to_steps(steps):
    number_of_steps = len(steps)
    done_svg = StepSVG(x=number_of_steps)
    done_svg.y = 1
    done_step = Step(id=number_of_steps, time=0, step_type='done', temperature='done', depends_on=[number_of_steps - 1])
    done_step.svg = done_svg
    steps.append(done_step)


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
                        dep_y = improve_positions(nodes[:dep+1], dep_group, dep, safe_y, safe_ys, i+1)
                        safe_y = dep_y + 1
                        safe_ys[i] = max(safe_ys[i], safe_y)


def improve_positions(nodes, current_group, cur_index, start_y, safe_ys, end):
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
    for y in safe_ys[first_in_group:end]:
        if y > y_used:
            y_used = y

    connected = len(cur_node.depends_on)
    if connected > 1:
        cur_node.svg.y = y_used
        safe_y = y_used
        for dep in cur_node.depends_on:
            dep_group = nodes[dep].svg.group
            dep_y = improve_positions(nodes[:cur_index], dep_group, dep, safe_y, safe_ys, cur_index+1)
            safe_y = dep_y + 1
            safe_ys[dep] = max(safe_ys[dep], safe_y)
        safe_ys[cur_index] = max(safe_ys[cur_index], cur_node.svg.y +1)
    elif connected == 1:
        y_used = improve_positions(nodes[:cur_index], current_group, cur_node.depends_on[0], y_used, safe_ys, cur_index+1)
    cur_node.svg.y = y_used
    safe_ys[cur_index] = max(safe_ys[cur_index], y_used+1)
    return y_used


def add_svg_positions(steps):
    global y_offset
    global y_spacing
    global x_offset
    global x_spacing

    for step in steps:
        step.svg.svg_x = int((step.svg.x * x_spacing) + x_offset)
        step.svg.svg_y = y_offset + (y_spacing * (step.svg.y-1))


def print_nodes(recipe):
    for step in recipe.steps:
        print('Node ', step.svg.x, '\ty: ', step.svg.y, '\tsvg_x: ', step.svg.svg_x, '%')

def add_timeline_to_data(recipe):
    global y_offset
    global y_spacing
    global x_spacing

    deepest_y = 0
    for step in recipe.steps:
        if step.svg.y > deepest_y:
            deepest_y = step.svg.y
    height = y_offset*2 + y_spacing*(deepest_y-1)
    recipe.timeline = Timeline(height=height)

    for step in recipe.steps:
        circle = Circle(color=step.temperature, center=Point(x=step.svg.svg_x, y=step.svg.svg_y), step_type=step.step_type)
        recipe.timeline.circles.append(circle)
        for d in step.depends_on:
            dep_step = recipe.steps[d]
            split_x = step.svg.svg_x - x_spacing
            if dep_step.svg.svg_x >= split_x:
                color = dep_step.temperature
                start = Point(x=dep_step.svg.svg_x, y=dep_step.svg.svg_y)
                end = Point(x=step.svg.svg_x, y=step.svg.svg_y)
                line = Line(start=start, end=end, color=color)
                recipe.timeline.lines.append(line)
            else:
                color = dep_step.temperature
                start = Point(x=dep_step.svg.svg_x, y=dep_step.svg.svg_y)
                middle = Point(x=split_x, y=dep_step.svg.svg_y)
                end = Point(x=step.svg.svg_x, y=step.svg.svg_y)
                line1 = Line(start=start, end=middle, color=color)
                line2 = Line(start=middle, end=end, color=color)
                recipe.timeline.lines.append(line1)
                recipe.timeline.lines.append(line2)


def generate_timeline_svg(recipe):
    find_positions(recipe)
    append_done_node_to_steps(recipe.steps)
    start_improve_positions(recipe.steps)
    add_svg_positions(recipe.steps)
    add_timeline_to_data(recipe)
    del recipe.steps[-1] # Remove "done" step used at end of timeline
