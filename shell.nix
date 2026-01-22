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

  RUST_SRC_PATH = pkgs.rustPlatform.rustLibSrc;
}
