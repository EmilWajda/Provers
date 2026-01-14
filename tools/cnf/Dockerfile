FROM loft-base

RUN nix-env -iA nixpkgs.vampire

ENTRYPOINT ["vampire", "--mode", "clausify"]
