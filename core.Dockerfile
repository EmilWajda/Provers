FROM loft-base

# Install necessary packages
RUN nix-env -iA nixpkgs.docker-client
COPY docker-compose.yaml .

# Prebuild dependencies for caching purposes
COPY core/default.nix .
COPY core/pyproject.toml .
RUN nix-build -A deps
RUN rm -rf result

# Build and install final package
COPY core/loft loft
RUN nix-build -A core

ENTRYPOINT ["result/bin/python", "-m", "loft"]
