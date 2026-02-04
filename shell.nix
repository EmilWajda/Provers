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
    (pkgs.rustfmt.override {
      asNightly = true;
    })
  ]
  ++ core-deps;

  RUST_SRC_PATH = pkgs.rustPlatform.rustLibSrc;
}
