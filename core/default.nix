let
  pkgs = import <nixpkgs> { };
  pyproject-nix =
    import
      (pkgs.fetchFromGitHub {
        owner = "pyproject-nix";
        repo = "pyproject.nix";
        rev = "d37dcf34ac7194eac4b0d10520d01298c434267d";
        hash = "sha256-HmcZQ/hMPHR22Ri/6Sl7Z0B5J8nZa9bRnZJtDFInM7I=";
      })
      {
        inherit (pkgs) lib;
      };
  python = pkgs.python313;

  project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
  attrs = project.renderers.buildPythonPackage { inherit python; };
  package = python.pkgs.buildPythonPackage attrs;
in
{
  deps = attrs.dependencies ++ [ python.buildEnv ];
  core = python.buildEnv.override {
    extraLibs = [ package ];
  };
}
