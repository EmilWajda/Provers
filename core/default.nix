let
  pkgs = import <nixpkgs> { };
  pyproject-nix =
    import
      (pkgs.fetchFromGitHub {
        owner = "pyproject-nix";
        repo = "pyproject.nix";
        rev = "2c8df1383b32e5443c921f61224b198a2282a657";
        hash = "sha256-xaKvtPx6YAnA3HQVp5LwyYG1MaN4LLehpQI8xEdBvBY=";
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
