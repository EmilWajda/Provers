let
  pkgs = import <nixpkgs> { };
  inherit (pkgs) lib;
in
pkgs.rustPlatform.buildRustPackage (finalAttrs: {
  pname = "tptp-checker";
  version = "1.0.0";

  src = lib.cleanSource ./.;
  cargoLock.lockFile = ./Cargo.lock;

  meta = {
    description = "A simple tool for checking syntax of TPTP problem files";
    license = lib.licenses.mit;
  };
})
