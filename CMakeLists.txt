cmake_minimum_required(VERSION 3.18)

project("The Caverns")

# Include the engine directory
include_directories("${PROJECT_SOURCE_DIR}/engine")
include_directories("${PROJECT_SOURCE_DIR}/lib")
# Make our target
add_executable("theCaverns" "src/main.cpp" "src/mainMenu.cpp" "src/game.cpp")
add_executable("mingwTheCaverns.exe" "src/main.cpp" "src/mainMenu.cpp" "src/game.cpp")
# Add SFML as dependancy
find_package(SFML 2.5 COMPONENTS system window graphics network audio REQUIRED)
target_link_libraries("theCaverns" sfml-graphics)
target_link_libraries("theCaverns" sfml-window)
target_link_libraries("theCaverns" sfml-system)
target_link_libraries("mingwTheCaverns.exe" sfml-graphics)
target_link_libraries("mingwTheCaverns.exe" sfml-window)
target_link_libraries("mingwTheCaverns.exe" sfml-system)
# Add tinytmx as a dependancy
find_package(tinytmx REQUIRED)
target_link_libraries("theCaverns" tinytmx::tinytmx)
target_link_libraries("mingwTheCaverns.exe" tinytmx::tinytmx)
# Target C++17
target_compile_features("theCaverns" PRIVATE cxx_std_17)
target_compile_features("mingwTheCaverns.exe" PRIVATE cxx_std_17)