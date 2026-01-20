{
  lib,
  self ? { },
  pyprojectPath ? ../pyproject.toml,
}:

let
  # Load and parse pyproject.toml to get the base version
  pyproject = lib.importTOML pyprojectPath;
  baseVersion = pyproject.project.version;

  rev = self.shortRev or "dirty";
  date = lib.substring 0 8 (self.lastModifiedDate or "19700101");

  isFlake = self ? shortRev || self ? lastModifiedDate;
in
# If in Flake/Git context, append PEP 440 compliant local version identifier
if isFlake then
  "${baseVersion}+g${rev}.d${date}" # Example: 0.2.0+ga1b2c3d.d20260119
else
  baseVersion
