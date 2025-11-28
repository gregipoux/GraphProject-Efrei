# run_all_tests.py

import os
from loader import load_graph_from_file
from floyd import floyd_warshall

TEST_DIR = "graphs"

files = sorted(
    [f for f in os.listdir(TEST_DIR) if f.endswith(".txt")],
    key=lambda x: int(''.join(filter(str.isdigit, x)))
)

with open("traces_execution.txt", "w", encoding="utf-8") as out:
    for f in files:
        path = os.path.join(TEST_DIR, f)
        out.write(f"\n===== TEST {f} =====\n")

        try:
            g = load_graph_from_file(path)
        except Exception as e:
            out.write(f"X Erreur chargement : {e}\n")
            continue

        L, P, cycle = floyd_warshall(g.L, g.P, verbose=True)

        if cycle:
            out.write("ATTENTION Cycle négatif détecté\n")
        else:
            out.write("PARFAIT ! Aucun cycle négatif\n")

print("PARFAIT ! Tests terminés — traces dans traces_execution.txt")