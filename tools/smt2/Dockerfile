FROM loft-base

COPY default.nix .
RUN nix-build

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
