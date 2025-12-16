FROM loft-base

RUN nix-env -iA nixpkgs.docker-client
COPY docker-compose.yaml .

COPY core/ .
RUN nix-build

ENTRYPOINT ["result/bin/python", "-m", "loft"]
