#include <iostream>

#include "lib.h"

auto main() -> int {
    try {
        auto const patch_version = version();
        std::cout << patch_version << '\n';
    } catch (std::exception const& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}