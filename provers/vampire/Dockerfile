FROM nixos/nix:2.32.2

RUN nix-channel --update
RUN nix-env -iA nixpkgs.vampire

ENTRYPOINT ["vampire"]
