let
  pkgs = import <nixpkgs> { };
  inherit (pkgs) lib;
in
pkgs.rustPlatform.buildRustPackage (finalAttrs: {
  pname = "inkresat-converter";
  version = "1.0.0";

  src = lib.cleanSource ./.;
  cargoLock.lockFile = ./Cargo.lock;

  meta = {
    description = "A tool for converting TPTP problems to the InKreSAT format";
    license = lib.licenses.mit;
  };
})
