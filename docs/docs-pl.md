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
    $ docker compose build
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
  formuł oraz czasie przerwania działania proverów (timeout) - opcjonalny,
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

TODO: opis modułów, klas, dependencji, itp.

## Frontend aplikacji

TODO: opis komponentów, dependencji, itp.

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
    - przyjmuje formuły w formacie TPTP.

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
