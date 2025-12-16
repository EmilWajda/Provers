let
  pkgs = import <nixpkgs> { };
  pyproject-nix =
    import
      (builtins.fetchGit {
        url = "https://github.com/pyproject-nix/pyproject.nix.git";
      })
      {
        inherit (pkgs) lib;
      };
  python = pkgs.python313;

  project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
  attrs = project.renderers.buildPythonPackage { inherit python; };
  package = python.pkgs.buildPythonPackage attrs;
in
python.buildEnv.override {
  extraLibs = [ package ];
}
