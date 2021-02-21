//
// Used to validate Mtwister
//

#include <iostream>
#include <random>

std::mt19937 randgen(0);

int main() {
    for (int i = 0; i<1000; i++)
        std::cout<<randgen()<<std::endl;
    return 0;
}