{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils
  } : flake-utils.lib.eachDefaultSystem
    ( system:
        let
          pkgs = (import nixpkgs) {
            inherit system;
            config.allowUnfree = true;
          };
        in {
          devShell = pkgs.mkShell {
            buildInputs = with pkgs; [
              nil
              nixd
              python312
              valgrind-light
              cifs-utils
              nfs-utils
              hdf5_1_10
              kcat
            ] ++ (
              with python312Packages; [
                pip
                requests
                pandas
                matplotlib
                numpy
                scipy
                ipykernel
                ipywidgets
                h5py
                elasticsearch
              ]
            );
          };
        }
    );
}