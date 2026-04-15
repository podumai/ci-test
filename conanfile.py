from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

class CiTestDeps(ConanFile):
    settings: list[str] = ["os", "compiler", "build_type", "arch"]
    generators: list[str] = ["CMakeDeps", "CMakeToolchain"]

    def requirements(self) -> None:
        self.requires("boost/1.90.0")

    def layout(self) -> None:
        cmake_layout(self)