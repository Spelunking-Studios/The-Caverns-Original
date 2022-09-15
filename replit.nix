{ pkgs }: {
	deps = [
		pkgs.python39Full
        pkgs.tokei
	];
  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath ([
      # Neded for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
    ] ++ (with pkgs.xorg; [ libX11 libXext libXinerama libXcursor libXrandr libXi libXxf86vm ]));

    PYTHONBIN = "${pkgs.python39Full}/bin/python3.9";
  };
}