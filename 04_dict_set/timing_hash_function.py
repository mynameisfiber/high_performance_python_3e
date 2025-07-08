import string
import timeit


class BadHash(str):
    def __hash__(self):
        return 42


class GoodHash(str):
    def __hash__(self):
        """
        This is a slightly optimized version of twoletter_hash
        """
        return ord(self[1]) + 26 * ord(self[0]) - 2619


if __name__ == "__main__":
    bad_dict = set()
    good_dict = set()
    list_control = list()
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            key = i + j
            bad_dict.add(BadHash(key))
            good_dict.add(GoodHash(key))
            list_control.append(key)

    bad_time = timeit.repeat(
        "key in bad_dict",
        setup="from __main__ import bad_dict, BadHash; key = BadHash('zz')",
        repeat=3,
        number=1_000_000,
    )
    good_time = timeit.repeat(
        "key in good_dict",
        setup="from __main__ import good_dict, GoodHash; key = GoodHash('zz')",
        repeat=3,
        number=1_000_000,
    )
    list_time = timeit.repeat(
        "key in list_control",
        setup="from __main__ import list_control; key = 'zz'",
        repeat=3,
        number=1_000_000,
    )

    print(f"Min lookup time for bad_dict: {min(bad_time)}")
    print(f"Min lookup time for good_dict: {min(good_time)}")
    print(f"Min lookup time for list_control: {min(list_time)}")

    # Results:
    #    Min lookup time for bad_dict: 10.160735580000619
    #    Min lookup time for good_dict: 0.18675472999893827
    #    Min lookup time for list_control: 8.958332514994254
