import sys

import click

from rap.entrypoints import (
    generate,
    read,
    project_visualization,
    write,
)


@click.group()
def main() -> None:
    """
    RAP

    Song generation and visualization

    """
    pass


main.add_command(generate, "generate")
main.add_command(read, "read"),
main.add_command(project_visualization, "project-visualization"),
main.add_command(write, "write")

if __name__ == "__main__":
    sys.exit(main())
