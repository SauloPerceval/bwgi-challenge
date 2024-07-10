from datetime import date
from typing import List, Tuple


def reconcile_accounts(l1, l2) -> Tuple[List]:
    def days_diff(d1, d2):
        t_delta = date.fromisoformat(d1) - date.fromisoformat(d2)

        return abs(t_delta.days)

    def process_result(input_list, missing_match_idx_list):
        return [
            [*v, "MISSING" if idx in set(missing_match_idx_list) else "FOUND"]
            for idx, v in enumerate(input_list)
        ]

    l1_sorted_idx_list = [
        idx for idx, _ in sorted(enumerate(l1), key=lambda x: x[1][0])
    ]

    l2_sorted_idx_list = [
        idx for idx, _ in sorted(enumerate(l2), key=lambda x: x[1][0])
    ]

    big_l_list, small_l_list = sorted([l1_sorted_idx_list, l2_sorted_idx_list], key=len)
    big_l, small_1 = sorted([l1, l2], key=len)

    found_idxs_on_big_l_set = set()
    for bl_idx in big_l_list:
        bl_val = big_l[bl_idx]
        found_idx_on_small_list = None
        for sl_idx in small_l_list:
            sl_val = small_1[sl_idx]
            if bl_val[1:] == sl_val[1:] and days_diff(bl_val[0], sl_val[0]) <= 1:
                found_idxs_on_big_l_set.add(bl_idx)
                found_idx_on_small_list = sl_idx
                break
        if found_idx_on_small_list is not None:
            small_l_list.remove(found_idx_on_small_list)

    {big_l_list.remove(idx) for idx in found_idxs_on_big_l_set}

    return (
        process_result(l1, l1_sorted_idx_list),
        process_result(l2, l2_sorted_idx_list),
    )


if __name__ == "__main__":

    import csv
    from pathlib import Path
    from pprint import pprint

    transactions1 = list(csv.reader(Path("transactions1.csv").open()))
    transactions2 = list(csv.reader(Path("transactions2.csv").open()))
    out1, out2 = reconcile_accounts(transactions1, transactions2)

    pprint(out1)
    pprint(out2)
