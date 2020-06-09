from data import *

def calculate_total_time_needed(recipe):
    root_node_ids = get_root_node_ids(recipe.steps)

    upper_bound_needed_time = calculate_total_time_needed_for_all_steps(recipe.steps)

    slowest_chain_times = set()
    steps_dictionary = make_step_dictionary(recipe.steps)
    for root in root_node_ids:
        slowest_chain_times.add(calculate_time_for_slowest_chain(root, steps_dictionary))

    lower_bound_needed_time = max(slowest_chain_times)

def calculate_time_for_slowest_chain(step_id, steps_dictionary)
    step = steps_dictionary[step_id]
    current_step_required_time = step.time.active + step.time.passive
    if step.depends_on == []:
        return current_step_required_time

    child_times = set()
    for child_id in step.depends_on:
        child_time = calculate_time_for_slowest_chain(child_id, steps_dictionary)
        child_times.add(child_time)

    child_path_needing_most_time = max(child_times)
    return child_path_needing_most_time + current_step_required_time

def calculate_total_time_needed_for_all_steps(steps):
    """ToDo: Describe that this is done simplistic to handle cycles without a lot of complexity"""
    time_needed = 0
    for step in steps:
        time_needed += step.time.active + step.time.passive
    return time_needed

def get_root_node_ids(steps):
    root_node_ids = set()

    for step in steps:
        root_node_ids.add(step.id)

    for step in steps:
        root_node_ids -= set(step.depends_on)

    return root_node_ids

def make_step_dictionary(steps):
    steps_dictionary = dict()
    for step in steps:
        steps_dictionary[step.id] = step
    return steps_dictionary
