{ pkgs, lib, config, inputs, ... }:

{

  dotenv.enable = true;

  packages = [
    pkgs.terraform
    pkgs.azure-cli
    pkgs.terraformer
  ];

  languages.python = {
    enable = true;
    poetry = {
      enable = true;
      install = {
        enable = true;
      };
    };
  };

  processes = {
    uvicorn.exec = "poetry run uvicorn app.main:app --reload --reload-include '.env*' --reload-include '.env' --reload-include '*.yaml'";
  };

  scripts.up.exec = "devenv up";
}
