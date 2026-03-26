FROM nixos/nix:2.34.4

RUN nix-channel --add \
    https://github.com/NixOS/nixpkgs/archive/46db2e09e1d3f113a13c0d7b81e2f221c63b8ce9.tar.gz \
    nixpkgs
RUN nix-channel --update

WORKDIR /loft

ENTRYPOINT ["nix-instantiate", "--eval", "-E", "(import <nixpkgs> {}).lib.version"]
