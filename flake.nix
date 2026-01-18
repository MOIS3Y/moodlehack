{
  description = "Moodle Test Answer Hub built with Django.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ (import ./nix/overlays.nix) ];
        };
      in {
      packages = {
        moodlehack = pkgs.callPackage ./default.nix { };
        default = self.packages.${system}.moodlehack;
      };
      apps = {
        moodlehack = {
          type = "app";
          program = "${self.packages.${system}.moodlehack}/bin/moodlehack";
        };
      };
      devShells = {
        moodlehack = pkgs.callPackage ./shell.nix { inherit pkgs; };
        default = self.devShells.${system}.moodlehack;
      };
    }
  );
}
