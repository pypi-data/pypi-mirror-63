from pathlib import Path
import typer
from jinja2 import Engironment, PackageLoader

def create_base_folders(
        output_dir: str="output",
        static_dir: str="static",
        content_path: str="content",
        templates_path: str="templates",
        )
    """
    Create Base Folders for your
    output_dir, static_dir, content_path, and templates_path
    """
    Path(output_dir).mkdir(exist_ok=True)
    typer.echo(f'{output_dir=} created')
    Path(content_path).mkdir(exist_ok=True)
    typer.echo(f'{content_path=} created')
    Path(static_dir).mkdir(exist_ok=True)
    typer.echo(f'{static_dir=} created')
    Path(templates_path).mkdir(exist_ok=True)
    typer.echo(f'{templates_path=} created')
    Path(templates_path).joinpath('page.html').touch(exist_ok=True)


def gen_run_template():
    env = Environment(
            loader=PackageLoader('render_engine', 'templates'),
            )
    template = env.get_template('run.txt')
    return template.render()

def _main(
        output_dir: str="output",
        static_dir: str="static",
        content_path: str="content",
        templates_path: str="templates",
        ):
    """
    - Create Folders
    - Test Folders Created
    - Test Folders Do Not Overwrite
    - Test Folders Do Not Error if exists already
    """

    create_base_folders(output_dir, static_dir, content_path, templates_path)
    Path('run.py').write_text(get_run_template)



if __name__ == "__main__":
    _main()
