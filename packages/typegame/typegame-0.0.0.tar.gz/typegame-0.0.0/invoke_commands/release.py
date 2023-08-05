from invoke import task
import io
import os

from .vars import mymodule


@task
def new(c):

    version = mymodule.__version__

    pypirc_str = "\n".join([
        "[pypi]"
        "  username = __token__"
        f"  password = {os.environ['TWINE_PASSWORD']}"
    ])

    pypirc_path = os.path.join(os.path.expanduser('~'), ".pypirc")

    if not os.path.exists(pypirc_path):
        with open(pypirc_path, "w") as fp:
            fp.write(pypirc_str)

    c.run("python setup.py sdist")
    c.run("twine check dist/*")
    # c.run(f"twine upload dist/*{version}.tar.gz --non-interactive --config-file {pypirc_path}")
    c.run(f"twine upload dist/*{version}.tar.gz -u __token__ -p $TWINE_PASSWORD")


@task
def tag(c):

    version = mymodule.__version__

    f = io.StringIO()
    c.run("git rev-parse --abbrev-ref HEAD", out_stream=f)
    branch = f.getvalue().strip()
    f.close()

    if branch == "master":
        tag_version = "v{}".format(version)
        f2 = io.StringIO()
        c.run("git tag", out_stream=f2)
        tags = f2.getvalue().split()
        print(tags)
        if tag_version not in tags:
            current_release_path = "docs_config/current_release.rst"
            with open(current_release_path) as fp:
                notes = fp.read()
            with open(
                "docs_config/release_notes/{}.rst".format(tag_version), "w"
            ) as fp:
                fp.write(notes)
            c.run(f"git tag -a {tag_version} -m '{notes}'")
            with open(current_release_path, "w") as fp:
                fp.write("")
            c.run("git push --tags")
        else:
            print("{} version already tagged".format(tag_version))
    else:
        print("only master branch can be tagged")
