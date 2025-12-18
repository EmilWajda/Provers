FROM loft-base

RUN nix-env -iA nixpkgs.time nixpkgs.iprover nixpkgs.vampire

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
