import re
import os


def checkVariableNaming(file):
    variable_map: dict[int, set[str]] = {}
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] not in [".inputs", ".outputs", ".names"]:
            continue
        for i in words[1:]:
            # print(i)
            # for j in matches:
            match = re.search(r"\(([^()]*)\)", i)
            if match:
                var = int(match.group(0)[1:-1])
                if var not in variable_map:
                    variable_map[var] = set([i])
                if i not in variable_map[var]:
                    print(f"{file.name}:{idx}: trying to add '{i}' to variable {var} = {variable_map[var]}")


def checkOutputs(file):
    outputs_initial = set()
    inputs_initial = set()
    current_outputs = set()
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".outputs":
            for i in line.split()[1:]:
                outputs_initial.add(i)
        if words[0] == ".inputs":
            for i in line.split()[1:]:
                inputs_initial.add(i)
        if words[0] == ".names":
            output = words[-1]
            current_outputs.add(output)
    file.seek(0)
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".names":
            output = words[-1]
            for i in words[1:-1]:
                if i in current_outputs:
                    if i in outputs_initial:
                        print(f"{file.name}:{idx}: initial .outputs entry {i} used as input")
                    current_outputs.remove(i)
    sorted_initial = list(outputs_initial)
    sorted_final = list(current_outputs)
    sorted_initial.sort()
    sorted_final.sort()
    for i in current_outputs:
        if i not in outputs_initial:
            print(f"{file.name}: output variable {i} not in .outputs line")
    sorted_difference = []
    for i in outputs_initial:
        if i not in current_outputs:
            print(f"{file.name}: initial .outputs variable {i} used as input")
            sorted_difference.append(i)
    sorted_difference.sort()
    print(file.name)
    print(f".outputs =", sorted_initial)
    print(f"not used =", sorted_final)
    print(f"diff     =", sorted_difference)


def checkDuplicateOutputs(file):
    output_occurence: dict[str, int] = {}  # variable -> line-number in file
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".names":
            output = words[-1]
            if output not in output_occurence:
                output_occurence[output] = idx
            else:
                print(f"{file.name}:{idx}: duplicate occurence of {output} as output detected (first on line {output_occurence[output]})")


def checkHierarchy(file):
    inputs_initial = set()
    outputs_parsed = set()
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".inputs":
            for i in words[1:]:
                inputs_initial.add(i)
        if words[0] == ".names":
            output = words[-1]
            for i in words[1:-1]:
                if i in inputs_initial:
                    continue
                if i not in outputs_parsed:
                    print(f"{file.name}:{idx}: unparsed variable {i} used as an input")
            outputs_parsed.add(output)



if __name__ == "__main__":
    benchmarks = [432, 499, 880, 1355, 1908, 2670, 3540, 5315, 6288, 7552]
    files = []
    for num in benchmarks:
        path = f"./tests/blif/C{num}.blif"
        file = open(path, "r")
        checkVariableNaming(file)
        checkOutputs(file)
        checkDuplicateOutputs(file)
        checkHierarchy(file)


