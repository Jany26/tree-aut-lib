#include "blif_parser.h"

template<typename V>
void print_tokens(std::string preface, std::vector<V> vector) {
    std::cout << preface << " = [ ";
    for (auto i: vector) {
        if (i == "\n") std::cout << "EOL" << ' ';
        else std::cout << i << ' ';
    }
    std::cout << "]" << std::endl;
}

template<typename K, typename V>
void print_unordered_map(std::string preface, std::unordered_map<K, V> const &m)
{
    std::cout << preface << " = {" << std::endl;
    for (auto const &pair: m) {
        std::cout << "  " << pair.first << ": " << pair.second << "\n";
    }
    std::cout << "}" << std::endl;
}

void BlifParser::print() {
    std::cout << "\n[--BlifParserContentStart--]\n";
    std::cout << "> input = " << this->input_file << std::endl;
    std::cout << "> output = " << this->output_file << std::endl;
    std::cout << "  name = " << this->name << std::endl;
    print_tokens("  tokens", this->tokens);
    // std::cout << "current_token = " << this->current_token << std::endl;
    PRINT_SET("  inputs", this->inputs);
    PRINT_SET("  outputs", this->outputs);


    std::cout << "  var -> num : [dependency] = {\n";
    for (auto i : this->parsed_constructs) {
        std::cout << "    " << i.first << "\t-> " <<  this->var_map[i.first] << "\t: [ ";
        for (auto j : i.second.inputs) std::cout << this->var_map[j] << " ";
        std::cout << "]\n";
    }
    std::cout << "  }\n";
    std::cout << "[---BlifParserContentEnd---]\n";
}

