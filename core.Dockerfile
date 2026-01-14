FROM loft-base AS frontend

# Build React frontend
RUN nix-env -iA nixpkgs.nodejs
COPY frontend/package.json .
COPY frontend/package-lock.json .
RUN npm install
COPY frontend/ .
RUN npm run build


FROM loft-base AS backend

# Install necessary packages
RUN nix-env -iA nixpkgs.docker-client

# Prebuild dependencies for caching purposes
COPY core/default.nix .
COPY core/pyproject.toml .
RUN nix-build -A deps
RUN rm -rf result

# Copy entrypoint script
COPY core/entrypoint.sh .
RUN chmod +x entrypoint.sh

# Build and install final package
COPY core/loft loft
COPY --from=frontend /loft/dist loft/static
RUN nix-build -A core
COPY docker-compose.yaml .

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
