{ 
  pkgs ? import ./nix/nixpkgs.nix 
}:

let
  defaultPackage = pkgs.callPackage ./default.nix { inherit pkgs; };
  python = pkgs.python3;
in

pkgs.mkShell {
  inputsFrom = [ defaultPackage ];

  packages = [
    pkgs.uv
    python
  ];

  shellHook = ''
    echo "==========================================================="
    echo "Moodlehack Development Environment"
    echo "Version: ${defaultPackage.version}"
    echo "==========================================================="
    
    if [ -f .envrc ]; then
      echo "✅ direnv: Active"
    else
      echo "💡 Tip: Use 'direnv' to automate your workflow."
      echo "   Example .envrc:"
      echo "     use flake"
      echo "     export MOODLEHACK_SETTINGS_FILE=\$PWD/settings.toml"
    fi
    echo "==========================================================="
  '';
}
