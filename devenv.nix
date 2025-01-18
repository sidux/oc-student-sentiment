{ pkgs, lib, config, inputs, ... }:

{

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
