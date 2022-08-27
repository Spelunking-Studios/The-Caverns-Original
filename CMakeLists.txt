cmake_minimum_required(VERSION 3.18)

project("The Caverns")

include_directories("${PROJECT_SOURCE_DIR}/engine")
add_executable("theCaverns" "src/main.cpp")
find_package("sfml-graphics")
find_package("sfml-window")
find_package("sfml-system")
target_link_libraries("${PROJECT_NAME}" "sfml-graphics")
target_link_libraries("${PROJECT_NAME}" "sfml-window")
target_link_libraries("${PROJECT_NAME}" "sfml-system")