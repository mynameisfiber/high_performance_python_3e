items_dict = dict()
last = 0
for i in range(1 << 16):
    items_dict[i] = True
    if items_dict.allocated() != last:
        print(f"{len(items_dict)}\t{(i-1)*3}\t{items_dict.allocated()=}")
        last = items_dict.allocated()
