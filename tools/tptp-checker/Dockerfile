FROM loft-base

COPY . .
RUN nix-build

ENTRYPOINT ["result/bin/tptp-checker"]
