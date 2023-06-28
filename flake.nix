{
  description = "App for hacking moodle tests";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixpkgs-unstable";
    };
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
  {
    packages.${system}.default = pkgs.poetry2nix.mkPoetryApplication {
      projectDir = self;
    };
    devShells.${system}.default = pkgs.mkShellNoCC {
      shellHook = "echo Welcome to your Nix-powered development environment!";
      TEST_ENV = "SEE_ME?";
      packages = with pkgs; [
        poetry
        # (poetry2nix.mkPoetryEnv { projectDir = self; })
      ];
    };
  };
}
