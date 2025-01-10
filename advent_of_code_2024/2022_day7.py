'''
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?

'''

from pathlib import Path
from rich import print
from copy import deepcopy
from dataclasses import dataclass, field
from typing import NamedTuple, Optional
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day7_example.txt'
INPUT = DATA_DIR / '2022_day7_input.txt'

@dataclass
class File():
    name: str
    size: int
    dir_name: str

@dataclass
class Directory():
    id: int
    level: int
    name: str
    parent: Optional['Directory'] = field(default=None, repr=False)
    files: list[File] = field(default_factory=list)
    children: list['Directory'] = field(default_factory=list)

    @property
    def children_names(self) -> list[str]:
        return [dir.name for dir in self.children]

    @property
    def total_size(self) -> int:
        if len(self.children) == 0:
            return sum(file.size for file in self.files)
        else:
            return sum(file.size for file in self.files) + sum(dir.total_size for dir in self.children)

@dataclass
class Filesystem():
    terminal_output: list[str]
    dir_list: list[Directory]

    def find_dir_by_name(self, name: str) -> Directory:
        try:
            return next(dir for dir in self.dir_list if dir.name == name)
        except StopIteration:
            raise FileNotFoundError(f"Directory \"{name}\" not found in filesystem.")

    @property
    def dir_names(self) -> list[str]:
        return [dir.name for dir in self.dir_list]

    def populate_children(self):
        for dir in self.dir_list:
            if dir.parent is not None:
                dir.parent.children.append(dir)

    def populate_files(self):
        current_dir = self.find_dir_by_name('/')
        for line in self.terminal_output:
            if line == '$ cd ..':
                if current_dir.parent is None:
                    current_dir = self.find_dir_by_name('/')
                else:
                    current_dir = self.find_dir_by_name(current_dir.parent.name)
            elif line.startswith('$ cd'):
                dir_name = line.removeprefix('$ cd ')
                current_dir = self.find_dir_by_name(dir_name)
            elif line[0].isdigit():
                file_size, file_name = line.split(' ')
                file = File(file_name, int(file_size), current_dir.name)
                current_dir.files.append(file)
            # elif line.startswith('dir'):
            #     child_dir_name = line.removeprefix('dir ')
            #     if child_dir_name in current_dir.children_names:
            #         continue
            #     else:
            #         current_dir.children.append(self.find_dir_by_name(child_dir_name))
            else:
                continue

    def get_part_one_answer(self) -> int:
        # for dir in self.dir_list:
        #     print(f"Directory {dir.name} has total size:  {dir.total_size}")
        return sum(dir.total_size for dir in self.dir_list if dir.total_size <= 100_000)
                

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def create_filesystem(terminal_output: list[str]) -> Filesystem:  
    dir_list = [Directory(id=0, level=0, name='/')]
    dir_level = 0
    for line in terminal_output:
        if line == '$ cd /':
            dir_level = 0
            continue
        if line == '$ cd ..':
            dir_level =- 1 if dir_level > 0 else 0
            continue
        if line == '$ ls':
            continue
        if line.startswith('$ cd'):
            dir_name = line.removeprefix('$ cd ')
            parent = dir_list[-1] if dir_level > 0 else dir_list[0]
            dir_level += 1   
            dir_list.append(Directory(id=len(dir_list),
                                        level=dir_level, 
                                        name=dir_name,
                                        parent=parent))
    return Filesystem(terminal_output, dir_list)


        
# def find_directory_sizes(terminal_output: list[str]) -> list[File]:
#     output_list = []
#     current_dir_name = '/'
#     for line in terminal_output:
#         if 

def part_one(filename: Path):
    terminal_output = ingest_data(filename)
    filesystem = create_filesystem(terminal_output)
    filesystem.populate_children()
    filesystem.populate_files()
    # print(filesystem)
    return filesystem.get_part_one_answer()

def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 95437
    print(f"Part One (input):  {part_one(INPUT)}") # 932962 is too low
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") #
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()