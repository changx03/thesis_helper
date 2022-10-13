"""Merge multiple LaTex bibliography files and remove duplicates

Author: Luke Chang (luke.x.chang@gmail.com)
Date: 14/10/2022
"""
import argparse
import os
import re
from glob import glob
from pathlib import Path

REG_EXP = '\@[\w]+\{(.*?)\,'  # Match case: "@article{art2018,"


def parse_bibstr(bibstr: str):
    """Return the keyword of the article."""
    match = re.match(REG_EXP, bibstr)
    # match can be None.
    return match.group(1) if match else None


class Article:
    """A LaTex bibliography entry.
    """

    def __init__(self, key: str, bibstr: str) -> None:
        self.key = key
        self.bibstr = bibstr

    def __repr__(self):
        return self.key

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key


def merge(path_input, path_output):
    files = sorted(glob(os.path.join(path_input, '*.bib')))
    print(f'Found {len(files)} bib files.')

    entries = []
    # Traverse all files
    for file in files:
        with open(file, mode='r') as f:
            lines = [row.strip() for row in f.readlines()]
            lines = '\n'.join(lines)
            entries += ['@' + x for x in lines.split('@') if x != '']

    # Traverse all entries
    print(f'Found {len(entries)} bib entries.')
    entry_set = set()
    for bib_txt in entries:
        key = parse_bibstr(bib_txt)
        if key:
            item = Article(key, bib_txt)
            entry_set.add(item)
    print(f'{len(entry_set)} unique entries are saved.')

    with open(path_output, mode='w') as file:
        bib_content = ([x.bibstr + '\n' for x in sorted(list(entry_set))])
        file.writelines(bib_content)
        


if __name__ == '__main__':
    """ Example: 
    python3 ./merge.py -i "./data/bib/"
    """
    parser = argparse.ArgumentParser(description='Merge multiple LaTex \
        bibliography files into one without deduplicate.')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='The input directory that contains the bib files.')
    parser.add_argument('-o', '--output', type=str, default='bibliography.bib',
                        help='The input directory that contains the bib files.')
    args = parser.parse_args()
    path_input = Path(args.input).absolute()
    path_output = Path(args.output).absolute()
    print('Input dir:', path_input)
    print('Output dir:', path_output)

    merge(path_input, path_output)
