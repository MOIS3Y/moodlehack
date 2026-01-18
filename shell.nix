{ pkgs ? import <nixpkgs> { overlays = [ (import ./nix/overlays.nix) ];} }:

let
  moodlehackPackage = pkgs.callPackage ./default.nix { };
  python = pkgs.python3;
in

pkgs.mkShell {
  inputsFrom = [ moodlehackPackage ];

  packages = [
    pkgs.uv
    python
  ];

  shellHook = ''
    echo "==========================================================="
    if [ -f .envrc ]; then
      echo "✅ Environment: Active"
    else
      echo "💡 Tip: Use 'direnv' to automate your workflow."
      echo "   Example .envrc:"
      echo "     use flake"
      echo "     export MOODLEHACK_SETTINGS_FILE=\$PWD/settings.toml"
    fi
    echo "==========================================================="
  '';
}
