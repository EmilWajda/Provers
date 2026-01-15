FROM loft-base

RUN nix-env -iA nixpkgs.time nixpkgs.z3

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
