FROM loft-base

COPY . .
RUN nix-build -E 'with import <nixpkgs> {}; callPackage ./. {}'

ENTRYPOINT ["result/bin/tptp-checker"]
