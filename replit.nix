{ pkgs }: {
    deps = [
        pkgs.xlibs.xinit
        pkgs.killall
        pkgs.cmake
        pkgs.pkgconfig
        pkgs.rustup
        pkgs.rustc
        pkgs.rust-analyzer
        pkgs.glib
        pkgs.xorg.xorgserver
        pkgs.xorg.xf86inputevdev
        pkgs.xorg.xf86inputsynaptics
        pkgs.xorg.xf86inputlibinput
        pkgs.xorg.xf86videointel
        pkgs.xorg.xf86videoati
        pkgs.xorg.xf86videonouveau
        pkgs.xorg.libX11
        pkgs.xorg.libXrandr
        pkgs.xorg.libXinerama
        pkgs.xorg.libXcursor
        pkgs.xorg.libXi
        pkgs.glfw
    ];
    env = {
        LD_INCLUDE_PATH = pkgs.lib.makeLibraryPath ([
            pkgs.glib
        ] ++ (with pkgs.xorg; [ libX11 libXext libXinerama libXcursor libXrandr libXi libXxf86vm ]));
  };
}