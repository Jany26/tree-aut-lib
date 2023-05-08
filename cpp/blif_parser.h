#include "bdd.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <unordered_set>
#include <cctype>

#ifndef BLIF_PARSER_H
#define BLIF_PARSER_H



#define PRINT_SET(name, set) \
    do { \
        std::cout << name << " = {"; \
        for (auto &it : set) std::cout << " " << it; \
        std::cout << " }" << std::endl; \
    } while(0)

#define PRINT_VECTOR(name, set) \
    do { \
        std::cout << name << " = ["; \
        for (auto &it : set) std::cout << " " << it; \
        std::cout << " ]" << std::endl; \
    } while(0)

template<typename V>
void print_tokens(std::string preface, std::vector<V> vector);

template<typename K, typename V>
void print_unordered_map(std::string preface, std::unordered_map<K, V> const &m);

enum parsing_type { OUTPUT_FUNCTION, CHARACTERISTIC_FUNCTION, };

class BlifParser {
    public:
        std::string input_file;
        std::string output_file;
        std::string name;
        std::vector<std::string> tokens;
        std::string current_token;
        std::vector<std::string> inputs;
        std::vector<std::string> outputs;
        std::vector<int> var_order;
        std::vector<int> names;
        std::unordered_map<int, std::vector<int>> names_map;
        std::unordered_map<std::string, int> var_map;
        int construct_total;
        int construct_counter;
        int var_counter;
        bdd result;
        bdd current_bdd;
        std::unordered_map<int, std::pair<bdd, bool>> bdd_map;
        parsing_type parsing;

        BlifParser(std::string input, std::string output, parsing_type type) {
            this->input_file = input;
            this->output_file = output;
            
            this->name = "";
            this->tokens = {};
            this->inputs = {};
            this->outputs = {};
            this->names = {};
            this->var_map = {};
            this->var_counter = 0;

            this->var_order = {};
            this->names_map = {};
            this->construct_total = 0;
            this->construct_counter = 0;
            this->parsing = type;
            
            this->result = bdd_true();
            this->current_bdd = bdd_false();
            this->bdd_map = {};
        }

        void print();

        void tokenize();
        void initial_parse();  // variable sorting by (inner) names
        
        std::string get_token();

        void characteristic_function_parse();
        void create_temp_struct();
        void inputs_list();
        void outputs_list();
        void names_list();
        void names_content_characteristic();

        void output_function_parse();
        void inputs_list_output();
        void names_content_output();

        void variable_order_dfs();
        void build_var_dependency();

        void pick_result();
        void export_to_abdd();
        void export_to_abdd_append_result();
        void export_to_vtf();
};

#endif // BLIF_PARSER_H
