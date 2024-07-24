# compares each item in a list with the rest of the items and if n items are equal the item is returned.
def get_first_element_that_has_n_equal_elements(a_list, n):
    a_list_copy = a_list.copy()
    elm_max = len(a_list_copy)-1
    for _ in range(elm_max):
        item = a_list_copy.pop(0)
        if len(a_list_copy) < n-1:
            return None
        match_count = 1
        for other_item in a_list_copy:
            if item == other_item:
                match_count += 1
                if match_count >= n:
                    return item
    return None