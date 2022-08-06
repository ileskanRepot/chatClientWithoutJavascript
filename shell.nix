{ pkgs ? import <nixpkgs> {}}:
  pkgs.mkShell {
    nativeBuildInputs = let
      env = pyPkgs : with pyPkgs; [
        numpy
        matplotlib
        pandas
      ];
    in with pkgs; [
      (python39.withPackages env)
    ];
}
