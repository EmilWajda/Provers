FROM nixos/nix:2.33.0

RUN nix-channel --add \
    https://github.com/NixOS/nixpkgs/archive/2fbfb1d73d239d2402a8fe03963e37aab15abe8b.tar.gz \
    nixpkgs
RUN nix-channel --update

WORKDIR /loft

ENTRYPOINT ["nix-instantiate", "--eval", "-E", "(import <nixpkgs> {}).lib.version"]
