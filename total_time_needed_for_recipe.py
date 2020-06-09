from data import *

def calculate_total_time_needed(recipe):
    root_node_ids = get_root_node_ids(recipe.steps)

    upper_bound_needed_time = calculate_total_time_needed_for_all_steps(recipe.steps)

    slowest_chain_times = set()
    steps_dictionary = make_step_dictionary(recipe.steps)
    for root in root_node_ids:
        slowest_chain_times.add(calculate_time_for_slowest_chain(root, steps_dictionary))

    lower_bound_needed_time = max(slowest_chain_times)

def calculate_total_time_needed_for_all_steps(steps):
    """
    A simplistic function for calculating the time needed for completing a collection of steps,
    assuming that all the steps are being done consecutively.
    This is done separately from the recursive function for finding the slowest sequence of steps
    that bounds your execution time when you can paralellize all steps perfectly.
    The reason for the separation (and therefore "needless" extra traversal of all the steps),
    is that it would make the calculate_time_for_slowest_chain much more complex, for very little benefit.
    For instance, to handle the case that some steps might branch out to be used by several subsequent
    steps, one would have to introduce the concept of coloring or marking the nodes as visited.
    That in turn would require a new, more complex data structure to store that state, and so on.
    """
    time_needed = 0
    for step in steps:
        time_needed += step.time.active + step.time.passive
    return time_needed

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

def get_root_node_ids(steps):
    """Not sure if we're ever going to actually have to depend on it, but it was fun to make!"""
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
