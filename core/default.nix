let
  pkgs = import <nixpkgs> { };
  pyproject-nix =
    import
      (builtins.fetchGit {
        url = "https://github.com/pyproject-nix/pyproject.nix.git";
        rev = "2c8df1383b32e5443c921f61224b198a2282a657";
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
  deps = pkgs.symlinkJoin {
    name = "loft-deps";
    paths = attrs.dependencies ++ [ python.buildEnv ];
  };
  core = python.buildEnv.override {
    extraLibs = [ package ];
  };
}
