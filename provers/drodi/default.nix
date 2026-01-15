let
  pkgs = import <nixpkgs> { };
  drodi-path = "provers-containerised/provers/Drodi---3.6.0";
in
pkgs.stdenv.mkDerivation {
  pname = "drodi";
  version = "3.6.0";

  src = pkgs.fetchFromGitHub {
    owner = "StarExecMiami";
    repo = "StarExec-ARC";
    rev = "fc00c9f4f1196223406fe8517b2473b5b367a8b7";
    hash = "sha256-H/U1FEvdpsX0VzlafgopOn0xn5MybYsh3v0ZPHyIRTk=";
    sparseCheckout = [ drodi-path ];
  };

  nativeBuildInputs = [ pkgs.makeWrapper ];

  installPhase = ''
    mkdir -p $out/bin
    mkdir -p $out/lib
    cp ${drodi-path}/drodi $out/bin/drodi
    cp ${drodi-path}/drodi.lrn $out/lib/drodi.lrn
    runHook postInstall
  '';

  postInstall = ''
    wrapProgram $out/bin/drodi --add-flags "\"-learnfrom($out/lib/drodi.lrn)\""
  '';

  dontFixup = true;

  meta.description = "A very basic and lightweight automated theorem prover";
}
