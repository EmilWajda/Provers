{
  pkgs ? import <nixpkgs> { },
  ...
}:
pkgs.mkShell {
  packages = [
    (pkgs.python313.withPackages (
      ps: with ps; [
        pip
      ]
    ))
    pkgs.nodejs
    pkgs.cargo
    pkgs.rustc
  ];

  shellHook = ''
    cd core
    if [ ! -d ".venv" ]; then
      python -m venv .venv
      source .venv/bin/activate
      pip install .
    else
      source .venv/bin/activate
    fi
    cd ..
    cd frontend
    if [ ! -d "node_modules" ]; then
      npm install
    fi
    cd ..
  '';
}
