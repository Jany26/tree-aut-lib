#include <string>
#include <list>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_map>
#include <hash_map>
#include <map>

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

enum TransitionSymbol {
    ZERO, ONE, LH,
};

enum BoxType {
    SHORT,
    X,
    L0,
    L1,
    H0,
    H1,
    LPort,
    HPort,
};

typedef std::map<int, std::map<int, TreeAutomatonTransition>> TransitionMap;

class TreeAutomatonTransition {
    // src ---[sym, var]---> [ L:Low->child1, H:High->child2 ]
    public:
        int src;
        TransitionSymbol sym;
        int var;
        BoxType low;
        BoxType high;
        int children[2];

        // TreeAutomatonTransition(string x, string y, int z)
};

class TreeAutomaton {
    public:
        std::string name;
        TransitionMap transitions;
        std::list<int> roots;
        int ports;
    
        TreeAutomaton(
            std::string name,
            int ports,
            std::list<int> roots,
            TransitionMap transitions
        ) {
            
        }
        void print();
};

void TreeAutomaton::print() {
    for (auto& it: this->transitions) {
        for (auto it2: it.second) {
            int src_state = it.first;
            TreeAutomatonTransition tr = it2.second;
            std::cout << tr.src << tr.sym << tr.var << tr.children;
        }
    }
}


TreeAutomaton load_vtf(std::string file_path) {
    // FILE *f = fopen(file_path, "r");
    // if (f == NULL) {
    //     printf("Error\n");
    //     return 1;
    // }
    std::ifstream infile(file_path);
    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        std::cout << line;
    }
    std::string name = "";
    int ports = 0;
    std::list<int> roots;
    TransitionMap transitions;

    TreeAutomaton ta(name, ports, roots, transitions);
    return ta;
}


int main(int argc, char **argv) {
    // if string(argv[1]) == ""
    std::string fileName = argv[1];
    TreeAutomaton ta = load_vtf(fileName);
    std::ifstream infile("thefile.txt");
    return 0;
}