from pathlib import Path
import argparse


from textual.app import App, ComposeResult
from textual.widgets import Tree


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    return parser


class TreeApp(App):
    StartDir: Path | None = None

    def compose(self) -> ComposeResult:
        nodes = dict()
        tree = None
        current_node = None

        if self.StartDir is None:
            raise Exception("StartDir has not been set")

        for dirpath, dirs, files in Path.walk(Path(self.StartDir)):
            if not nodes.get(dirpath.absolute()):
                if not tree:
                    tree = Tree(dirpath.name)
                    tree.root.expand()
                    current_node = tree.root
                    nodes[dirpath.absolute] = current_node
                else:
                    raise Exception(
                        f"All node should exist in the dict... {dirpath.absolute} -- {nodes}"
                    )
            else:
                current_node = nodes.get(dirpath.absolute())

            if current_node is None:
                raise Exception("current_node should be set...")

            for file_ in files:
                current_node.add_leaf(file_)

            for dir in dirs:
                new_node = current_node.add(dir, expand=True)
                nodes[dirpath.joinpath(dir).absolute()] = new_node

        yield tree


def main():
    parser = parse_args()
    args = parser.parse_args()

    path = Path(args.path)

    app = TreeApp()
    app.StartDir = path
    app.run()


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()

    path = Path(args.path)

    app = TreeApp()
    app.StartDir = path
    app.run()
