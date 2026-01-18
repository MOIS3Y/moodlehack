final: prev: {
  python3 = prev.python3.override (old: {
    packageOverrides = python-final: python-prev: {
      #! waiting from nixpkgs
      #? see: https://github.com/NixOS/nixpkgs/pull/463651
      django-typer = prev.callPackage ./django-typer.nix {
        buildPythonPackage = python-prev.buildPythonPackage;
        inherit (python-prev)
          hatchling
          django
          click
          typer-slim
          shellingham
          typing-extensions
          rich
          pytest
          pytest-django;
        inherit (prev)
          fetchFromGitHub
          lib;
      };
    };
  });
}
