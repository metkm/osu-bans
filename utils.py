def iterate_list(list_to_iterate: list, n: int):
    start = 0
    end = start + n

    while end <= len(list_to_iterate):
        yield list_to_iterate[start: end]

        start = end
        end = start + n


def difference_between_lists(main_list: list, second_list: list) -> list:
    difference = []
    for element in main_list:
        if element not in second_list:
            difference.append(element)

    return difference
