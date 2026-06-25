# LOFT

### Autorzy: Emil Wajda, Kacper Wojciuch

---

## Uruchamianie

### Aplikacja webowa - wersja produkcyjna

Jeśli interesuje Cię szybkie uruchomienie aplikacji bez konieczności instalowania dodatkowego oprogramowania,
skorzystaj z tego sposobu.

1. Zainstaluj [Dockera](https://www.docker.com/get-started).
2. Sklonuj to repozytorium i przejdź do jego katalogu głównego.
3. Zbuduj obrazy:
   ```bash
   $ docker compose build base
   $ docker compose --profile tools build
   ```
4. Uruchom aplikację webową:
   ```bash
   $ docker compose up
   ```
5. Otwórz przeglądarkę i przejdź do `http://localhost:8000`.

### Aplikacja webowa - wersja deweloperska

Jeśli chcesz rozwijać aplikację lub wprowadzać w niej zmiany, skorzystaj z tego sposobu.

**Podpowiedź:** użytkownicy [NixOS](https://nixos.org/) mogą wykorzystać plik `shell.nix`, aby łatwo skonfigurować środowisko.

1. Zainstaluj [Pythona](https://www.python.org/downloads/) w wersji **3.13+**.
2. Zainstaluj [NPM](https://nodejs.org/en/download/).
3. Sklonuj to repozytorium i przejdź do jego katalogu głównego.
4. Utwórz i aktywuj wirtualne środowisko Pythona w podfolderze `core`:
   ```bash
   $ python -m venv .venv
   $ source .venv/bin/activate  # Linux/MacOS
   $ .venv\Scripts\activate     # Windows
   ```
5. Zainstaluj zależności Pythona (dalej w katalogu `core`):
   ```bash
   $ pip install .
   ```
6. Przejdź do podfolderu `frontend` i zainstaluj zależności frontendu:
   ```bash
   $ npm install
   ```
7. Uruchom backend oraz frontend:
   ```bash
   $ python -m loft  # W terminalu 1 (katalog core)
   $ npm run dev     # W terminalu 2 (katalog frontend)
   ```
8. Otwórz przeglądarkę i przejdź do `http://localhost:5173`.

Jeśli chcesz również testować benchmarki, będziesz potrzebować Dockera tak czy inaczej.
Możesz wtedy wybiórczo budować tylko potrzebne obrazy Dockera. Na przykład, aby zbudować obraz z proverem Vampire, użyj:

```bash
$ docker compose build vampire
```

### Interfejs wiersza poleceń (CLI)

Jeśli wolisz korzystać z niektórych funkcjonalności aplikacji w trybie konsolowym (np. do szybkich testów), skorzystaj z tego sposobu.

Moduł backendowy posiada wbudowaną pomoc odnośnie dostępnych poleceń. W zależności od dostępnego środowiska,
użyj jednej z poniższych komend:

```bash
$ python -m loft --help                # Środowisko deweloperskie
$ docker compose run --rm core --help  # Środowisko produkcyjne
```

## Przewodnik użytkownika

Niniejsza sekcja przedstawia podstawy korzystania z aplikacji webowej LOFT. Interfejs składa się z paska
bocznego po lewej stronie oraz głównego obszaru roboczego po prawej.

### Tworzenie i wybór workspace

Po uruchomieniu aplikacji należy najpierw utworzyć lub wybrać przestrzeń roboczą (workspace). W pasku bocznym
znajduje się przycisk "Create Workspace" służący do utworzenia nowego workspace.
Po utworzeniu pojawi się na liście i można go rozwinąć, aby zobaczyć dostępne zakładki:
**Settings**, **Generator**, **Benchmark** oraz **Results**.
Przestrzeni roboczej można zmienić nazwę (ikona ołówka) lub ją usunąć (ikona kosza z potwierdzeniem).

### Konfiguracja ustawień (Settings)

![Widok ustawień workspace](images/settings.png)

Zakładka **Settings** umożliwia konfigurację następujących parametrów:

- **Seed Configuration** - wybór między losowym seedem (każde generowanie da inne wyniki)
  a stałym seedem (powtarzalne eksperymenty),
- **Prover Timeout** - maksymalny czas w sekundach, jaki prover ma na rozwiązanie problemu.
  Po przekroczeniu tego czasu wynik zostanie oznaczony jako `TIMEOUT`,
- **Enable Generator Checks** - opcjonalne sprawdzanie składni TPTP wygenerowanych plików, domyślnie włączone.

Po wprowadzeniu zmian należy kliknąć przycisk **Save Settings**.

### Generowanie problemów (Generator)

![Widok zakładki Generator](images/generate_problems.png)

Zakładka **Generator** wyświetla listę wszystkich wygenerowanych problemów w danym workspace,
pogrupowanych według typu problemu. Każdy problem pokazuje swoje parametry oraz seed użyty do generowania.
Problemom można zmieniać nazwę (ikona ołówka) lub je usuwać (ikona kosza).

Aby wygenerować nowy problem, należy kliknąć przycisk **Generate Problems** w prawym górnym rogu.

![Formularz generowania problemu](images/generate_problems_form.png)

Otworzy się modal z formularzem, w którym można:

1. **Wybrać typ problemu** - z listy rozwijanej (Problem 1-18, w tym 9a i 9b),
2. **Wybrać preset** - predefiniowany zestaw parametrów (np. Default, Short, Long),
3. **Dostosować parametry** - każdy typ problemu ma swoje specyficzne parametry,
   takie jak liczba klauzul, długości klauzul, rozkład itp.

Po skonfigurowaniu parametrów kliknięcie **Generate** utworzy nowy plik TPTP w workspace.

### Uruchamianie benchmarków (Benchmark)

![Widok zakładki Benchmark](images/benchmark_view.png)

Zakładka **Benchmark** służy do konfiguracji i uruchamiania testów wydajnościowych. Interfejs składa się z dwóch sekcji:

**Wybór problemów:**

- Problemy są pogrupowane według typu (problem_1, problem_2 itd.),
- Można rozwinąć grupę klikając na jej nazwę,
- Zaznaczanie/odznaczanie problemów odbywa się przez kliknięcie na dany problem,
- Przycisk "Select/Deselect All" zaznacza lub odznacza wszystkie problemy w grupie.

**Wybór proverów:**

- Na dole ekranu znajduje się lista checkboxów z dostępnymi proverami (Vampire, SPASS, E, iProver, Prover9, Z3, CVC4, CVC5, Drodi, InKreSAT),
- Należy zaznaczyć co najmniej jeden prover.

Po wybraniu problemów i proverów kliknięcie **Run Benchmark** uruchomi testy.
Aplikacja automatycznie przejdzie do zakładki Results i będzie wyświetlać wyniki w czasie rzeczywistym.

### Przeglądanie wyników (Results)

![Lista wyników benchmarków](images/results_view.png)

Zakładka **Results** wyświetla listę wszystkich przeprowadzonych benchmarków z informacjami:

- Data/ID benchmarku (lub "Ongoing..." dla trwających),
- Lista użytych proverów,
- Liczba testowanych problemów (z tooltipem wyświetlającym wszystkie ścieżki).

Kliknięcie **View Report** otwiera szczegółowy widok wybranego benchmarku.
Dla zakończonych benchmarków dostępne są także przyciski **Rename** oraz **Delete** umożliwiające
zmianę nazwy pliku lub usunięcie wyniku.

![Szczegółowy widok wyników](images/results.png)

Widok szczegółowy prezentuje tabelę z wynikami dla każdej kombinacji problem × prover:

- **Result** - wynik provera (`SATISFIABLE`, `UNSATISFIABLE`, `UNKNOWN`, `TIMEOUT`, `UNCONVERTED`),
- **Real Time** - rzeczywisty czas wykonania w sekundach,
- **System Time** - czas procesora w sekundach,
- **Memory** - szczytowe zużycie pamięci w KB.

Wyniki są kolorowane dla łatwiejszej interpretacji:

- Zielony = `SATISFIABLE`,
- Czerwony = `UNSATISFIABLE`,
- Żółty = `UNKNOWN` (np. błąd provera) lub `UNCONVERTED` (nieudana konwersja formatu),
- Szary = `TIMEOUT` lub w trakcie.

### Wykresy porównawcze

![Wykresy wyników](images/charts.png)

Pod tabelą wyników znajdują się interaktywne wykresy umożliwiające analizę porównawczą:

- **Wybór parametru (oś X)** - można wybrać parametr problemu (np. liczba klauzul),
  względem którego będą prezentowane wyniki,
- **Metryki (oś Y)** - czas systemowy, czas rzeczywisty lub zużycie pamięci,
- **Osobne trzy wykresy dla każdego provera** - pozwala łatwo porównać wydajność różnych proverów
  w zależności od parametrów problemu.

Wykresy są szczególnie przydatne do analizy skalowalności proverów - jak zmienia się czas
rozwiązywania w zależności od rozmiaru problemu.

## Struktura projektu

Najważniejszymi ścieżkami w projekcie są:

- `core/` - moduł backendowy napisany w Pythonie, zawierający logikę generowania formuł, zarządzania benchmarkami poprzez
  uruchamianie kontenerów Dockera na żądanie oraz API dla frontendu,
- `frontend/` - moduł frontendowy napisany w [TypeScript](https://www.typescriptlang.org/) z wykorzystaniem frameworka
  [Vite](https://vite.dev/) + [React](https://react.dev/), zawierający interfejs użytkownika aplikacji webowej,
- `provers/` - katalog zawierający pliki Dockerfile dla poszczególnych proverów,
- `tools/` - dodatkowe narzędzia (sprawdzanie składni TPTP oraz konwertery formatów), również oparte na Dockerze,
- `workspaces/` - przestrzenie robocze, które wykorzystuje projekt do przechowywania swoich rezultatów
  (np. wygenerowane formuły, wyniki benchmarków).
- `docker-compose.yml` - plik konfiguracyjny [Docker Compose](https://docs.docker.com/compose/), definiujący usługi
  i obrazy potrzebne do uruchomienia aplikacji oraz proverów.

## Struktura `workspaces`

Katalog `workspaces/` zawiera podkatalogi, które są tworzone w momencie, gdy użytkownik sobie tego zażyczy.
Każdy katalog reprezentuje jedną przestrzeń roboczą, w której mogą być przechowywane formuły, ustawienia oraz
wyniki benchmarków. Struktura katalogu przestrzeni roboczej jest następująca:

- `settings.json` - plik konfiguracyjny przestrzeni roboczej, zawierający informacje o seedzie generatora
  formuł, czasie przerwania działania proverów (timeout) oraz opcjonalnej fladze sprawdzania składni,
- `problem_1/`, `problem_2/`, ... - podkatalogi reprezentujące poszczególne typy problemów logicznych,
  zawierające jedynie pliki w formacie TPTP - nazwy plików są bez znaczenia, ważne jest jedynie rozszerzenie
  oraz ich zawartość z poprawnym komentarzem zawierającym informacje o parametrach generatora,
- `convertion_cache/` - katalog przechowujący pliki w formatach innych niż TPTP, wygenerowane
  przez konwertery - aby uniknąć wielokrotnego konwertowania tych samych plików, pliki te polegają na hashach
  (skrótach) oryginalnych plików TPTP,
- `results/` - katalog przechowujący wyniki uruchomień proverów na formułach z danej przestrzeni roboczej.

## Budowanie obrazów Dockera

Projekt polega na jednym bazowym obrazie Dockera (`base`), który zawiera wspólne zależności dla wszystkich proverów.
Z kolei sam obraz bazowy dziedziczy po obrazie [`nixos/nix`](https://hub.docker.com/r/nixos/nix).
Wybór tego obrazu został podyktowany klikoma powodami:

- Nix stawia na powtarzalność budowania oprogramowania, co daje nam jeszcze silniejszą gwarancję, że projekt będzie
  można zbudować nawet po wielu latach, nie martwiąc się o zmieniające się zależności systemowe - w celu aktualizacji
  oprogramowania wewnątrz wszystkich kontenerów, należy jedynie zmienić commit kanału `nixpkgs`,
  ustawiony na stałe właśnie w obrazie `base`,
- pliki konfiguracyjne `.nix` są pisane w deklaratywnym, funkcyjnym języku, co ułatwia wyrażenie logiki związanej
  z budowaniem pakietów i jest mniej podatne na błędy niż tradycyjne skrypty pisane w Bashu,
- wiele spośród wykorzystywanych przez nas narzędzi (np. proverów) jest już dostępnych w `nixpkgs`, co upraszcza
  proces ich instalacji i zarządzania wersjami.

Jak już wspomniano, każdy obraz w projekcie dziedziczy po obrazie `base` i instaluje jedynie specyficzne dla siebie
dependencje. Jeśli jest to konieczne, dostarczone są również skrypty procesu budowy danego pakietu (pliki `.nix`)
oraz ewentualne pliki `entrypoint.sh`, modyfikujące domyślne zachowanie kontenera przy jego uruchomieniu.

Plik `docker-compose.yml` definiuje wszystkie obrazy oraz usługi potrzebne do uruchomienia aplikacji. Mimo to,
jedynym serwisem uruchamianym na stałe przy użyciu komendy `docker compose up` jest `core` (backend aplikacji webowej).
Jest to celowe działanie, mające na celu oszczędność zasobów systemowych - provery i narzędzia są uruchamiane
dopiero na żądanie użytkownika, poprzez interfejs webowy lub CLI. Takie zachowanie zostało osiągnięte dzięki
opcji `profiles` w Docker Compose oraz udostępnieniu socketu Dockera wewnątrz kontenera `core`
(`/var/run/docker.sock` w `volumes`). Dzięki temu, nie jest konieczne stosowanie podejścia opartego na
mikroserwisach i udostępniania nadmiarowych interfejsów sieciowych między kontenerami (to podejście było
stosowane w projekcie przed jego całkowitym przepisaniem).

Warto również wspomnieć o procesie budowania obrazu `core` - w tym przypadku wykorzystano mechanizm budowania
wieloetapowego ([multi-stage build](https://docs.docker.com/build/building/multi-stage/)), aby móc połączyć
w jednym obrazie zarówno aplikację backendową (Python), jak i frontendową (Node.js). Wspiera to również
cache'owanie warstw Dockera, co przyspiesza proces budowania obrazu podczas wprowadzania zmian w kodzie źródłowym
aplikacji - był to jeden z celów, który dyktował również niektóre nadmiarowe polecenia w rozmaitych plikach `Dockerfile`.

## Backend aplikacji

Backend aplikacji LOFT został zaimplementowany w języku **Python 3.13+** z wykorzystaniem asynchronicznego
frameworka webowego [Quart](https://quart.palletsprojects.com/). Kod źródłowy znajduje się w katalogu `core/loft/`.

### Zależności

Plik `pyproject.toml` definiuje następujące główne zależności:

- **Quart** (`>=0.20.0`) - asynchroniczny framework webowy oparty na ASGI, kompatybilny z Flask,
- **aiofiles** (`>=24.1.0`) - biblioteka do asynchronicznego I/O na plikach.

### Struktura modułów

#### Moduł główny (`main.py`, `cli.py`)

- `main.py` - punkt wejścia aplikacji, definiuje parser argumentów CLI oraz uruchamia odpowiedni tryb działania
  (serwer deweloperski, generowanie problemów, uruchamianie benchmarków, sprawdzanie składni TPTP),
- `cli.py` - implementacja funkcji wywoływanych przez interfejs wiersza poleceń (`check`, `benchmark`, `generate`).

#### Moduł Docker (`docker.py`)

Zawiera funkcje do asynchronicznego uruchamiania kontenerów Docker:

- `run_docker_container()` - uruchamia kontener z podanym obrazem, przekazując dane przez stdin i odbierając stdout/stderr,
- `run_tptp_checker()` - wrapper do uruchamiania narzędzia sprawdzającego składnię TPTP.

#### Moduł formuł logicznych (`formulas.py`)

Definiuje struktury danych reprezentujące formuły logiki pierwszego rzędu (FOL) za pomocą dataclass:

- `LogicToken` - abstrakcyjna klasa bazowa z metodą `to_tptp()`,
- `Atom` - atom logiczny z nazwą i parametrem,
- `Not`, `Alternative`, `Conjunction`, `Implication` - operatory logiczne,
- `ForAll`, `Exists` - kwantyfikatory,
- `GreaterThan` - predykat porównania.

Każda klasa implementuje metodę `to_tptp()` zwracającą reprezentację w formacie TPTP.

#### Moduł budowania TPTP (`tptp_builder.py`)

Klasa `TPTPBuilder` odpowiada za:

- budowanie pojedynczych wpisów FOF w formacie TPTP,
- konwersję listy klauzul `LogicToken` na pełny string TPTP,
- dodawanie metadanych (nazwa problemu, parametry, seed) jako komentarz JSON.

#### Moduł generatorów (`generators/`)

Pakiet zawierający logikę generowania problemów logicznych:

- `generator.py` - abstrakcyjna klasa bazowa `Generator` definiująca interfejs generatorów:
  - walidacja parametrów wejściowych,
  - metody pomocnicze do generowania klauzul bezpieczeństwa i żywotnościowych,
  - sugerowanie ścieżki zapisu pliku,
- `param_spec.py` - specyfikacje typów parametrów (`Integer`, `Float`, `Boolean`, `Choice`, `IntegerList`)
  z walidacją i serializacją,
- `std_params.py` - predefiniowane, często używane parametry jako enum `StandardParams`,
- `problem1.py` - `problem18.py` - konkretne implementacje generatorów dla 18 różnych typów problemów logicznych (w tym `problem9a.py` i `problem9b.py`).

Każdy generator definiuje:

- `name` - identyfikator problemu,
- `param_spec` - słownik specyfikacji parametrów,
- `presets` - predefiniowane zestawy parametrów,
- `validate_extra()` - dodatkowa walidacja międzyparametrowa,
- `generate()` - metoda zwracająca listę klauzul `LogicToken`.

#### Moduł proverów (`provers/`)

Pakiet obsługujący uruchamianie automatycznych dowodzicieli:

- `prover.py` - klasa `Prover` odpowiedzialna za:
  - uruchamianie provera na pliku problemu,
  - konwersję formatu (jeśli prover wymaga innego formatu niż TPTP),
  - cache'owanie skonwertowanych plików (w katalogu `convertion_cache/`),
- `run_output.py` - definicje wyników uruchomienia:
  - `RunResult` - enum z możliwymi wynikami (`SAT`, `UNSAT`, `UNKNOWN`, `TIMEOUT`),
  - `RunStats` - statystyki wykonania (czas systemowy, czas rzeczywisty, szczytowe zużycie pamięci),
  - `basic_result_parser()` - fabryka parserów wyjścia proverów,
- `__init__.py` - rejestr wszystkich wspieranych proverów w słowniku `KNOWN_PROVERS`.

#### Moduł benchmarków (`benchmarks.py`)

Zarządza asynchronicznym uruchamianiem benchmarków:

- `BenchmarkCell` - pojedyncza komórka wyniku (problem × prover),
- `BenchmarkResult` - pełny wynik benchmarku z timestampem i listą komórek,
- `BenchmarkOrchestrator` - koordynator benchmarków wspierający:
  - równoległe uruchamianie wielu testów,
  - streaming wyników w czasie rzeczywistym przez WebSocket,
  - zapisywanie wyników do plików JSON.

#### Moduł Web API (`web_api/`)

REST API aplikacji zbudowane na frameworku Quart:

- `__init__.py` - inicjalizacja aplikacji Quart, rejestracja tras, endpoint `/api/provers`,
- `workspaces.py` - zarządzanie przestrzeniami roboczymi (CRUD),
- `settings.py` - odczyt/zapis ustawień workspace (seed, timeout, check),
- `problems.py` - zarządzanie problemami (lista, generowanie, usuwanie),
- `results.py` - zarządzanie benchmarkami (lista, tworzenie, WebSocket do streamingu wyników).

### Endpointy API

| Metoda | Ścieżka                         | Opis                            |
| ------ | ------------------------------- | ------------------------------- |
| GET    | `/api/provers`                  | Lista dostępnych proverów       |
| GET    | `/api/workspaces`               | Lista workspace'ów              |
| POST   | `/api/workspaces`               | Tworzenie workspace             |
| PUT    | `/api/workspaces`               | Zmiana nazwy workspace          |
| DELETE | `/api/workspaces`               | Usuwanie workspace              |
| GET    | `/api/workspaces/<ws>/settings` | Ustawienia workspace            |
| PUT    | `/api/workspaces/<ws>/settings` | Aktualizacja ustawień           |
| GET    | `/api/problems`                 | Definicje typów problemów       |
| GET    | `/api/workspaces/<ws>/problems` | Lista problemów w workspace     |
| POST   | `/api/workspaces/<ws>/problems` | Generowanie problemu            |
| PUT    | `/api/workspaces/<ws>/problems` | Zmiana nazwy pliku problemu     |
| DELETE | `/api/workspaces/<ws>/problems` | Usuwanie problemu               |
| GET    | `/api/workspaces/<ws>/results`  | Lista benchmarków               |
| POST   | `/api/workspaces/<ws>/results`  | Uruchomienie benchmarku         |
| PUT    | `/api/workspaces/<ws>/results`  | Zmiana nazwy wyniku benchmarku  |
| DELETE | `/api/workspaces/<ws>/results`  | Usuwanie wyniku benchmarku      |
| WS     | `/ws/workspaces/<ws>/results`   | WebSocket do streamingu wyników |

## Frontend aplikacji

Frontend aplikacji LOFT został zaimplementowany w języku **TypeScript** z wykorzystaniem frameworka
[React](https://react.dev/) oraz narzędzia budowania [Vite](https://vite.dev/).
Kod źródłowy znajduje się w katalogu `frontend/src/`.

### Zależności

Plik `package.json` definiuje następujące główne zależności:

- **React** - biblioteka do budowania interfejsów użytkownika,
- **@tanstack/react-query** - zarządzanie stanem serwera, cache'owanie zapytań i mutacje,
- **axios** - klient HTTP do komunikacji z API,
- **chart.js** + **react-chartjs-2** - biblioteka do tworzenia wykresów,
- **lucide-react** - ikony w stylu Lucide,
- **react-use-websocket** - hook do obsługi WebSocket,
- **TailwindCSS** - framework CSS utility-first.

Zależności deweloperskie obejmują TypeScript, ESLint oraz Vite.

### Struktura komponentów

#### Komponent główny (`App.tsx`)

Główny komponent aplikacji odpowiedzialny za:

- zarządzanie stanem aktywnego workspace i zakładki,
- routing między widokami (Settings, Generator, Benchmark, Results),
- renderowanie paska bocznego i głównej zawartości.

#### Typy danych (`types.ts`)

Definicje interfejsów TypeScript odpowiadających strukturom danych z API:

- `ParamSpec`, `ProblemType`, `ProblemTypeList` - specyfikacje typów problemów,
- `Problem`, `ProblemFileList` - problemy i ich parametry,
- `ResultSummary`, `ResultCell`, `RunStats` - wyniki benchmarków,
- `WorkspaceSettings` - ustawienia workspace,
- `TabName` - nazwy zakładek w interfejsie.

#### Komponenty Sidebar (`components/Sidebar/`)

Pasek boczny aplikacji:

- `Sidebar.tsx` - główny kontener z listą workspace'ów,
- `SidebarHeader.tsx` - nagłówek z logo LOFT,
- `WorkspaceItem.tsx` - element listy z rozwijalnymi zakładkami, możliwością zmiany nazwy i usuwania,
- `SidebarTab.tsx` - pojedyncza zakładka (Settings, Generator, Benchmark, Results),
- `CreateWorkspace.tsx` - formularz tworzenia nowego workspace.

#### Komponenty Settings (`components/Settings/`)

- `SettingsView.tsx` - widok ustawień workspace:
  - konfiguracja seeda generatora (losowy/stały),
  - ustawienie timeoutu dla proverów,
  - przełącznik sprawdzania składni TPTP przy generowaniu.

#### Komponenty Generator (`components/Generator/`)

- `GeneratorView.tsx` - główny widok zakładki Generator z listą problemów i przyciskiem generowania,
- `ProblemList.tsx` - lista wygenerowanych problemów pogrupowana według typu, z możliwością zmiany nazwy i usuwania,
- `CreateProblemModal.tsx` - modal do tworzenia nowego problemu:
  - wybór typu problemu,
  - konfiguracja parametrów z presetami,
  - dynamiczne formularze dla różnych typów parametrów.

#### Komponenty Benchmark (`components/Benchmark/`)

- `BenchmarkView.tsx` - widok konfiguracji benchmarku:
  - wybór problemów do testowania (z grupowaniem według typu),
  - wybór proverów,
  - uruchamianie benchmarku.

#### Komponenty Results (`components/Results/`)

- `ResultListView.tsx` - lista wszystkich benchmarków w workspace z możliwością przeglądania szczegółów, zmiany nazwy i usuwania,
- `ResultView.tsx` - szczegółowy widok pojedynczego benchmarku:
  - tabela wyników (problem × prover),
  - statystyki wykonania (czas, pamięć),
  - streaming wyników w czasie rzeczywistym przez WebSocket,
- `ResultCharts.tsx` - interaktywne wykresy porównawcze:
  - wizualizacja zależności metryk od parametrów problemów,
  - wybór osi X (parametr problemu).

#### Komponent Notification (`components/Notification.tsx`)

Wyświetla powiadomienia o sukcesie/błędzie operacji w górnej części ekranu.

### Custom Hooks (`hooks/`)

Własne hooki React do zarządzania stanem i komunikacji z API:

- `useActiveWorkspace.tsx` - Context API do zarządzania aktywnym workspace,
- `useNotificationContext.tsx` - Context API do wyświetlania powiadomień,
- `useWorkspaces.tsx` - hook do CRUD na workspace'ach,
- `useProblems.tsx` - hook do zarządzania problemami (lista, generowanie, usuwanie),
- `useProblemTypes.tsx` - hook pobierający definicje typów problemów z API,
- `useMutationNotify.tsx` - wrapper na `useMutation` z automatycznymi powiadomieniami o sukcesie/błędzie.

### Narzędzia pomocnicze (`utils.tsx`)

- `PrettyPrintParams()` - komponent formatujący parametry problemu,
- `splitPath()`, `groupProblems()` - funkcje do grupowania problemów według katalogów.

## Informacje o proverach

Obrazy Dockera dla poszczególnych proverów zawierają specyficzne podejście do ich uruchamiania.
Używany jest plik `entrypoint.sh`, który:

- wczytuje plik ze standardowego wejścia i zapisuje go do pliku tymczasowego o nazwie `input`,
- przekierowuje ewentualne błędy (stderr) do standardowego wyjścia (stdout), aby nie było konfliktu w następnym kroku,
- uruchamia komendę startową provera opakowując ją w wywołanie [GNU Time](https://www.gnu.org/software/time/)
  w celu zmierzenia czasu wykonania oraz zużycia pamięci - narzędzie to zapisuje swoje wyniki do stderr.

Lista wspieranych proverów wraz z ich krótkim opisem:

- [Vampire](https://github.com/vprover/vampire):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie TPTP,
- [SPASS](https://en.wikipedia.org/wiki/SPASS):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie TPTP po sprecyzowaniu opcji `-TPTP`,
- [E Prover](https://github.com/eprover/eprover):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie TPTP,
- [iProver](https://gitlab.com/korovin/iprover):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie TPTP, ale wymaga "uproszczonej postaci",
  - używany jest konwerter zamieniający formuły FOF na CNF (`tools/cnf`),
- [Prover9](https://www.cs.unm.edu/~mccune/prover9/):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w swoim własnym formacie (LADR),
  - używany jest konwerter dostarczony wraz z Prover9 (`tools/ladr`),
- [Z3](https://github.com/Z3Prover/z3):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie SMT-LIB2,
  - używany jest konwerter zbudowany w `tools/smt2`,
- [CVC4](https://cvc4.github.io/):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie TPTP (z odpowiednimi opcjami linii komend),
- [CVC5](https://github.com/cvc5/cvc5):
  - wersja z `nixpkgs`,
  - przyjmuje formuły w formacie SMT-LIB2 (o dziwo przestali wspierać format TPTP),
- [Drodi](https://tptp.org/CASC/29/SystemDescriptions.html#Drodi---3.5.1):
  - brak jakiegokolwiek kodu źródłowego lub paczki w `nixpkgs`,
  - plik wykonywalny pobierany z repozytorium GitHub projektu [StarExec](https://github.com/StarExecMiami/StarExec-ARC/tree/master/provers-containerised/provers/Drodi---3.6.0), pobierany automatycznie przy budowie za pomocą Nixa,
  - przyjmuje formuły w formacie TPTP,
- [InKreSAT](https://www.ps.uni-saarland.de/~kaminski/inkresat/):
  - wersja z własnego pliku `.nix`, budowana ze źródeł,
  - przyjmuje formuły w formacie własnym,
  - jest to prover formuł logiki modalnej, a nie FOF jak reszta,
  - używany jest konwerter napisany w `tools/inkresat-converter`.

## Informacje o narzędziach

### Sprawdzanie składni TPTP

Do dodatkowego sprawdzania składni formuł w formacie TPTP używamy własnego narzędzia w folderze `tools/tptp-checker`.
Narzędzie to jest napisane w Rust'cie ze względu na istnienie biblioteki [`tptp`](https://crates.io/crates/tptp),
polecanej przez samego prof. Geoffa Sutcliffe'a, która umożliwia łatwe parsowanie składni TPTP. Poprzez użycie
Rusta, uzyskujemy też dodatkową korzyść w postaci szybkości i poprawności działania kodu.

W momencie pisania tego narzędzia, wydawał się to jedyny sensowny sposób, gdyż zawiodły nas inne skrypty
lub programy znalezione w Internecie (brak pełnego wsparcia dla FOF w TPTP, długie czasy pobierania,
długie czasy działania dla większych problemów, etc.).

### Konwerter CNF

Konwerter formuł do postaci CNF znajduje się w folderze `tools/cnf` - mimo iż nazwa może brzmieć strasznie,
pod tym konwerterem kryje się `vampire` z odpowiednimi opcjami linii komend służącymi do operacji `clausify`.

### Konwerter LADR

Konwerter formuł do formatu LADR z folderze `tools/ladr` również jest bardzo prosty w użyciu, gdyż dostarczają
go sami autorzy Prover9 wraz z resztą pakietu.

### Konwerter SMT2

W celu konwersji formuł do formatu SMT-LIB2, wykorzystujemy narzędzie prof. Geoffa Sutcliffe'a, `tptp4X`.
Mimo iż pełny pakiet narzędzi TPTP jest dostępny w `nixpkgs`, polega on na pobraniu gotowych plików binarnych
z serwera strony TPTP, który ewidentnie ma zbyt małą przepustowość (pobieranie trwało nawet kilka godzin).
W związku z tym dostarczyliśmy własny plik `.nix`, który kompiluje `tptp4X` ze źródeł.

### Konwerter InKreSAT

Konwerter formuł do formatu InKreSAT znajduje się w folderze `tools/inkresat-converter` i jest narzędziem
napisanym w Rust'cie. Konwertuje on formuły z formatu TPTP na format natywny akceptowany przez prover InKreSAT,
zachowując przy tym semantykę oryginalnej formuły. Rust został wybrany z podobnych względów jak w przypadku
narzędzia do sprawdzania składni TPTP.

Konwersja większości operatorów jest trywialna - tłumaczą się one dosłownie na odpowiednie symbole w formacie InKreSAT. 
Mimo to, warto wyróżnić kilka nietypowych zachowań konwertera:

- kwantyfikatory mają specjalne reguły klasyfikujące je jako klauzule typu "safety" lub "liveness", po czym ich
  składnia jest zamieniana na równoważne operacje logiki modalnej InKreSATa,
- predykaty/wywołania funkcji są zamieniane na zwykłe atomy zdaniowe o odpowiednich alfanumerycznych nazwach,
- konwertowane są tylko wyrażenia typu "axiom".

## Dostępne typy problemów

Poniżej znajduje się lista wszystkich dostępnych typów problemów wraz ze szczegółowym opisem.

---

### P01. Wpływ wielkości formuły na czas/pamięć - równe liczby klauzul tej samej długości

Generujemy formuły testowe składające się z 50, 100, 200, 500, 1000 lub 2000 klauzul. Każda formuła składa się w połowie z klauzul żywotnościowych (liveness) i w połowie z klauzul bezpieczeństwa (safety). Klauzule generowane są o długościach 2, 3, 4, 6, 8, 10 - w równej liczbie dla każdej grupy. Formuły generowane są nad liczbą atomów równą liczbie klauzul podzielonej przez 2.

**Parametry:** `clauses` (int), `lengths` (int list)

---

### P02. Wpływ wielkości formuły na czas/pamięć - rozkład Poissona

Problem podobny do P01, jednak liczba klauzul w poszczególnych grupach długości wynika z rozkładu Poissona o zadanej wartości oczekiwanej lambda (oczekiwana długość klauzuli).

**Parametry:** `clauses` (int), `lambda` (float)

---

### P03. Wpływ wielkości formuły na czas/pamięć - różne stosunki atomów do klauzul

Generujemy formuły testowe o zadanej liczbie klauzul, badając wpływ stosunku liczby atomów do liczby klauzul (wartości 2, 3, 4, 5, 10). Maksymalna długość klauzuli jest ograniczona przez liczbę wszystkich atomów podzieloną przez liczbę klauzul.

**Parametry:** `clauses` (int), `ratio` (float)

---

### P04. Wpływ wielkości formuły na czas/pamięć - stałe długości klauzul

Wszystkie klauzule w formule mają tę samą, stałą długość (kolejno: 2, 3, 4, 5). Badamy wpływ jednolitej długości klauzul na wydajność proverów.

**Parametry:** `clauses` (int), `length` (int)

---

### P05. Wpływ wielkości formuły na czas/pamięć - grupy stałych długości klauzul

Wszystkie klauzule w pojedynczej formule mają stałą długość (1, 5, 10 lub 20). Rozpatrywane są trzy przypadki rozkładu: (a) wszystkie grupy po 25%, (b) klauzule o długości 1 stanowią 1% - reszta po równo, (c) klauzule o długości 20 stanowią 1% - reszta po równo.

**Parametry:** `clauses` (int), `lengths` (int list), `distribution` (choice: even/tiny_short/tiny_long)

---

### P06. Wpływ współczynnika liveness/safety na czas/pamięć

Badamy wpływ proporcji klauzul żywotnościowych do bezpieczeństwa na wydajność. Rozpatrywane stosunki: 90:10, 80:20, 65:35, 50:50, 35:65, 20:80, 10:90. Dostępny jest również wariant z rozkładem Poissona.

**Parametry:** `clauses` (int), `safety_percentage` (float), `poisson` (bool), `lambda` (float), `lengths` (int list)

---

### P07. Łączenie kilku prostych formuł - wpływ na czas/pamięć

Generujemy trzy formuły $F_1, F_2, F_3$ (każda składa się z zadanej liczby klauzul), które łączymy alternatywą lub koniunkcją, otrzymując $G$. Testowaniu poddawana jest formuła $G \Rightarrow R$, gdzie $R$ to prosta klauzula żywotnościowa zbudowana z atomów użytych w $G$. Liczby klauzul dla $F_1, F_2, F_3$: kolejno 50, 100, 200.

**Parametry:** `clauses` (int), `poisson` (bool), `conjunction` (bool), `lambda` (float), `lengths` (int list)

---

### P08. Porównanie formuł - kwadrat logiczny

Generujemy dwie formuły $F_1$ i $F_2$ (liczba klauzul: 50, 100, 200, 500, 1000). Testowane są trzy relacje logiczne:

- **contradictory:** $(F_1 \Rightarrow \neg F_2) \land (\neg F_1 \Rightarrow F_2)$
- **subcontrary:** $\neg(\neg F_1 \land \neg F_2)$
- **subalternated:** $(F_1 \Rightarrow F_2) \land \neg(F_2 \Rightarrow F_1)$

Dostępny jest również wariant z rozkładem Poissona.

**Parametry:** `clauses` (int), `poisson` (bool), `mode` (choice: contradictory/subcontrary/subalternated), `lambda` (float), `lengths` (int list)

---

### P09. Warianty kwadratu logicznego - asymetria

Kontynuacja problemu P08, badanie wpływu asymetrii strukturalnej i semantycznej na relacje z kwadratu logicznego.

**P09a. Asymetria strukturalna (różna złożoność)**

Badanie relacji subalternacji między formułami o istotnie różnej złożoności. Generujemy $F_1, F_2$ o różnej liczbie klauzul: $F_1$ — 50, 100, 200; $F_2$ — 500, 1000, 2000. Proporcja liveness/safety: 50:50. Każdy atom występuje co najmniej raz.

**Parametry:** `clauses_f1` (int), `clauses_f2` (int), `lengths` (int list), `mode` (choice)

**P09b. Asymetria semantyczna (liveness vs safety)**

Badanie wpływu dominującego typu własności w formułach na relacje logiczne. Dwa przypadki:

- case1: $F_1$ — 80% safety, 20% liveness; $F_2$ — 20% safety, 80% liveness
- case2: $F_1$ — 20% safety, 80% liveness; $F_2$ — 80% safety, 20% liveness

Testowane relacje: sprzeczność (T1) i subalternacja (T2). Liczba klauzul: 50, 100, 200, 500.

**Parametry:** `clauses` (int), `lengths` (int list), `mode` (choice), `semantic_case` (choice: case1/case2)

---

### P10. Ewolucja modeli behawioralnych

Badanie wpływu zmian w modelu na relacje logiczne między jego kolejnymi wersjami. Generujemy formułę bazową $F_1$ (100, 200 lub 500 klauzul). Tworzymy $F_2$ przez modyfikację $p\%$ klauzul. Zmiana klauzuli oznacza losowo:

- **M1:** usunięcie klauzuli
- **M2:** dodanie nowej klauzuli
- **M3:** zamiana klauzuli na nową

Zbiór atomów oraz proporcja liveness/safety (50:50) pozostają zachowane. Dla każdej pary $(F_1, F_2)$ testujemy relacje: R1 $(F_1 \Rightarrow F_2)$, R2 $(F_2 \Rightarrow F_1)$, R3 $(F_1 \land \neg F_2)$, R4 $(F_1 \land F_2)$.

**Parametry:** `clauses` (int), `lengths` (int list), `modification_percent` (float), `evolution_mode` (choice: r1-r4)

---

### P11. Kontrolowana redundancja specyfikacji

Badanie wpływu nadmiarowych klauzul na relacje logiczne oraz koszt wnioskowania. Generujemy formułę bazową $F$ (100, 200, 500 lub 1000 klauzul), a następnie tworzymy $F'$, w której określony procent klauzul jest redundantny (0\%, 10\%, 25\%, 50\%). Klauzule redundantne powstają przez:

- **R1:** powtórzenie istniejącej klauzuli
- **R2:** utworzenie klauzuli równoważnej logicznie (zmiana kolejności literałów)
- **R3:** utworzenie klauzuli zawierającej podzbiór literałów istniejącej klauzuli

Testowane relacje: T1 (równoważność), T2 (wzmocnienie), T3 (osłabienie), T4 (współspełnialność).

**Parametry:** `clauses` (int), `lengths` (int list), `redundancy_percent` (float), `redundancy_mode` (choice: t1-t4)

---

### P12. Krytyczność klauzul i odporność na braki

Badanie wpływu usunięcia części klauzul na zachowanie własności oraz stabilność wnioskowania. Generujemy formułę $F$ (200, 500 lub 1000 klauzul), a następnie tworzymy $F'$ przez usunięcie części klauzul (5\%, 10\%, 25\%, 50\%). Usuwanie realizowane jest w trzech wariantach:

- **D1 (losowe):** usuwanie bez względu na typ klauzuli
- **D2 (preferencja safety):** w pierwszej kolejności usuwane są klauzule safety
- **D3 (preferencja liveness):** w pierwszej kolejności usuwane są klauzule liveness

Dla każdej formuły definiujemy prostą klauzulę $R$ (typu liveness). Testowane relacje: R1 $(F \Rightarrow R)$, R2 $(F' \Rightarrow R)$, R3 $(F \land \neg R)$, R4 $(F' \land \neg R)$.

**Parametry:** `clauses` (int), `lengths` (int list), `degradation_percent` (float), `degradation_variant` (choice: d1-d3), `missing_info_mode` (choice: r1-r4)

---

### P13. Struktura grafu współwystępowania atomów

Badanie wpływu topologii powiązań między atomami na wydajność wnioskowania. Generujemy formuły o liczbie klauzul 100, 200, 500 lub 1000, kontrolując współwystępowanie atomów. Proporcja liveness/safety: 50:50. Każdy atom występuje co najmniej raz.

Rozważane topologie:

- **G1 (rzadki):** duży zbiór atomów względem liczby klauzul, minimalna szansa na współwystępowanie
- **G2 (gęsty):** bardzo mały zbiór atomów, ekstremalnie wysoka liczba powiązań
- **G3 (drzewiasty):** atomy uporządkowane hierarchicznie, eliminacja cykli w grafie zależności
- **G4 (modułowy):** zbiór podzielony na rozłączne klastry; 90% klauzul zawiera atomy z jednego klastra, 10% to mosty między klastrami
- **G5 (centralny):** wybrany atom (hub) występuje we wszystkich klauzulach

**Parametry:** `clauses` (int), `lengths` (int list), `topology_variant` (choice: g1-g5)

---

### P14. Modularność i integracja modeli behawioralnych

Badanie wpływu stopnia powiązania między modułami na wydajność wnioskowania. Generujemy $n$ modułów $M_1,\dots,M_n$ ($n \in \{2, 3, 5\}$), każdy po 50, 100 lub 200 klauzul. Model globalny: $G = M_1 \land M_2 \land \dots \land M_n$. Proporcja liveness/safety: 50:50.

Warianty sprzężenia:

- **C1 (niezależne):** zbiory atomów rozłączne
- **C2 (słabo powiązane):** 5–10% współdzielonych atomów
- **C3 (średnio powiązane):** 25% współdzielonych atomów
- **C4 (silnie powiązane):** 50% współdzielonych atomów

Testowane relacje: lokalność ($M_i \Rightarrow R$), globalność ($G \Rightarrow R$), współspełnialność ($G \land R$).

**Parametry:** `clauses` (int), `lengths` (int list), `modules_count` (int), `coupling_variant` (choice: c1-c4), `modular_mode` (choice: locality/globality/co-sat)

---

### P15. Kontrolowana sprzeczność lokalna

Badanie wydajności wykrywania niespełnialności (UNSAT) przy kontrolowanym wprowadzaniu sprzecznych klauzul. Generujemy formułę $F$ (100, 200, 500 lub 1000 klauzul), a następnie wprowadzamy $p\%$ par konfliktowych (0\%, 1\%, 5\%, 10\%).

Typy konfliktów:

- **C1 (bezpośrednie):** klauzule o przeciwnej polaryzacji tego samego atomu
- **C2 (warunkowe):** klauzule sprzeczne przy określonym założeniu
- **C3 (behawioralne):** konflikt między klauzulą safety (zakaz) i liveness (wymuszenie)

Warianty głębokości:

- **V1 (lokalny):** konflikt w obrębie dwóch bezpośrednio powiązanych klauzul
- **V2 (bliski):** konflikt wymagający krótkiego łańcucha wnioskowania
- **V3 (rozproszony):** konflikt wymagający długiego łańcucha wnioskowania

**Parametry:** `clauses` (int), `lengths` (int list), `conflict_percent` (float), `conflict_type` (choice: c1-c3), `conflict_depth` (choice: v1-v3)

---

### P16. Głębokość łańcuchów implikacyjnych

Badanie wydajności wnioskowania przy wielokrotnym złożeniu implikacji. Generujemy formułę $F$ zawierającą liniowy łańcuch implikacji między atomami (długość łańcucha $k \in \{2, 5, 10, 25, 50\}$) oraz dodatkowe klauzule tła, tak aby całkowita liczba klauzul wynosiła 100, 200 lub 500.

Testowane relacje:

- **T1 (przechodniość):** weryfikacja relacji $A_1 \Rightarrow A_k$
- **T2 (niesprzeczność):** badanie $A_1 \land \neg A_k$ w celu potwierdzenia UNSAT

**Parametry:** `clauses` (int), `lengths` (int list), `chain_length` (int), `implication_mode` (choice: t1/t2)

---

### P17. Struktury Hornowskie i prawie-Hornowskie

Badanie wydajności wnioskowania w zależności od udziału klauzul Hornowskich (z co najwyżej jednym literałem pozytywnym). Rozpatrywane przypadki: 100%, 75%, 50%, 25%, 0% klauzul Hornowskich. Całkowita liczba klauzul: 100, 200, 500, 1000. Pozostałe parametry zgodne z P01/P02.

**Parametry:** `clauses` (int), `lengths` (int list), `horn_percent` (float)

---

### P18. Trudność w pobliżu granicy SAT/UNSAT (przejście fazowe)

Badanie wydajności wnioskowania w zależności od stosunku liczby klauzul do liczby atomów ($\alpha = m/n$). Generujemy formuły o ustalonej liczbie atomów $n$ (np. 100, 200, 500), dobierając liczbę klauzul $m$ dla zadanych wartości $\alpha$.

Rozpatrywane przypadki:

- $\alpha \in \{0.5, 1.0\}$ — niski poziom zagęszczenia
- $\alpha \in \{2.0, 3.0, 4.0\}$ — obszar potencjalnego przejścia fazowego (zwiększona trudność)
- $\alpha \in \{6.0, 8.0\}$ — wysoki poziom zagęszczenia

**Parametry:** `atoms` (int), `alpha` (float), `lengths` (int list)

---
