let
  pkgs = import <nixpkgs> { };
  flags = [
    "-fpermissive"
    "--no-warnings"
  ];
  ocaml = pkgs.ocaml-ng.ocamlPackages_4_14;
in
pkgs.stdenv.mkDerivation {
  pname = "InKreSAT";
  version = "1.0";

  src = pkgs.fetchurl {
    url = "https://www.ps.uni-saarland.de/~kaminski/inkresat/inkresat-1.0.tar.bz2";
    sha256 = "sha256-rvOqrc06cTNVc7Q3y7Oc4PTSkd75zGhd/fAOVZJWw40=";
  };

  postPatch = ''
    substituteInPlace src/Makefile --replace-fail g++ 'g++ ${builtins.concatStringsSep " " flags}'
  '';

  CFLAGS = flags;

  nativeBuildInputs = [
    pkgs.zlib
    ocaml.ocaml
    ocaml.extlib
    ocaml.findlib
  ];

  buildPhase = ''
    make inkresat
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp inkresat $out/bin/
  '';

  meta.description = "Modal Reasoning via Reduction to SAT";
}
