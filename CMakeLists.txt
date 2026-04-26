cmake_minimum_required(VERSION 3.30)

find_package(Git QUIET)

if(Git_FOUND)
  execute_process(
    COMMAND ${GIT_EXECUTABLE} describe --tags --abbrev=0
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_TAG
    OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET
  )

  if(GIT_TAG)
    string(SUBSTRING ${GIT_TAG} 1 -1 PROJECT_VERSION)
  endif()
endif()

if(NOT PROJECT_VERSION)
  set(PROJECT_VERSION "1.0.1")
endif()

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
include(cmake/parse_version.cmake)

set(PROJECT_VERSION_MAJOR "")
set(PROJECT_VERSION_MINOR "")
set(PROJECT_VERSION_PATCH "")
parse_version(PROJECT_VERSION_MAJOR PROJECT_VERSION_MINOR PROJECT_VERSION_PATCH PROJECT_VERSION ${PROJECT_VERSION})

project(helloworld VERSION ${PROJECT_VERSION})

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(CI_CD_RELEASE)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU|AppleClang")
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|amd64")
      add_compile_options(-mtune=generic -march=x86-64)
    elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "arm64|aarch64|ARM64")
      add_compile_options(-mtune=generic -march=armv8-a)
    else()
      message(WARNING "[${PROJECT_NAME}] Unknown processor: ${CMAKE_SYSTEM_PROCESSOR}")
    endif()
  else()
    message(FATAL_ERROR "[${PROJECT_NAME}] Unsupported compiler: ${CMAKE_CXX_COMPILER_ID}")
  endif()
endif()

find_package(
  Boost
  COMPONENTS unit_test_framework
  REQUIRED
)

configure_file(version.h.in version.h @ONLY)

add_executable(helloworld_cli main.cpp)
add_library(helloworld STATIC lib.cpp)
add_executable(test_version test_version.cpp)

target_include_directories(helloworld PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")
target_sources(helloworld PUBLIC FILE_SET HEADERS BASE_DIRS "${CMAKE_SOURCE_DIR}/" FILES "${CMAKE_SOURCE_DIR}/lib.h")

target_link_libraries(helloworld_cli PRIVATE helloworld)
target_link_options(helloworld_cli PRIVATE "$<$<BOOL:${CI_CD_RELEASE}>:-static>")

target_link_libraries(test_version boost::boost helloworld)

install(TARGETS helloworld_cli RUNTIME DESTINATION bin)

set(CPACK_GENERATOR DEB)

set(CPACK_PACKAGE_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
set(CPACK_PACKAGE_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
set(CPACK_PACKAGE_VERSION_PATCH "${PROJECT_VERSION_PATCH}")

set(CPACK_PACKAGE_CONTACT example@example.com)

include(CPack)

enable_testing()

add_test(test_version test_version)
