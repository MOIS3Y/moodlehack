{
  pkgs ? import ./nix/nixpkgs.nix,
  self ? { },
}:

let
  python = pkgs.python3;
  inherit (python.pkgs)
    buildPythonApplication
    uv-build
    ;
  inherit (pkgs) lib;
  version = import ./nix/version.nix { inherit lib self; };
in

buildPythonApplication {
  pname = "moodlehack";
  inherit version;
  format = "pyproject";
  src = ./.;

  nativeBuildInputs = [
    pkgs.gettext
    uv-build
  ];

  dependencies = with python.pkgs; [
    django
    djangorestframework
    drf-spectacular
    django-filter
    django-crispy-forms
    django-typer
    crispy-bootstrap5
    markdown
    platformdirs
    pydantic-settings
    rich
    starlette
    uvicorn
  ];

  preBuild = ''
    # Compile localization messages (.po to .mo) for the application
    export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
    cd src/moodlehack
    python manage.py compilemessages
    cd ../..
  '';
}
