FROM loft-base
# TODO: fix
RUN nix-env -iA nixpkgs.time nixpkgs.spass

COPY core/pyproject.toml .
RUN pip install --no-cache-dir .

COPY core/ .

ENTRYPOINT ["python", "-m", "loft"]
