let
  lock = builtins.fromJSON (builtins.readFile ../flake.lock);
  node = lock.nodes.nixpkgs.locked;
in
import
  (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/${node.rev}.tar.gz";
    sha256 = node.narHash;
  })
  {
    overlays = [ (import ./overlays.nix) ];
  }
