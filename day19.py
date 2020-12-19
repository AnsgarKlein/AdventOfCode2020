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

def rule_to_regex(rules, rule):
    # Rule contains XOR
    if '|' in rule:
        half1 = rule.split('|')[0].strip()
        half2 = rule.split('|')[1].strip()

        half1_result = rule_to_regex(rules, half1)
        half2_result = rule_to_regex(rules, half2)

        return '(' + half1_result +'|' + half2_result + ')'

    # Rule contains literal
    if '"' in rule:
        match = re.match('"(.*)"', rule.strip())

        return match.group(1)

    # Rule contains concatenation of rules (or just one rule)
    result = ''
    for member in rule.strip().split(' '):
        result += rule_to_regex(rules, rules[int(member)].strip())

    return result

def main():
    # Read input file
    rules_str, inputs = read_input_file('day19_input.txt')
    rules = rules_to_array(rules_str)

    # Convert rules to regex
    regex = '^' + rule_to_regex(rules, rules[0]) + '$'

    # Count input lines matching regex
    count = 0
    for line in inputs:
        match = re.match('^' + regex + '$', line)
        matched = (match is not None)

        if matched:
            count += 1

    print(count)


if __name__ == '__main__':
    main()
