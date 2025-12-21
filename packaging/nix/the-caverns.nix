{ stdenv, pkgs }:
stdenv.mkDerivation {
  pname = "the-caverns";
  version = "0.1.0";

  srcs = ./../../.;
  nativeBuildInputs = with pkgs; [
    python313
    uv
    stdenv.cc.cc.lib
  ];

  buildPhase = ''
  echo $SSL_CERT_FILE
  python --version
  export UV_NO_MANAGED_PYTHON=1
  export UV_PYTHON_DOWNLOADS=never
  export UV_LOCKED=1
  export UV_NO_CACHE=1
  #uv sync --no-managed-python --no-python-downloads --locked --no-cache
  uv sync
  $srcs/build.sh
  '';
  installPhase = ''
  mkdir -p $out/bin
  cp "dist/The Caverns" $out/bin/the-caverns
  '';

  outputHash = "sha256-7s/SUZxzTpaHmLsvbozWIFMhh6Q7eZUNSlAE5xQyLqU=";
  outputHashMode = "recursive";
}
