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
        variant: str = self.params.get("topology_variant")  # type: ignore
        if variant not in ["g1", "g2", "g3", "g4", "g5"]:
            return f"Topology variant '{variant}' is not supported. Use 'g1', 'g2', 'g3', 'g4', or 'g5'."
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
            # g3, g4, g5: standardowo
            num_atoms = max(3, total_clauses // 2)

        atom_names = [f"var{i+1}" for i in range(num_atoms)]
        
        # lista nieużytych atomów do wymuszenia pokrycia 100%
        unused_atoms = list(atom_names)
        self.random.shuffle(unused_atoms)

        # 2. struktury pomocnicze określające pulę powiązań (edges)
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

        # 4. przydzielanie atomów zachowując rygorystycznie topologię
        for i, length in enumerate(target_lengths):
            chosen: List[str] = []

            # a) ustalanie dozwolonej puli (pool) i pre-wypełnianie
            if variant == "g4":
                if i < num_bridges:
                    # most (10%): musi połączyć co najmniej dwa klastry
                    c1, c2 = self.random.sample(range(len(clusters)), 2)
                    chosen.extend([self.random.choice(clusters[c1]), self.random.choice(clusters[c2])])
                    pool = clusters[c1] + clusters[c2]
                else:
                    # wewnątrz-klastrowe (90%)
                    c = self.random.randint(0, len(clusters) - 1)
                    pool = clusters[c]
            elif variant == "g3":
                # drzewo: musi połączyć poziom k z k+1
                lvl = self.random.randint(0, len(levels) - 2)
                chosen.extend([self.random.choice(levels[lvl]), self.random.choice(levels[lvl+1])])
                pool = levels[lvl] + levels[lvl+1]
            else:
                pool = atom_names

            # b) wymuszanie węzła centralnego dla g5
            if variant == "g5":
                if hub_atom not in chosen:
                    chosen.append(hub_atom)

            chosen = list(set(chosen)) # usunięcie ewentualnych duplikatów z wymuszania

            # usunięcie wybranych z unused_atoms
            for c_atom in chosen:
                if c_atom in unused_atoms:
                    unused_atoms.remove(c_atom)
            
            pool = [x for x in pool if x not in chosen]

            # c) priorytetowe ściąganie atomów z puli, które jeszcze nigdy nie wystąpiły
            pool_unused = [a for a in pool if a in unused_atoms]
            while pool_unused and len(chosen) < length:
                a = pool_unused.pop()
                chosen.append(a)
                unused_atoms.remove(a)
                pool.remove(a)

            # d) uzupełnianie brakujących miejsc losowo z dozwolonej puli
            needed = length - len(chosen)
            if needed > 0:
                if len(pool) >= needed:
                    chosen.extend(self.random.sample(pool, needed))
                else:
                    chosen.extend(pool)
                    full_pool = pool + chosen
                    if not full_pool: 
                        full_pool = atom_names
                    while len(chosen) < length:
                        chosen.append(self.random.choice(full_pool))

            clause_assignments.append(chosen)

        # 5. post-processing: bezpieczne lokowanie resztek w celu zachowania topologii (kod defensywny)
        for a in unused_atoms:
            if variant == "g3":
                lvl_a = next(j for j, l in enumerate(levels) if a in l)
                candidates = [idx for idx, assign in enumerate(clause_assignments) if any(x in levels[lvl_a] for x in assign)]
            elif variant == "g4":
                c_a = next(j for j, c in enumerate(clusters) if a in c)
                candidates = [idx for idx, assign in enumerate(clause_assignments) if any(x in clusters[c_a] for x in assign)]
            else:
                candidates = list(range(total_clauses))

            if candidates:
                idx = self.random.choice(candidates)
                clause_assignments[idx].append(a)
            else:
                clause_assignments[0].append(a)

        # 6. budowanie finalnych tokenów w oparciu o przypisane atomy (rygor 50:50)
        clauses: List[LogicToken] = []
        safety_count = total_clauses // 2

        for i, chosen_atoms in enumerate(clause_assignments):
            is_safety = i < safety_count
            length = len(chosen_atoms)
            
            if is_safety:
                clauses.append(self._generate_safety_clause(length, chosen_atoms))
            else:
                if length < 2:
                    chosen_atoms.append(chosen_atoms[0]) 
                clauses.append(self._generate_liveness_clause(max(2, length), chosen_atoms))

        self.random.shuffle(clauses)
        
        return clauses