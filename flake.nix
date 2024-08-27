{
  description = "nix flake for the development environment, use direnv to load the `.envrc` file to run this environment automatically or run `nix develop` to enter this shell";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      p2nix = import poetry2nix {inherit pkgs;};

      pyenv = (p2nix.mkPoetryEnv {
        groups = ["dev"];
        preferWheels = true;
        overrides = p2nix-buildInputs-overrides;
        projectDir = ./.;
        editablePackageSources = {
          data_sources = ./data_sources;
          dagster_project = ./dagster_project;
          dagster_project_tests = ./dagster_project_tests;
        };

      # Sometimes bytecode objects have the same name which causes nix to throw errors
      # In the case of general binaries, having the same binary name R  
      }).override {ignoreCollisions = true;};

      # Add build overrides here
      pypkgs-build-requirements = {
        pytest-parametrization = [ "setuptools" ];
        pendulum = ["distutils"];
        daff = ["setuptools"];
        sling-linux-amd64 = ["setuptools"];
        sling = ["setuptools"];
      };
      
      p2nix-buildInputs-overrides = p2nix.defaultPoetryOverrides.extend (final: prev:
         builtins.mapAttrs (package: build-requirements:
          (builtins.getAttr package prev).overridePythonAttrs (old: {
            buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg: if builtins.isString pkg then builtins.getAttr pkg prev else pkg) build-requirements);
          })
        ) pypkgs-build-requirements
      );

    in {

      devShells.default = pkgs.mkShell {
        buildInputs = [
          pyenv
          pkgs.podman
          pkgs.lazygit
          pkgs.poetry
          pkgs.cmake
        ];
      };
    });
}
