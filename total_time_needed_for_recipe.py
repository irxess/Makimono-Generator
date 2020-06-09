from data import *

def calculate_total_time_needed(recipe):
    # for step in recipe.steps:
    #     step_sum = step.time.active + step.time.passive
    root_node_ids = get_root_node_ids(recipe.steps)
    time_if_all_steps_done_consecutively = 0
    time_if_execution_perfectly_paralell = 0

    for root in root_node_ids:
        calculate_time(root, time_if_all_steps_done_consecutively, time_if_execution_perfectly_paralell, recipe.steps)

def calculate_time(step_id, most_time, least_time, steps):
    step = get_step_with_id_from_recipe(step_id, steps)
    most_time += step.time.active + step.time.passive

    for child_id in step.depends_on:
        calculate_time(child_id, most_time, least_time, recipe)



def calculate_time(step, calculated_time):
    calculated_time += step.time.active + step.time.passive
    if step.depends_on == []:
        return
    else:
        for child in step.depends_on:
            calculate_time(child, calculated_time)


# To get sum of slowest possible execution:
# - sum all active and passive time for all steps

# To get time needed for fastets possible execution:
# - sum all active and passive time for longes chain (in terms of needed time) of dependent steps
# For each step:
# Add it's passive and active time to the larges of the ones from it's children

def calculate_time_for_slowest_chain(step_id, steps)
    step = get_step_with_id_from_recipe(step_id, steps)
    current_step_required_time = step.time.active + step.time.passive
    if step.depends_on == []:
        return current_step_required_time

    child_times = set()
    for child_id in step.depends_on:
        child_time = calculate_time_for_slowest_chain(child_id, steps)
        child_times.add(child_time)

    child_path_needing_most_time = max(child_times)
    return child_path_needing_most_time + current_step_required_time






def get_leaf_node_ids(steps):
    leaf_node_ids = []
    for step in steps:
        if step.depends_on == []:
            leaf_node_ids.append(step.id)
    return leaf_node_ids

def get_root_node_ids(steps):
    root_node_ids = set()

    for step in steps:
        root_node_ids.add(step.id)

    for step in steps:
        root_node_ids -= set(step.depends_on)

    return root_node_ids

def get_step_by_id(step_id, steps):
    for step in steps:
        if step.id == step_id:
            return step
    return None

# def is_direct_child_of(child, parent):
#   return child.id in parent.depends_on

# def is_child_of(child_id, parent_id, recipe):
#   # don't need this, fun to think of though