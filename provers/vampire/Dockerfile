FROM nixos/nix:2.32.2

WORKDIR /loft

RUN nix-channel --update
RUN nix-env -iA nixpkgs.vampire

ENTRYPOINT ["vampire"]
