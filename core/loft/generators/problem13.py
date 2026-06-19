from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem13(Generator):
    name = "13"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "topology_variant": StandardParams.TOPOLOGY_VARIANT.value,
    }
    presets = {
        "G1-Sparse": {"clauses": 100, "lengths": [2, 3, 4, 6], "topology_variant": "g1"},
        "G2-Dense": {"clauses": 100, "lengths": [2, 3, 4, 6], "topology_variant": "g2"},
        "G3-Tree": {"clauses": 200, "lengths": [2, 3, 4, 6], "topology_variant": "g3"},
        "G4-Modular": {"clauses": 500, "lengths": [2, 3, 4, 6], "topology_variant": "g4"},
        "G5-Hub": {"clauses": 100, "lengths": [2, 3, 4, 6], "topology_variant": "g5"},
    }

    def validate_extra(self) -> str | None:
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        variant: str = self.params.get("topology_variant")  # type: ignore

        # 1. ustalenie liczby atomów w zależności od topologii grafu
        if variant == "g1":
            # rzadki: liczba atomów równa liczbie klauzul (ratio 1.0)
            num_atoms = total_clauses
        elif variant == "g2":
            # gęsty: zbiór radykalnie mniejszy (np. pierwiastek z liczby klauzul)
            num_atoms = max(3, int(total_clauses ** 0.5))
        else:
            # g3, g4, g5
            num_atoms = max(3, total_clauses // 2)

        atom_names = [f"var{i+1}" for i in range(num_atoms)]
        
        # lista nieużytych atomów do wymuszenia pokrycia 100%
        unused_atoms = list(atom_names)
        self.random.shuffle(unused_atoms)

        # 2. struktury pomocnicze określające pulę powiązań (edges) dla konkretnych grafów
        levels = []
        if variant == "g3":
            num_levels = max(2, num_atoms // 5)
            levels = [[] for _ in range(num_levels)]
            for i, a in enumerate(atom_names):
                levels[i % num_levels].append(a)

        clusters = []
        num_bridges = 0
        if variant == "g4":
            num_clusters = max(2, num_atoms // 5)
            clusters = [[] for _ in range(num_clusters)]
            for i, a in enumerate(atom_names):
                clusters[i % num_clusters].append(a)
            num_bridges = int(total_clauses * 0.10)

        hub_atom = atom_names[0] if variant == "g5" else ""

        # 3. generowanie docelowych długości dla klauzul
        target_lengths = []
        num_per_length = total_clauses // len(clause_lengths)
        for length in clause_lengths:
            target_lengths.extend([length] * num_per_length)
        while len(target_lengths) < total_clauses:
            target_lengths.append(self.random.choice(clause_lengths))
        
        # nie tasujemy długości na tym etapie, aby w G4 "bridge" miały sprawiedliwy rozkład

        clause_assignments: List[List[str]] = []

        # 4. przydzielanie atomów zachowując topologię
        for i, length in enumerate(target_lengths):
            chosen: List[str] = []

            # a) ustalanie dozwolonej puli (pool) na podstawie topologii
            if variant == "g4":
                if i < num_bridges:
                    # most (10%): łączy co najmniej dwa różne klastry
                    c1, c2 = self.random.sample(range(len(clusters)), 2)
                    pool = clusters[c1] + clusters[c2]
                else:
                    # wewnątrz-klastrowe (90%)
                    c = self.random.randint(0, len(clusters) - 1)
                    pool = clusters[c]
            elif variant == "g3":
                # drzewo: łączy atom z poziomu k z k+1
                lvl = self.random.randint(0, len(levels) - 2)
                pool = levels[lvl] + levels[lvl+1]
            else:
                pool = atom_names

            # b) wymuszanie węzła centralnego dla g5
            if variant == "g5":
                chosen.append(hub_atom)
                if hub_atom in unused_atoms:
                    unused_atoms.remove(hub_atom)
                # nie losujemy więcej huba
                pool = [x for x in pool if x != hub_atom]

            # c) priorytetowe ściąganie atomów z puli, które jeszcze nigdy nie wystąpiły
            pool_unused = [a for a in pool if a in unused_atoms]
            while pool_unused and len(chosen) < length:
                a = pool_unused.pop()
                chosen.append(a)
                unused_atoms.remove(a)

            # d) uzupełnianie brakujących miejsc losowo z dozwolonej puli
            needed = length - len(chosen)
            remaining = [a for a in pool if a not in chosen]

            if len(remaining) >= needed:
                chosen.extend(self.random.sample(remaining, needed))
            else:
                chosen.extend(remaining)
                # jeśli długość wymaga więcej literałów niż unikalnych atomów w puli (np. dense graph), pozwalamy na duplikaty
                while len(chosen) < length and pool:
                    chosen.append(self.random.choice(pool))

            clause_assignments.append(chosen)

        # 5. post-processing: wciskanie resztek nieużywanych atomów do pasujących klauzul (kod defensywny)
        for a in unused_atoms:
            if variant == "g3":
                lvl_a = next(j for j, l in enumerate(levels) if a in l)
                pool_idx = max(0, lvl_a - 1)
                pool = levels[pool_idx] + levels[pool_idx+1]
            elif variant == "g4":
                c_a = next(j for j, c in enumerate(clusters) if a in c)
                pool = clusters[c_a]
            else:
                pool = atom_names

            # nadpisujemy całkowicie losową klauzulę
            idx = self.random.randint(0, total_clauses - 1)
            length = target_lengths[idx]
            chosen = [a]
            
            if variant == "g5" and a != hub_atom:
                chosen.append(hub_atom)
                pool = [x for x in pool if x != hub_atom]

            needed = length - len(chosen)
            remaining = [x for x in pool if x not in chosen]
            
            if len(remaining) >= needed:
                chosen.extend(self.random.sample(remaining, needed))
            else:
                chosen.extend(remaining)
                while len(chosen) < length and pool:
                    chosen.append(self.random.choice(pool))
                    
            clause_assignments[idx] = chosen

        # 6. budowanie finalnych tokenów w oparciu o przypisane atomy (rygor 50:50)
        clauses: List[LogicToken] = []
        safety_count = total_clauses // 2

        for i, chosen_atoms in enumerate(clause_assignments):
            is_safety = i < safety_count
            length = len(chosen_atoms)
            
            if is_safety:
                clauses.append(self._generate_safety_clause(length, chosen_atoms))
            else:
                # liveness potrzebuje min. długości 2
                if length < 2:
                    chosen_atoms.append(chosen_atoms[0]) 
                clauses.append(self._generate_liveness_clause(max(2, length), chosen_atoms))

        self.random.shuffle(clauses)
        
        return clauses