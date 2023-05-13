def prepare_data(massiv_with_incidents):
    unique_items = {}
    clear_data = []

    for item in massiv_with_incidents:
        key = tuple(item[:2])
        if key in unique_items and item[4] == unique_items.get(key)[0][4]:
            unique_items[key].append(item)
        else:
            unique_items[key] = [item]
    duplicates = [value for value in unique_items.values() if len(value) >= 2]
    for index, _ in enumerate(duplicates):
        test = []
        for item in _:
            test.append([item[0], item[1], item[2], str(item[3]).strip(), item[4]])
        clear_data.append(test)
    return clear_data
