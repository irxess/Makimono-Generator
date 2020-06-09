from data import *

def calculate_total_time_needed(recipe):
    for step in recipe.steps:
        step_sum = step.time.active + step.time.passive



def calculate_time(step, calculated_time):
    calculated_time += step.time.active + step.time.passive
    if step.depends_on == []:
        return
    else:
        for child in step.depends_on:
            calculate_time(child, calculated_time)

def get_leaf_node_ids(recipe):
    leaf_node_ids = []
    for step in recipe.steps:
        if step.depends_on == []:
            leaf_node_ids.append(step.id)
    return leaf_node_ids

def get_root_node_ids(recipe):
    # ToDo
    root_node_ids = []
    for step in recipe.steps:
        is_root = True
        for other_step in recipe.steps:
            if step.id in other_step.depends_on:
                is_root = False
                break
        if is_root:
            root_node_ids.append(step.id)
    return root_node_ids

def get_root_node_ids_linear(recipe):
    root_node_ids = []

    for step in recipe.steps:
        root_node_ids.append(step.id)

    for step in recipe.steps:
        for child in step.depends_on:
            if child.id in root_node_ids:
                root_node_ids.remove(child.id)

    return root_node_ids

def get_root_node_ids_linear_set(recipe):
    root_node_ids = set()

    for step in recipe.steps:
        root_node_ids.add(step.id)

    for step in recipe.steps:
        root_node_ids -= set(step.depends_on)

    return list(root_node_ids)



# root_node_ids = recipe.steps(step => recipe.steps.All(other_steps => step.id not in recipe.steps.depends_on))
#       if all(!is_direct_child_of(step.id, other_steps) for other_steps in recipe.steps):
#           root_node_ids.append(step.id)

# def is_direct_child_of(child, parent):
#   return child.id in parent.depends_on

# def is_child_of(child_id, parent_id, recipe):
#   # don't need this, fun to think of though
