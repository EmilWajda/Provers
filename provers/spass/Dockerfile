FROM nixos/nix:2.32.2

WORKDIR /loft

RUN nix-channel --update
RUN nix-env -iA nixpkgs.time nixpkgs.spass

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
