#include "bdd.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>

#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <unordered_set>
#include <cctype>

class DimacsParser {
    public:
        std::string input_file, output_file, name;
        int variables_count, clausules_count, processed_clausules;
        // int variables_count, clausules_count;
        bool cnf; // if true => parsed as CNF, if false => DNF
        std::vector<std::string> tokens;
        std::string current_token;
        bdd result;
        bdd current_bdd;

        DimacsParser(std::string input, std::string output) {
            this->input_file = input;
            this->output_file = output;
            this->variables_count = 0;
            this->clausules_count = 0;
            this->processed_clausules = 0;
            this->cnf = false;
            this->name = "";
            this->tokens = {};
            this->current_token = "";
        };
        void reset();
        void print();
        void print_tokens();
        void tokenize();
        
        void parse();
        void preamble();
        void clausule();

        void export_to_abdd();
        std::string get_token();
    
};

void DimacsParser::reset() {
    this->input_file = "";
    this->output_file = "";
    this->variables_count = 0;
    this->clausules_count = 0;
    this->processed_clausules = 0;
    this->cnf = false;
    this->name = "";
    this->tokens = {};
    this->current_token = "";
}

void DimacsParser::print() {

}

void DimacsParser::print_tokens() {
    std::cout << "tokens = [ ";
    for (auto i: this->tokens) {
        if (i == "\n") std::cout << "EOL" << ' ';
        else std::cout << i << ' ';
    }
    std::cout << "]" << std::endl;
}

void DimacsParser::tokenize() {
    this->tokens = {};
    FILE *file = fopen(this->input_file.c_str(), "r");
    if (file == NULL) {
        fprintf(stderr, "Could not open file '%s'\n", this->input_file.c_str());
        exit(EXIT_FAILURE);
    }
    std::string line = "";
    int c;
    while ((c = fgetc(file)) != EOF) {
        if (c != '\n') {
            line += c;
            continue;
        } 
        if (line.length() == 1 or line[0] == 'c') {
            line = "";
            continue;
        }
        // std::cout << line;
        std::string word;
        line += '\n';
        for (char c : line) {
            if (isspace(c)) {
                if (word != "") {
                    this->tokens.push_back(word);
                    word = "";
                }
                if (c == '\n') {
                    this->tokens.push_back("\n");
                    break;
                } else continue;
            }
            word += c;
        }
        line = "";
    }
};

std::string DimacsParser::get_token() {
    if (this->tokens.size() == 0) {
        this->current_token = "";
        return "";
    }
    // std::cout << this->current_token << std::endl;
    this->current_token = this->tokens[0];
    this->tokens.erase(this->tokens.begin());
    return this->current_token;
}


void DimacsParser::parse() {
    while (this->tokens.size() > 0) {
        get_token();
        if (this->current_token == "p") {
            preamble();
            bdd_setvarnum(this->variables_count);
        } else {
            // printf("clausule %d of %d\n", this->processed_clausules, this->clausules_count);
            clausule();
            this->processed_clausules++;
        }
        if (this->tokens.size() <= 1) {
            return;
        }
    }
    if (this->processed_clausules != this->clausules_count) {
        fprintf(stderr, "error\n");
        return;
    }
}

void DimacsParser::preamble() {
    std::string type = get_token();
    if (type == "dnf") {
        this->cnf = false;
        this->result = bdd_false();
        this->current_bdd = bdd_true();
    } else if (type == "cnf") {
        this->cnf = true;
        this->result = bdd_true();
        this->current_bdd = bdd_false();
    } else {
        fprintf(stderr, "unsupported dimacs type = %s\n", type.c_str());
        exit(EXIT_FAILURE);
    }
    this->variables_count = stoi(get_token());
    this->clausules_count = stoi(get_token());
    if (variables_count <= 0 or clausules_count <= 0) {
        fprintf(stderr, "variable count or clausule count error\n");
        exit(EXIT_FAILURE);
    }
    get_token(); // '\n'
}

void DimacsParser::clausule() {
    if (this->cnf)
        this->current_bdd = bdd_false();
    else
        this->current_bdd = bdd_false();
    while (true) {
        int literal = stoi(this->current_token);
        bdd bdd = bdd_ithvar(abs(literal) - 1);
        if (literal > 0) {
            if (this->cnf) {
                this->current_bdd = this->current_bdd | bdd;
            } else {
                this->current_bdd = this->current_bdd & bdd;
            }
        } else {
            if (this->cnf) {
                this->current_bdd = this->current_bdd | (!bdd);
            } else {
                this->current_bdd = this->current_bdd & (!bdd);
            }
        }
        get_token();
        if (this->current_token == "0") {
            if (this->cnf) {
                this->result = this->result & this->current_bdd;
            } else {
                this->result = this->result | this->current_bdd;
            }
            get_token(); // '\n'
            return;
        }
    }
}

