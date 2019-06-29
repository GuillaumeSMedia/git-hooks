#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Pre-Commit check
   for PHP/JS/CSS/SCSS projects

   => Module 'Code Quality'
"""

__author__ = "Guillaume C."
__copyright__ = "Copyright 2019, Spicle Labs"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Guillaume C."
__email__ = "lab@spicle.com"
__status__ = "Production"

import os
import re
import subprocess
import sys
import shutil

modified = re.compile(r'^(?:M|A)(\s+)(?P<name>.*)')

CHECKS = [
    {
        'check_type': 'PHP',  # For display only
        'output': 'Looking for dump, die, dd, print_r statements...',
        'command': 'grep',
        'command_options': "-n -e 'dump(' -e 'die(' -e 'dd(' -e 'print_r(' %s /dev/null",
        'match_files': [r'.*\.php$'],
        'multi_files': True,
        'print_filename': True
    },
    {
        'check_type': 'PHP',
        'output': 'Checking syntax...',
        'command': 'phpcs',
        'command_options': '--standard=PSR2 %s',
        'dependency_instructions': 'pear install PHP_CodeSniffer',
        'match_files': [r'.*\.php$'],
        'multi_files': True,
        'print_filename': True,
    },
    {
        'check_type': 'JS',
        'output': 'Looking for console.log() or debugger...',
        'command': 'grep',
        'command_options': '-n -e console.log -e debugger %s',
        'match_files': [r'.*\.js$'],
        'multi_files': True,
        'print_filename': True,
    },
    {
        'check_type': 'JS',
        'output': 'Running Jshint...',
        'command': 'jshint',
        # By default, jshint prints 'Lint Free!' upon success. We want to filter this out.
        'command_options': '%s | grep -v "Lint Free!"',
        'match_files': [r'.*\.js$'],
        'multi_files': True,
        'print_filename': False,
    },
    {
        'check_type': 'CSS/SASS',
        'output': 'Running linter...',
        'command': './node_modules/.bin/stylelint',
        'command_options': '--formatter verbose --allow-empty-input %s',
        'match_files': [r'.*\.(s[ac]ss|css|html)$'],
        'multi_files': True,
        'print_filename': True,
    },
]

# Define output colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    ENDC = '\033[0m'


# Checks if a command exists on the current system
def cmd_exists(cmd):

    # Python < 3.3
    from distutils.spawn import find_executable
    return find_executable(cmd) is not None

    # Python >= 3.3
    # from shutil import which
    # return shutil.which(cmd) is not None


def matches_file(file_name, match_files):
    return any(re.compile(match_file).match(file_name) for match_file in match_files)


def check_files(files, check):
    result = 0
    matched_files = []

    # List the files that match the specific test
    for file_name in files:
        if not 'match_files' in check or matches_file(file_name, check['match_files']):
            if not 'ignore_files' in check or not matches_file(file_name, check['ignore_files']):

                if (check['multi_files']):
                    matched_files.append(file_name)
                else:
                    process = subprocess.Popen(check['command']+' '+check['command_options'] %
                                               file_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = process.communicate()

    # Skip to next test if no files match the current test pattern
    if(len(matched_files) == 0):
        return

    # Skip check if the parser/linter does not exist on this system
    if not cmd_exists(check['command']):
        print
        print(bcolors.WARNING + check['check_type'] + ' - Skipping check "' +
              check['output'] + '": command "'+check['command']+'" is not present' + bcolors.ENDC)

        # Are there instructions on how to install the missing dependency?
        if 'dependency_instructions' in check:

            # Print the instruction (with a nicer aligment to above text)
            print((len(check['check_type']) + 3) * ' ') + bcolors.WARNING + 'To install it: ' + \
                bcolors.ITALIC + \
                check['dependency_instructions'] + bcolors.ENDC

        return

    # Display the test's name
    print
    print(check['check_type'] + ' - ' + check['output'])

    # Run the test
    process = subprocess.Popen(
        (check['command']+' ' + check['command_options']) % ' '.join(matched_files), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()

    # Any errors/output?
    if out or err:
        print

        prefix = '\t'
        output_lines = [(bcolors.FAIL + '%s%s' + bcolors.ENDC) %
                        (prefix, line) for line in out.splitlines()]
        print('\n'.join(output_lines))

        if err:
            print(bcolors.FAIL + err + bcolors.ENDC)
        result = 1

    return result


def main(all_files):

    # List the files that need to be analysed
    files = []
    if all_files:
        for root, dirs, file_names in os.walk('.'):
            for file_name in file_names:
                files.append(os.path.join(root, file_name))
    else:
        p = subprocess.Popen(
            ['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            match = modified.match(line)
            if match:
                files.append(match.group('name'))

    result = 0

    for check in CHECKS:
        result = check_files(files, check) or result

    # Return exit code
    sys.exit(result)


if __name__ == '__main__':
    all_files = False
    if len(sys.argv) > 1 and sys.argv[1] == '--all-files':
        all_files = True
    main(all_files)
