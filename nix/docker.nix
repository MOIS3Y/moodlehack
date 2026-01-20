{
  pkgs,
  self,
  system,
}:

let
  inherit (pkgs) lib;
  pyproject = lib.importTOML ../pyproject.toml;
  moodlehack = self.packages.${system}.moodlehack;
  userName = "moodlehack";
in
pkgs.dockerTools.buildLayeredImage {
  name = "mois3y/moodlehack";
  tag = pyproject.project.version;

  contents = with pkgs; [
    moodlehack
    coreutils
    bashInteractive
    procps
    dockerTools.binSh
    dockerTools.usrBinEnv
    dockerTools.caCertificates
  ];

  enableFakechroot = true;

  fakeRootCommands = ''
    # Setup basic /etc files required by shadow-utils
    ${pkgs.dockerTools.shadowSetup}

    # Create group and user with specific UID/GID 1000
    groupadd -r -g 1000 ${userName}
    useradd -r -u 1000 -g ${userName} -d /app -s /bin/sh ${userName}

    # Create application directories and set correct ownership
    mkdir -p /app/config /app/data /app/cache /app/state
    chown -R ${userName}:${userName} /app
  '';

  config = {
    User = "${userName}";
    WorkingDir = "/app";

    Labels = {
      "org.opencontainers.image.title" = "MoodleHack";
      "org.opencontainers.image.description" = pyproject.project.description or "";
      "org.opencontainers.image.version" = moodlehack.version;
      "org.opencontainers.image.source" = "https://github.com/mois3y/moodlehack";
      "org.opencontainers.image.authors" = "MOIS3Y <stepan@zhukovsky.me>";
      "org.opencontainers.image.licenses" = "GPLv3";
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
    ExposedPorts = {
      "8000/tcp" = { };
    };
  };
}
