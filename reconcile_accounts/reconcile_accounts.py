from datetime import date
from typing import List, Tuple


def reconcile_accounts(l1: List[List[str]], l2: List[List[str]]) -> Tuple[List]:
    def days_diff(d1: str, d2: str):
        t_delta = date.fromisoformat(d1) - date.fromisoformat(d2)

        return abs(t_delta.days)

    def process_result(input_list: List[List[str]], missing_match_idx_list: List[int]):
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

    found_idxs_on_l1_set = set()
    for l1_idx in l1_sorted_idx_list:
        l1_val = l1[l1_idx]
        found_idx_on_l2 = None
        for l2_idx in l2_sorted_idx_list:
            l2_val = l2[l2_idx]
            if l1_val[1:] == l2_val[1:] and days_diff(l1_val[0], l2_val[0]) <= 1:
                found_idxs_on_l1_set.add(l1_idx)
                found_idx_on_l2 = l2_idx
                break
        if found_idx_on_l2 is not None:
            l2_sorted_idx_list.remove(found_idx_on_l2)

    {l1_sorted_idx_list.remove(idx) for idx in found_idxs_on_l1_set}

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
