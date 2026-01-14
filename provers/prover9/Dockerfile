FROM loft-base

RUN nix-env -iA nixpkgs.time nixpkgs.prover9

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
