> [!IMPORTANT]
> This template is **archived**.  
> UV can now [generate a sample project](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)  
> I recommend using **UV** to bootstrap your peojects.  
> [Copier](https://github.com/copier-org/copier) is a tools that can bootstrap projects from templates.  


# Flask Project Template

A full feature Flask project template.

See also 
- [Python-Project-Template](https://github.com/rochacbruno/python-project-template/) for a lean, low dependency Python app.
- [FastAPI-Project-Template](https://github.com/rochacbruno/fastapi-project-template/) The base to start an openapi project featuring: SQLModel, Typer, FastAPI, JWT Token Auth, Interactive Shell, Management Commands.

### HOW TO USE THIS TEMPLATE

> **DO NOT FORK** this is meant to be used from **[Use this template](https://github.com/rochacbruno/flask-project-template/generate)** feature.

1. Click on **[Use this template](https://github.com/rochacbruno/flask-project-template/generate)**
3. Give a name to your project  
   (e.g. `my_awesome_project` recommendation is to use all lowercase and underscores separation for repo names.)
3. Wait until the first run of CI finishes  
   (Github Actions will process the template and commit to your new repo)
4. If you want [codecov](https://about.codecov.io/sign-up/) Reports and Automatic Release to [PyPI](https://pypi.org)  
  On the new repository `settings->secrets` add your `PIPY_API_TOKEN` and `CODECOV_TOKEN` (get the tokens on respective websites)
4. Read the file [CONTRIBUTING.md](CONTRIBUTING.md)
5. Then clone your new project and happy coding!

> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.

### What is included on this template?

- 🍾 A full feature Flask application with CLI, API, Admin interface, web UI and modular configuration.
- 📦 A basic [setup.py](setup.py) file to provide installation, packaging and distribution for your project.  
  Template uses setuptools because it's the de-facto standard for Python packages, you can run `make switch-to-poetry` later if you want.
- 🤖 A [Makefile](Makefile) with the most useful commands to install, test, lint, format and release your project.
- 📃 Documentation structure using [mkdocs](http://www.mkdocs.org)
- 💬 Auto generation of change log using **gitchangelog** to keep a HISTORY.md file automatically based on your commit history on every release.
- 🐋 A simple [Containerfile](Containerfile) to build a container image for your project.  
  `Containerfile` is a more open standard for building container images than Dockerfile, you can use buildah or docker with this file.
- 🧪 Testing structure using [pytest](https://docs.pytest.org/en/latest/)
- ✅ Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- 📊 Code coverage reports using [codecov](https://about.codecov.io/sign-up/)
- 🛳️ Automatic release to [PyPI](https://pypi.org) using [twine](https://twine.readthedocs.io/en/latest/) and github actions.
- 🎯 Entry points to execute your program using `python -m <ticketselling>` or `$ ticketselling` with basic CLI argument parsing.
- 🔄 Continuous integration using [Github Actions](.github/workflows/) with jobs to lint, test and release your project on Linux, Mac and Windows environments.

> Curious about architectural decisions on this template? read [ABOUT_THIS_TEMPLATE.md](ABOUT_THIS_TEMPLATE.md)  
> If you want to contribute to this template please open an [issue](https://github.com/rochacbruno/flask-project-template/issues) or fork and send a PULL REQUEST.

<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->

---
# ticketselling Flask Application

Awesome ticketselling created by cdat13

## Installation

From source:

```bash
git clone https://github.com/cdat13/TicketSelling ticketselling
cd ticketselling
make install
```

From pypi:

```bash
pip install ticketselling
```

## Executing

This application has a CLI interface that extends the Flask CLI.

Just run:

```bash
$ ticketselling
```

or

```bash
$ python -m ticketselling
```

To see the help message and usage instructions.

## First run

```bash
ticketselling create-db   # run once
ticketselling populate-db  # run once (optional)
ticketselling add-user -u admin -p 1234  # ads a user
ticketselling run
```

Go to:

- Website: http://localhost:5000
- Admin: http://localhost:5000/admin/
  - user: admin, senha: 1234
- API GET:
  - http://localhost:5000/api/v1/product/
  - http://localhost:5000/api/v1/product/1
  - http://localhost:5000/api/v1/product/2
  - http://localhost:5000/api/v1/product/3


> **Note**: You can also use `flask run` to run the application.
