FROM nixos/nix:2.33.0

WORKDIR /loft

RUN nix-channel --update

COPY . .
RUN nix-build -E 'with import <nixpkgs> {}; callPackage ./. {}'

ENTRYPOINT ["result/bin/tptp-checker"]
