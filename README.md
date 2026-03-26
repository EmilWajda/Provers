# LOFT

First order logic formula generator and benchmarking tool for theorem provers.

## How to run

1. Install [Docker](https://www.docker.com/get-started).
2. Clone this repository.
3. Build the images:
    ```bash
    $ docker compose build base
    $ docker compose --profile tools build
    ```
4. Run the web application:
    ```bash
    $ docker compose up
    ```
5. Open your browser and go to `http://localhost:8000`.

## How to build PDF report (suggestion)

1. Install [Pandoc](https://pandoc.org/installing.html) and [TeX Live](https://www.tug.org/texlive/).
2. Clone this repository.
3. Run the following commands:
    ```bash
    $ cd docs
    $ pandoc docs-pl.md -o docs-pl.pdf -V geometry:margin=1in -V colorlinks=true
    ```
