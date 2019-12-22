import os
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Generator, Any, Callable

import regex
from graphviz import Digraph


@dataclass
class ParsedLaunchPath:
    package: str
    name: str

    def __str__(self):
        return f'{self.package}/{self.name}'


def parse_path(path: PurePosixPath) -> ParsedLaunchPath:
    if path.parts.count('launch') != 1:
        raise ValueError(f'Launch file path must have exactly one "launch" part ({path})')
    launch_index = path.parts.index('launch')
    if launch_index == 0:
        raise ValueError(f'Launch file path must not start with "launch" part ({path})')
    if launch_index == len(path.parts)-1:
        raise ValueError(f'Launch file path must not end with "launch" part ({path})')
    return ParsedLaunchPath(package=path.parts[launch_index-1], name=path.parts[-1])


def starts_with_dot(path: PurePosixPath) -> bool:
    pattern = regex.compile(r'\.[^.].*')
    return any(regex.fullmatch(pattern, part) is not None for part in path.parts)


def is_launch_file(path: PurePosixPath) -> bool:
    return path.parts[-1].endswith('.launch') or path.parts[-1].endswith('.launch.xml')


def walk_launch_files(base: PurePosixPath, filter_path: Callable[[PurePosixPath], bool]) -> Generator[PurePosixPath, Any, None]:
    for root, dirs, files in os.walk(base.as_posix()):
        for path in (os.path.join(root, name) for name in files):
            path: PurePosixPath = PurePosixPath(path)
            if filter_path(PurePosixPath(path)):
                yield path


def get_includes(text: str) -> Generator[ParsedLaunchPath, Any, None]:
    for match in re.finditer(r'<include file="\$\(find ([^)]+)\)/.*/(.*?\.launch)', text):
        yield ParsedLaunchPath(package=match.group(1), name=match.group(2))


def main():
    dot = Digraph()

    def filter_path(path: PurePosixPath) -> bool:
        return is_launch_file(path) and not starts_with_dot(path)

    for path in walk_launch_files(PurePosixPath('/data'), filter_path):
        try:
            x = parse_path(path)
        except ValueError:
            continue
        dot.node(str(x))
        with open(path.as_posix()) as file:
            text = file.read()
        for y in get_includes(text):
            dot.edge(str(x), str(y))

    dot.render('/data/launch-files.gv')


if __name__ == '__main__':
    main()
