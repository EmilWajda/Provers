{
  pkgs ? import <nixpkgs> { },
  core-deps ? (import ./core).deps,
  ...
}:
pkgs.mkShell {
  packages = [
    pkgs.python313

    pkgs.nodejs

    pkgs.cargo
    pkgs.rustc
    pkgs.clippy
  ]
  ++ core-deps;

  shellHook = ''
    cd frontend
    if [ ! -d "node_modules" ]; then
      npm install
    fi
    cd ..

    export RUST_SRC_PATH="${pkgs.rustPlatform.rustLibSrc}";
  '';
}
