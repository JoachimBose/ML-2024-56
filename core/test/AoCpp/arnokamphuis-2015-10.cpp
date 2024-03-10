#include <iostream>
#include <string>

std::string lookandsay(std::string input) {
    std::string output = "";

    int count = 0;
    char lastc = ' ';
    for (auto c : input) {
        if (lastc != ' ') {
            if (lastc == c) {
                ++count;
            } else {
                output += std::to_string(count) + lastc;
                count = 1;
            }
        } else {
            ++count;
        }

        lastc = c;
    }
    output += std::to_string(count) + lastc;

    return output;
}

int main() {
    std::string original_input = "1113122113";

    std::string input = original_input;
    for (int i = 0; i < 40; i++)
        input = lookandsay(input);

    input = original_input;
    for (int i = 0; i < 50; i++)
        input = lookandsay(input);
}