{ pkgs, lib, config, inputs, ... }:

{

  packages = [
    pkgs.railway-cli
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
}
