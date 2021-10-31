with import <nixpkgs> {};

(python38.withPackages (ps: with ps; [ pycrypto requests ])).env

