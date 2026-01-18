{ pkgs ? import <nixpkgs> { overlays = [ (import ./nix/overlays.nix) ];} }:

let
  python = pkgs.python3;
  inherit (python.pkgs)
    buildPythonApplication
    uv-build
  ;
in

buildPythonApplication {
  pname = "moodlehack";
  version = "0.2.0";
  format = "pyproject";
  src = ./.;

  nativeBuildInputs = [
    uv-build
  ];

  dependencies = with python.pkgs; [
    django
    django-environ
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
}
