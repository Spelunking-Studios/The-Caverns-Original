cmake_minimum_required(VERSION 3.18)

project("The Caverns")

# Include the engine directory
include_directories("${PROJECT_SOURCE_DIR}/engine")
# Make our target
add_executable("theCaverns" "src/main.cpp" "src/mainMenu.cpp")
# Add SFML as dependancy
find_package(SFML 2.5 COMPONENTS system window graphics network audio REQUIRED)
target_link_libraries("theCaverns" sfml-graphics)
target_link_libraries("theCaverns" sfml-window)
target_link_libraries("theCaverns" sfml-system)