with import <nixpkgs> {};

(python37.withPackages (ps: with ps; [ pycrypto ])).env

