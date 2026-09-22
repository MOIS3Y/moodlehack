{
  description = "Moodle Test Answer Hub built with Django.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        pyproject-nix.follows = "pyproject-nix";
      };
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        pyproject-nix.follows = "pyproject-nix";
        uv2nix.follows = "uv2nix";
      };
    };
  };

  outputs =
    {
      nixpkgs,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
      ...
    }:
    let
      inherit (nixpkgs) lib;
      inherit (lib.importTOML ./pyproject.toml) project;
      inherit (project) version;
      sourceUrl = "https://github.com/mois3y/moodlehack";
      authors = lib.concatMapStringsSep ", " (
        author: "${author.name} <${author.email}>"
      ) project.authors;
      forAllSystems = lib.genAttrs [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };

      perSystem = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python314;
          pythonSet =
            (pkgs.callPackage pyproject-nix.build.packages {
              inherit python;
            }).overrideScope
              (
                lib.composeManyExtensions [
                  pyproject-build-systems.overlays.wheel
                  (workspace.mkPyprojectOverlay {
                    sourcePreference = "wheel";
                  })
                  (_final: prev: {
                    moodlehack = prev.moodlehack.overrideAttrs (old: {
                      nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
                        pkgs.gettext
                      ];
                      # Compile catalogs without loading application settings.
                      preBuild = (old.preBuild or "") + ''
                        while IFS= read -r -d "" catalog; do
                          msgfmt "$catalog" -o "''${catalog%.po}.mo"
                        done < <(find src/moodlehack -name '*.po' -print0)
                      '';
                    });
                  })
                ]
              );

          application =
            (pythonSet.mkVirtualEnv "moodlehack-${version}" {
              moodlehack = [ ];
            }).overrideAttrs
              {
                inherit version;
              };

          dockerImage = pkgs.dockerTools.buildLayeredImage {
            name = "mois3y/moodlehack";
            tag = version;
            contents = [
              application
              pkgs.coreutils
              pkgs.bashInteractive
              pkgs.procps
              pkgs.dockerTools.binSh
              pkgs.dockerTools.usrBinEnv
              pkgs.dockerTools.caCertificates
            ];
            enableFakechroot = true;
            fakeRootCommands = ''
              ${pkgs.dockerTools.shadowSetup}
              groupadd -r -g 1000 moodlehack
              useradd -r -u 1000 -g moodlehack -d /app -s /bin/sh moodlehack
              mkdir -p /app/config /app/data /app/cache /app/state
              chown -R moodlehack:moodlehack /app
            '';
            config = {
              User = "moodlehack";
              WorkingDir = "/app";
              Labels = {
                "org.opencontainers.image.title" = "MoodleHack";
                "org.opencontainers.image.description" = project.description;
                "org.opencontainers.image.version" = version;
                "org.opencontainers.image.source" = sourceUrl;
                "org.opencontainers.image.authors" = authors;
                "org.opencontainers.image.licenses" = project.license;
                "me.zhukovsky.moodlehack.id" = "me.zhukovsky.moodlehack";
              };
              Env = [
                "HOME=/app"
                "XDG_CONFIG_HOME=/app/config"
                "XDG_DATA_HOME=/app/data"
                "XDG_CACHE_HOME=/app/cache"
                "XDG_STATE_HOME=/app/state"
                "PYTHONUNBUFFERED=1"
              ];
              Cmd = [
                "moodlehack"
                "serve"
                "--host"
                "0.0.0.0"
              ];
              ExposedPorts."8000/tcp" = { };
            };
          };

          devShell = pkgs.mkShell {
            packages = [
              python
              pkgs.uv
              pkgs.gettext
            ];
            shellHook = "unset PYTHONPATH";
            env = {
              UV_PYTHON = python.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
            };
          };
        in
        {
          packages = {
            moodlehack = application;
            default = application;
          }
          // lib.optionalAttrs pkgs.stdenv.hostPlatform.isLinux {
            inherit dockerImage;
          };
          apps.moodlehack = {
            type = "app";
            meta.description = "Moodle test answer hub";
            program = "${application}/bin/moodlehack";
          };
          devShells = {
            moodlehack = devShell;
            default = devShell;
          };
        }
      );
    in
    {
      packages = forAllSystems (system: perSystem.${system}.packages);
      apps = forAllSystems (system: perSystem.${system}.apps);
      devShells = forAllSystems (system: perSystem.${system}.devShells);
    };
}