void DimacsParser::export_to_abdd() {
    std::string temp_name = this->output_file;
    temp_name += ".temp";
    FILE *temp = fopen(temp_name.c_str(), "w");
    // fprintf(stderr, "... creating file %s\n", this->output_file.c_str());
    if (temp == NULL) {
        fprintf(stderr, "BlifParser: export_to_abdd():");
        fprintf(stderr, "failed to open file '%s.temp'\n", this->output_file.c_str());
        return;
    }

    // for now I could not find a better way to output the BDD
    // other than outputing the BuDDy format into a temporary file
    // as BuDDy does not seem to offer any way to parse the bdd itself manually
    bdd_fprinttable(temp, this->result);
    fclose(temp);
    temp = fopen(temp_name.c_str(), "r");
    if (temp == NULL) {
        fprintf(stderr, "BlifParser: export_to_abdd():");
        fprintf(stderr, "failed to re-open file '%s.temp'\n", this->output_file.c_str());
        return;
    }
    // this->output_file = this->name + this->construct_counter;
    // this->output_file = "./benchmarks/" + this->name + ".var" + std::to_string(this->clausules_count) + ".abdd";
    // printf("%s\n", this->output_file.c_str());
    FILE *f = fopen(this->output_file.c_str(), "w");

    fprintf(f, "@BDD\n");
    fprintf(f, "# imported from %s\n", this->input_file.c_str());
    fprintf(f, "%%Vars %d\n", this->variables_count);
    fprintf(f, "# Variable mapping (from original file):\n");

    // fprintf(f, "#");
    // for (auto &it: this->var_map)
    //     fprintf(f, " %s:%d", it.first.c_str(), it.second);
    // fprintf(f, "\n");

    fprintf(f, "%%Root %d\n\n", this->result.id());

    std::string line;
    int c;
    while ((c = fgetc(temp)) != EOF) {
        if (c != '\n') {
            line += c;
            continue;
        }
        const std::regex edge_regex("\\[\\s*(\\d*)\\]\\s*(\\d*):\\s*(\\d*)\\s*(\\d*)");
        std::smatch group;
        if (std::regex_search(line, group, edge_regex)) {
            // [node-num] var: low high
            if (group.size() == 5) {
                std::string current_node = group[1].str();
                std::string variable = group[2].str();
                std::string low_node = group[3].str();
                std::string high_node = group[4].str();
                if (low_node == "0" or low_node == "1")
                    low_node = "<" + low_node + ">";
                if (high_node == "0" or high_node == "1")
                    high_node = "<" + high_node + ">";
                fprintf(f, "%s[%s] %s %s\n", 
                    current_node.c_str(),
                    variable.c_str(),
                    low_node.c_str(),
                    high_node.c_str()
                );
            }
        }
        line = "";
    }
    fprintf(f, "\n");
    fclose(f);
    fclose(temp);
    remove(temp_name.c_str());
    return;
}


int main(/*int argc, char **argv*/) {
    // if (argc < 3) {
    //     fprintf(stderr, "missing args\n");
    //     return 1;
    // }
    int benchmark_start = 1;
    int benchmark_end = 1000;

    // std::string input_path = argv[1];
    // std::string output_path = argv[2];

    DimacsParser parser = DimacsParser("", "");
    bdd_init(100000, 100000);
    for(int i = benchmark_start; i <= benchmark_end; i++) {
        struct stat sb;
        if (!(stat("../data/uf20/", &sb) == 0 && S_ISDIR(sb.st_mode))) {
            int result = mkdir("../data/uf20/", 0777);
            if (result != 0) {
                fprintf(stderr, "DimacsParser: could not create ");
                fprintf(stderr, "folder '../data/uf20/' for outputs\n");
                return 1;
            }
        }
        parser.reset();
        parser.input_file = "../benchmark/dimacs/uf20/uf20-0"+ std::to_string(i)+  ".cnf";
        parser.output_file = "../data/uf20/uf20-0" + std::to_string(i) + ".abdd";
        parser.tokenize();
        parser.parse();
        parser.export_to_abdd();
        bdd_printtable(parser.result);
        printf("node count = %d\n", bdd_nodecount(parser.result));
    }
    bdd_done();

    return 0;
}
