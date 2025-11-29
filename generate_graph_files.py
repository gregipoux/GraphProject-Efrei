# generate_graph_files.py

import os
import re

SOURCE = "GrahRecap.txt"
TARGET_DIR = "graphs"

os.makedirs(TARGET_DIR, exist_ok=True)

with open(SOURCE, "r", encoding="utf-8") as f:
    content = f.read()

# découpe sur "Graphe X"
blocks = re.split(r"Graphe\s+(\d+)\s*:", content)

for i in range(1, len(blocks), 2):
    num = blocks[i]
    text = blocks[i + 1]

    # extraction des arcs
    lines = [
        l.strip()
        for l in text.splitlines()
        if "→" in l or "->" in l
    ]

    arcs = []
    for line in lines:
        m = re.search(r"(\d+)\s*[→->]\s*(\d+).*\((?:poids\s*)?(-?\d+)", line)
        if m:
            u, v, w = m.groups()
            arcs.append((int(u), int(v), int(w)))

    if not arcs:
        continue

    max_node = max(max(u, v) for u, v, w in arcs)

    outfile = os.path.join(TARGET_DIR, f"g{num}.txt")
    with open(outfile, "w", encoding="utf-8") as out:
        out.write(str(max_node + 1) + "\n")
        out.write(str(len(arcs)) + "\n")
        for u, v, w in arcs:
            out.write(f"{u} {v} {w}\n")

    print(f"Généré : {outfile}")
