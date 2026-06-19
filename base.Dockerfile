FROM nixos/nix:2.34.4

RUN nix-channel --add \
    https://github.com/NixOS/nixpkgs/archive/9ae611a455b90cf061d8f332b977e387bda8e1ca.tar.gz \
    nixpkgs
RUN nix-channel --update

WORKDIR /loft

ENTRYPOINT ["nix-instantiate", "--eval", "-E", "(import <nixpkgs> {}).lib.version"]
