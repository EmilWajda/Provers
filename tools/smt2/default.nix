let
  pkgs = import <nixpkgs> { };
  tptp4x-src = pkgs.fetchFromGitHub {
    owner = "TPTPWorld";
    repo = "TPTP4X";
    rev = "a5357562d22e156f3662e76d81b044576c7b42ae";
    hash = "sha256-/Dn2rHRZ8LoQbUOaeyut89zEwjEej3yWn8A4WgDOTXA=";
  };
  jjparser-src = pkgs.fetchFromGitHub {
    owner = "TPTPWorld";
    repo = "JJParser";
    rev = "fc6644b90d0a4b353cbdfe37439712a82a761196";
    hash = "sha256-ZOPxT+fCv09Fh9wrCU4XSgakjZrgKq4YR6N3zY+zOuQ=";
  };
in
pkgs.stdenv.mkDerivation {
  name = "tptp4X";
  src = tptp4x-src;

  buildInputs = [ pkgs.curl ];

  preConfigure = ''
    rm ./JJParser
    cp -r ${jjparser-src} ./JJParser
    chmod -R u+w ./JJParser
  '';

  buildPhase = ''
    make -j$NIX_BUILD_CORES
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp tptp4X $out/bin/tptp4X
  '';

  meta = {
    description = "A tool for processing TPTP problem files";
    homepage = "http://www.tptp.org/";
  };
}