void BlifParser::tokenize() {
    this->tokens = {};
    FILE *file = fopen(this->input_file.c_str(), "r");
    if (file == NULL) {
        fprintf(stderr, "couldn't open input file %s\n", input_file.c_str());
        exit(EXIT_FAILURE);
    }
    std::string line = "";
    int c;
    while ((c = fgetc(file)) != EOF) {
        if (c != '\n') {
            line += c;
            continue;
        } 
        if (line.length() == 1 or line[0] == '#') {
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

void BlifParser::create_orders() {
    for (auto i: this->outputs) {
        std::vector<std::string> order = {};

        std::list<std::string> queue;
        queue.push_back(i);
        std::string current;
        while (!queue.empty()) {
            current = queue.front();
            order.push_back(current);
            queue.pop_front();
            if (this->parsed_constructs.find(current) == this->parsed_constructs.end()) {
                continue;
            }
            for (auto dependency : this->parsed_constructs[current].inputs) {
                queue.push_back(dependency);
            }
        }
        
        std::cout << i << " => ";
        PRINT_VECTOR("order", order);
    }
};

void BlifParser::initial_parse() {
    // temporary set for storing all found variable strings
    std::unordered_set<std::string> vars = {};
    int i = 0;
    // std::unordered_set<std::string> keywords = {".inputs", ".outputs", ".names", };

    while (i < (int) this->tokens.size()) {
        if (this->tokens[i] == ".inputs" or this->tokens[i] == ".outputs") {
            i++; // skip keyword
            while (this->tokens[i] != "\n") {
                if (this->tokens[i] == "\\") {
                    i+=2; // skip \ and \n right after
                    continue;
                }
                vars.insert(this->tokens[i++]);
            }
            i++; // skip \n
            continue;
        }
        if (this->tokens[i] != ".names") {
            i++; 
            continue;
        }
        i++; // .names
        this->construct_total++;
        names_construct current_construct = {.inputs = {}, .gates = {},
            .output_order = {}, .bdd_created = false, .resulting_bdd=bdd_false()
        };

        std::string last_variable;
        // .names in-1 in-2 ... in-n out
        while (this->tokens[i] != "\n") {
            if (this->tokens[i] == "\\") {
                i+=2; // skip \ and \n right after
                continue;
            }
            last_variable = this->tokens[i];
            current_construct.inputs.push_back(last_variable);
            if (vars.find(this->tokens[i]) == vars.end())
                vars.insert(this->tokens[i]);
            i++;
        }
        current_construct.inputs.pop_back();
        i++;
        do {
            std::string values = this->tokens[i++];
            std::string res = this->tokens[i++];
            int stored = stoi(res);
            current_construct.gates.push_back(std::make_pair(values, (bool) stored));
            if (this->tokens[i] == "\n") i++;
        } while (this->tokens[i] != ".names" and this->tokens[i] != ".end");
        this->parsed_constructs[last_variable] = current_construct;
    }
    if (!this->smartvars) {
        this->var_map = {};
        for (const auto &var: vars) {
            this->var_map[var] = this->var_counter;
            this->var_counter++;
        }
    } else {
        const std::regex var_regex("\\(([^(^)]*)\\)"); // finding the inside content of parentheses
        std::smatch group;
        for (const auto &var : vars) {
            if (std::regex_search(var, group, var_regex)) {
                if (group.size() == 2) { // first = whole string, second = paranthesized expr.
                    std::ssub_match sub_match = group[1];
                    std::string var_number = sub_match.str();
                    this->var_map[var] = atoi(var_number.c_str());
                }
            } else {
                fprintf(stderr, "BlifParser.initial_parse():");
                fprintf(stderr, "could not extract content inside () of variable '%s'\n", var.c_str());
                fprintf(stderr, "... trying to typecast into integer\n");
                this->var_map[var] = atoi(var.c_str());
            }
        }
    }


    // checking if every gate has consistent number of inputs
    for (auto it : this->parsed_constructs) {
        auto inputs_number = it.second.inputs.size();
        for (auto it2 : it.second.gates) {
            if (it2.first.length() != inputs_number) {
                fprintf(stderr,
                "inconsistent numbers of inputs for gate outputting '%s'\n",
                it.first.c_str());
            }
        }
    }
}

void BlifParser::export_to_abdd() {
    if (access(this->output_file.c_str(), F_OK) == 0) {
        remove(this->output_file.c_str());
    }
    if (this->parsing == CHARACTERISTIC_FUNCTION) {
        export_to_abdd_append_result();
    } else if (this->parsing == OUTPUT_FUNCTION) {
        for (auto &it : this->bdd_map) {
            // printf("it.first = %d\n", it.first);
            // // printf("it.second")
            // printf("it.second.second = %d\n", it.second.second);
            // bdd_printtable(it.second.first);
            if (it.second.second) {
                continue;
            }
            this->result = it.second.first;
            this->construct_counter = it.first;
            export_to_abdd_append_result();
        }
    }
}

void BlifParser::export_to_abdd_append_result() {
    std::string temp_name = this->output_file;
    temp_name += ".temp";
    FILE *temp = fopen(temp_name.c_str(), "w");
    struct stat sb;
    if (!(stat(this->output_file.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode))) {
        int result = mkdir(this->output_file.c_str(), 0777);
        if (result != 0) {
            fprintf(stderr, "BlifParser: export_to_abdd(): could not create ");
            fprintf(stderr, "folder '%s' for outputs\n", this->output_file.c_str());
            return;
        }
    }

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

    std::string output_file_str = this->output_file + "/" + this->name + ".var" + std::to_string(this->construct_counter) + ".abdd";
    FILE *f = fopen(output_file_str.c_str(), "w");
    if (f == NULL) {
        fprintf(stderr, "failed to open file '%s'\n", output_file_str.c_str());
        exit(EXIT_FAILURE);
    }

    fprintf(f, "@BDD\n");
    fprintf(f, "# imported from %s\n", this->input_file.c_str());
    if (this->parsing == OUTPUT_FUNCTION) {
        fprintf(f, "%%Name %s.var%d\n", this->name.c_str(), this->construct_counter);
    } else {
        fprintf(f, "%%Name %s\n", this->name.c_str());
    }
    fprintf(f, "%%Vars %ld\n", this->var_map.size());
    fprintf(f, "# Variable mapping (from original file):\n");

    fprintf(f, "#");
    for (auto &it: this->var_map)
        fprintf(f, " %s:%d", it.first.c_str(), it.second);
    fprintf(f, "\n");

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

void BlifParser::export_to_vtf() {
    // dumping bdd to temp file
    std::string temp_name = this->output_file;
    temp_name += ".temp";
    FILE *temp = fopen(temp_name.c_str(), "w");
    fprintf(stderr, "... creating file %s\n", this->output_file.c_str());
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

    // parsing the dump file
    temp = fopen(temp_name.c_str(), "r");
    if (temp == NULL) {
        fprintf(stderr, "BlifParser: export_to_abdd():");
        fprintf(stderr, "failed to re-open file '%s.temp'\n", this->output_file.c_str());
        return;
    }

    std::unordered_set<int> states;
    std::vector<std::vector <int>> node_data = {};
    std::string line;
    std::vector<int> line_data;

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
                line_data = {
                    stoi(group[1].str()), // node-number
                    stoi(group[2].str()), // variable
                    stoi(group[3].str()), // low node
                    stoi(group[4].str()), // high node
                };
                if (states.find(line_data[0]) == states.end())
                    states.insert(line_data[0]);
                if (states.find(line_data[2]) == states.end())
                    states.insert(line_data[2]);
                if (states.find(line_data[3]) == states.end())
                    states.insert(line_data[3]);
                node_data.push_back(line_data);
            }
        }
        line = "";
    }

    FILE *f = fopen(this->output_file.c_str(), "w");

    fprintf(f, "@NTA\n");
    fprintf(f, "# imported from %s\n", this->input_file.c_str());
    fprintf(f, "%%Root %d\n", this->result.id());

    fprintf(f, "%%States");
    for (auto &s: states)
        fprintf(f, " %d:0", s);
    fprintf(f, " 0:0 1:0\n");

    fprintf(f, "# Variable mapping (from original file):\n");
    fprintf(f, "#");
    for (auto &it: this->var_map)
        fprintf(f, " %s:%d", it.first.c_str(), it.second);
    fprintf(f, "\n");

    fprintf(f, "%%Alphabet LH:2 0:0 1:0\n\n");
    for (auto &vec : node_data) {
        fprintf(f, "%d LH <%d> ( %d %d )\n", vec[0], vec[1], vec[2], vec[3]);
    }
    fprintf(f, "0 0 ( )\n");
    fprintf(f, "1 1 ( )\n");
    fclose(f);
    fclose(temp);
    remove(temp_name.c_str());
    return;
}

std::string BlifParser::get_token() {
    this->current_token = this->tokens[0];
    this->tokens.erase(this->tokens.begin());
    return this->current_token;
}

void BlifParser::characteristic_function_parse() {
    get_token();
    std::unordered_set<std::string> keywords = {".model", ".inputs", ".outputs", ".names", ".end"};
    if (keywords.find(this->current_token) == keywords.end()) {
        fprintf(stderr, "Unsupported construct: %s\n", this->current_token.c_str());
    } else if (this->current_token == ".end") {
        get_token();
        return;
    } else if (this->current_token == ".model") {
        this->name = get_token();
        get_token(); // '\n'
    } else if (this->current_token == ".inputs") {
        inputs_list();
    } else if (this->current_token == ".outputs") {
        outputs_list();
        // create_orders();
    } else if (this->current_token == ".names") {
        this->names = {};
        names_list();
        build_var_dependency();
        names_content_characteristic();
        this->result = this->current_bdd & this->result;
        this->current_bdd = bdd_false();
        this->construct_counter += 1;
    } else {
        fprintf(stderr, "BlifParser: unsupported construct: %s\n", this->current_token.c_str());
    }
    characteristic_function_parse();
}

void BlifParser::inputs_list() {
    get_token();
    if (this->current_token == "\n") {
        return;
    }
    this->inputs.insert(this->current_token);
    int var = this->var_map[this->current_token];
    this->names_map[var] = {};
    inputs_list();
}

void BlifParser::outputs_list() {
    get_token();
    if (this->current_token == "\n") {
        return;
    }
    this->outputs.insert(this->current_token);
    outputs_list();
}

void BlifParser::names_list() {
    get_token();
    if (this->current_token == "\\") {
        get_token(); // skip backslash
        get_token(); // skip immediate following newline
        names_list();
    }
    if (this->current_token == "\n") {
        return;
    }
    this->names.push_back(this->var_map[this->current_token]);
    names_list();
}

void BlifParser::names_content_characteristic() {
    bdd input_paths = bdd_false();
    std::string input_plane, output;
    std::vector<std::pair<int, char>> assignment;
    while (this->tokens[0] != ".names" and this->tokens[0] != ".end") {
        input_plane = get_token();
        output = get_token();
        assignment = {};
        // itearting until size - 1 because the last name is output
        for (int i = 0; i < (int) this->names.size() - 1; ++i) {
            // assignment consists of pairs - (var_number, its_value)
            assignment.push_back(std::make_pair(this->names[i], input_plane[i]));
        }
        std::sort(assignment.begin(), assignment.end());
        
        bdd path = bdd_true();

        for (auto &pair : assignment) {
            int var = pair.first;
            char bit = pair.second;
            if (bit == '-')
                continue;
            bdd bdd = bdd_ithvar(var);

            if (bit == '1')
                path = path & bdd;
            else
                path = path & (!bdd);
        }
        input_paths = input_paths | path;
        while (this->tokens[0] == "\n") get_token();
    }
    bdd output_var = bdd_ithvar(this->names.back());
    if (output == "1") {
        this->current_bdd = (input_paths & output_var) | ((!input_paths) & (!output_var));
    } else {
        this->current_bdd = (input_paths & (!output_var)) | ((!input_paths) & output_var);
    }
}

void BlifParser::names_content_check() {
    bool return_set = false;
    int return_val;
    while (this->tokens[0] != ".names" and this->tokens[0] != ".end") {
        get_token(); // PLA field, can only contain characters '0', '1', '-'
        for (int i = 0; i < (int) this->current_token.length(); i++) {
            char c = this->current_token[i];
            if (c == '-' or c == '0' or c == '1') {
                continue;
            } else {
                fprintf(stderr, "unsupported character in names PLA field '%s'\n", this->current_token.c_str());
                exit(EXIT_FAILURE);
            }
        }
        if (this->current_token.length() != this->names.size() - 1) {
            fprintf(stderr, "inconsistent length of PLA field '%s' with names\n", this->current_token.c_str());
            exit(EXIT_FAILURE);
        }
        get_token(); // output value '0' or '1' => should be consistent through all lines of 1 construct
        if (this->current_token != "0" and this->current_token != "1") {
            fprintf(stderr, "unsupported character in names output field '%s'\n", this->current_token.c_str());
            exit(EXIT_FAILURE);
        }
        int ret = stoi(this->current_token);
        if (return_set) {
            if (ret != return_val) {
                fprintf(stderr, "inconsistent return value for .names construct");
                exit(EXIT_FAILURE);
            }
        } else {
            return_set = true;
            return_val = ret;
        }
        get_token(); // final \n
    }
}

void BlifParser::output_function_parse() {
    get_token();
    std::unordered_set<std::string> keywords = {".model", ".inputs", ".outputs", ".names", ".end"};
    if (keywords.find(this->current_token) == keywords.end()) {
        fprintf(stderr, "Unsupported construct: %s\n", this->current_token.c_str());
    } else if (this->current_token == ".end") {
        get_token();
        if (this->construct_counter == this->construct_total) {
            return;
        } else {
            fprintf(stderr, "did not parse all constructs\n");
            return;
        }
    } else if (this->current_token == ".model") {
        this->name = get_token();
        get_token(); // '\n'
    } else if (this->current_token == ".inputs") {
        inputs_list_output();
    } else if (this->current_token == ".outputs") {
        outputs_list();
        // create_orders();
    } else if (this->current_token == ".names") {
        this->names = {};
        names_list();
        if (this->recursive) {
            names_content_check();
        } else {
            build_var_dependency();
            names_content_output();
        }
        this->construct_counter += 1;
    }
    output_function_parse();
};

void BlifParser::inputs_list_output() {
    get_token();
    if (this->current_token == "\n") {
        return;
    }
    this->inputs.insert(this->current_token);
    int var = this->var_map[this->current_token];
    this->bdd_map[var] = std::make_pair(bdd_ithvar(var), false);
    this->names_map[var] = {};
    inputs_list_output();
}

void BlifParser::names_content_output() {
    bdd input_paths = bdd_false();
    std::string input_plane, output;
    std::vector<std::pair<int, char>> assignment;

    while (this->tokens[0] != ".names" and this->tokens[0] != ".end") {
        input_plane = get_token();
        output = get_token();
        assignment = {};
        // itearting until size - 1 because the last name is output
        for (int i = 0; i < (int) this->names.size() - 1; ++i) {
            // assignment consists of pairs - (var_number, its_value)
            assignment.push_back(std::make_pair(this->names[i], input_plane[i]));
        }
        // std::sort(assignment.begin(), assignment.end()); // not sure if needed
        
        bdd path = bdd_true();

        for (auto &pair : assignment) {
            int var = pair.first;
            char bit = pair.second;
            if (bit == '-')
                continue;
            bdd bdd = this->bdd_map[var].first;
            this->bdd_map[var].second = true;

            if (bit == '1')
                path = path & bdd;
            else
                path = path & (!bdd);
        }
        input_paths = input_paths | path;
        while (this->tokens[0] == "\n") get_token();
    }
    if (output == "1") {
        this->bdd_map[this->names.back()] = std::make_pair(input_paths, false);
    } else {
        this->bdd_map[this->names.back()] = std::make_pair(!(input_paths), false);
    }
};

void BlifParser::create_all_outputs() {
    for (std::string output : this->outputs) {
        if (!this->parsed_constructs[output].bdd_created) {
            this->parsed_constructs[output].bdd_created = true;
            this->parsed_constructs[output].resulting_bdd = create_output_bdd(output);
        }
        this->bdd_map[this->var_map[output]] =  std::make_pair(
            this->parsed_constructs[output].resulting_bdd, false
        );
    }
}

bdd BlifParser::create_output_bdd(std::string variable) {
    std::unordered_map<std::string, bdd> bdd_assignment;

    for (auto input : this->parsed_constructs[variable].inputs) {
        // if var has no corresponding bdd:
        if (this->var_bdd_map.find(input) == this->var_bdd_map.end()) {
            // if var is an input
            if (this->inputs.find(input) != this->inputs.end()) {
                this->var_bdd_map[input] = bdd_ithvar(this->var_map[input]);
            } else {
                this->var_bdd_map[input] = create_output_bdd(input);
                this->parsed_constructs[input].bdd_created = true;
                this->parsed_constructs[input].resulting_bdd = current_bdd;
            }
        }
        // assign a BDD to each input
        bdd_assignment[input] = this->var_bdd_map[input];
        this->bdd_map[this->var_map[input]] = std::make_pair(
            this->var_bdd_map[input], true
        );
    }

    bdd result = bdd_false();
    std::string input_plane;
    bool output;
    names_construct current_construct = this->parsed_constructs[variable];
    for (auto line : current_construct.gates) {
        input_plane = line.first;
        output = line.second;
        bdd path = bdd_true();
        for (int i = 0; i < (int) input_plane.length(); i++) {
            // assignment
            if (input_plane[i] == '-') {
                continue;
            }
            if (input_plane[i] == '0') {
                path = path & !bdd_assignment[current_construct.inputs[i]];
            } else {
                path = path & bdd_assignment[current_construct.inputs[i]];
            }
        }
        result = result | path;
    }
    return output ? result : !result;
}

void BlifParser::pick_result() {
    int max_bdd;
    int max_nodes = 0;
    int total_nodes = 0;
    // this->print();
    if (this->parsing == CHARACTERISTIC_FUNCTION) {
        int total_nodes = bdd_nodecount(this->result);
        fprintf(stderr, "total node count = %d\n", total_nodes);
        return;
    }
    // it => <int=var, < bdd, bool=used> -> if bool=false, bdd is output
    for (auto &it : this->bdd_map) {
        if (it.second.second) { // skip bdds, that were used as in input somewhere
            continue;
        }
        int node_count = bdd_nodecount(it.second.first);
        // fprintf(stderr, "var %d partial = %d\n", it.first, node_count);
        total_nodes += node_count;
        if (node_count > max_nodes) {
            max_bdd = it.first;
            max_nodes = node_count;
        }
    }
    fprintf(stderr, "total node count = %d\n", total_nodes);
    this->result = this->bdd_map[max_bdd].first;
}

void BlifParser::build_var_dependency() {
    int output = this->names.back();
    this->names_map[output] = {};
    // printf("build_var_dependency()\n");
    for (int i = 0; i < (int) this->names.size() - 1; ++i) {
        int input = this->names[i];
        this->names_map[output].push_back(input);
        // printf("[%d] += %d\n", output, input);
    }

}

void var_label_dfs(
    std::unordered_map<int, std::vector<int>> reference,
    std::unordered_set<int> &visited,
    std::vector<int> &result, 
    int variable
) {
    if (visited.find(variable) != visited.end())
        return;
    visited.insert(variable);
    result.push_back(variable);
    for (auto &var : reference[variable]) {
        var_label_dfs(reference, visited, result, var);
    }
}

void BlifParser::variable_order_dfs() {
    std::vector<int> outputs = {};
    std::unordered_set<int> used = {};
    for (auto &it : this->names_map)
        for (auto &it2 : it.second)
            used.insert(it2);
    for (auto &it : this->names_map)
        if (used.find(it.first) == used.end())
            outputs.push_back(it.first);
    this->var_order = {};
    std::unordered_set<int> visited = {};
    for (auto &var : outputs) {
        var_label_dfs(this->names_map, visited, this->var_order, var);
    }

    // PRINT_VECTOR("order", this->var_order);
    if (this->parsing == CHARACTERISTIC_FUNCTION)
        return;
    used = {};
    for (auto &name : this->inputs) {
        used.insert(this->var_map[name]);
    }
    std::vector<int> to_remove = {};
    for (int i = 0; i < (int) this->var_order.size(); ++i)
        if (used.find(this->var_order[i]) == used.end())
            to_remove.push_back(i);
    // for (auto &idx : to_remove)
    for (int i = to_remove.size() - 1; i >= 0; --i)
        this->var_order.erase(this->var_order.begin() + to_remove[i]);
    // PRINT_VECTOR("order", this->var_order);
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "missing arguments" << std::endl;
        return 1;
    }


    std::string blif_input = argv[1];
    std::string output_file_name = argv[2];
    
    BlifParser parser = BlifParser(blif_input, output_file_name, OUTPUT_FUNCTION);
    if (argc > 3 and strcmp(argv[3], "rec") == 0) {
        parser.recursive = true;
    }
    if (argc > 4 and strcmp(argv[4], "smartvars") == 0) {
        parser.smartvars = true;
    }
    parser.tokenize();
    parser.initial_parse();
    bdd_init(1000000, 100000);
    bdd_setvarnum((int) parser.var_map.size());
    if (parser.parsing == CHARACTERISTIC_FUNCTION) {
        parser.characteristic_function_parse();
    } else {
        parser.output_function_parse();
        if (parser.recursive) {
            parser.create_all_outputs();
        }
    }
    parser.print();
    parser.variable_order_dfs();
    parser.pick_result();
    parser.export_to_abdd();
    bdd_done();
    return 0;
}
