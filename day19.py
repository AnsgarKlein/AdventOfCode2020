#!/usr/bin/env python3

import re

def read_input_file(filename):
    rules = []
    inputs = []

    with open(filename, 'r') as input_file:
        content = input_file.read().split('\n')

        # Rules
        for i, line in enumerate(content):
            if line.strip() == '':
                content = content[i+1:]
                break

            rules.append(line.strip())

        # Input
        for line in content:
            inputs.append(line.strip())

    return rules, inputs

def rules_to_array(rules):
    arr = {}

    for rule in rules:
        rule_index = int(rule.split(':')[0])
        rule_body = rule.split(':')[1]

        arr[rule_index] = rule_body

    return arr

def rule_to_regex(rules, rule, index):
    # Check if rule is a loop
    is_loop_rule = False
    if index in [ int(x) for x in rule.split(' ') if x.isdigit() ]:
        is_loop_rule = True

    # Hardcode loop rule 8
    if is_loop_rule and index == 8:
        return '(' + rule_to_regex(rules, rules[42], 42) + ')+'

    # Hardcode loop rule 11
    if is_loop_rule and index == 11:
        result42 = rule_to_regex(rules, rules[42], 42)
        result31 = rule_to_regex(rules, rules[31], 31)

        txt = '('
        for i in range(10):
            # (42){i}
            txt += '({}){{{}}}'.format(result42, i + 1)

            # (42){i}
            txt += '({}){{{}}}'.format(result31, i + 1)

            txt += '|'
        txt = txt[:-1]
        txt += ')'
        return txt


    # Handle non-hardcoded, non-loop rules

    # Rule contains XOR
    if '|' in rule:
        half1 = rule.split('|')[0].strip()
        half2 = rule.split('|')[1].strip()

        half1_result = rule_to_regex(rules, half1, index)
        half2_result = rule_to_regex(rules, half2, index)

        return '(' + half1_result +'|' + half2_result + ')'

    # Rule contains literal
    if '"' in rule:
        match = re.match('"(.*)"', rule.strip())

        return match.group(1)

    # Rule contains concatenation of rules (or just one rule)
    result = ''
    for member in rule.strip().split(' '):
        result += rule_to_regex(rules, rules[int(member)].strip(), int(member))

    return result

def main():
    # Read input file
    rules_str, inputs = read_input_file('day19_input.txt')
    rules = rules_to_array(rules_str)


    ############ PART ONE ############

    # Convert rules to regex
    regex = '^' + rule_to_regex(rules, rules[0], 0) + '$'

    # Count input lines matching regex
    count = 0
    for line in inputs:
        match = re.match('^' + regex + '$', line)
        matched = (match is not None)

        if matched:
            count += 1

    print('Part One: {}'.format(count))


    ############ PART TWO ############

    # Change rules 8 and 11 (-> loop)
    rules[8] = '42 | 42 8'
    rules[11] = '42 31 | 42 11 31'

    # Convert to regex again
    regex = '^' + rule_to_regex(rules, rules[0], 0) + '$'

    # Count input lines matching regex
    count = 0
    for line in inputs:
        match = re.match(regex, line)
        matched = (match is not None)

        if matched:
            count += 1

    print('Part Two: {}'.format(count))


if __name__ == '__main__':
    main()
