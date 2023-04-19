### What is your favourite package manager and why?
Currently, I use to use poetry because I had many problems with pipenv in the past (it usually took long time to resolve dependencies). But some months ago, I tried again pipenv for a side project and it had a new version that goes really well.

So I don't have a favourite package manager, I like these two.

### What architecture did you follow for this project?
I have use DDD as you suggested during the first interview. I also added a UoW (Unit of Work) layer.

I tried to follow the next diagram described in [Architecture Patterns with Python](https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/) book

![DDD](https://www.cosmicpython.com/book/images/apwp_p101.png)

### Do you know and understand UML? What would the class diagram of the domain exposed in the mastermind game be like for you?
Yes, I know UML. The domain's diagram of this project is:

![UML](https://i.imgur.com/RPBxjBf.png)

### What tools are you aware of to handle things like code styling and consistency, formatting, typing…?
For example, for this project, I configure a pre-commit file with the following steps:

- [mypy](https://mypy.readthedocs.io/en/stable/): type checker to ensure that you’re using variables and functions in your code correctly.
- trailing-whitespace: to trims trailing whitespaces
- [black](https://pypi.org/project/black/): code formatter
- [flake8](https://flake8.pycqa.org/en/latest/): linter

Also, in the GitHub action, I run [bandit](https://pypi.org/project/bandit/) for security checks. Dependabot is also configured ([safety](https://pyup.io/safety/) can be used as an alternative to dependabot)

### Is there anything you would like to comment about the project, this small exercise, etc?
I tried to respect DDD pattern as much as I can, this is my first time implementing a project with this architecture, so maybe there are some mistakes :')

The project could be improved using async calls, but I had prefer to take care about the architecture. Also, API is not secured by any mechanism to make easier to test, but there is an implementation of a method to secure endpoints by an APIKEY, you just need to inject the dependency of *api_key_validator* to the endpoint (you can see an example in test_dependencies.py file)

I tried to have a good code coverage with the tests (around 96%), using factories ([factory-boy](https://factoryboy.readthedocs.io/en/stable/index.html)) to create automatically objects in the database, [faker](https://faker.readthedocs.io/en/master/index.html) to give some randomness to data and pytest fixtures to avoid to repeat code during tests.

This project has been created using a cookiecutter that I had participated developing it in Aplazame.

Project is production-ready, having integrated sentry with just configuring the credentials in settings file. Also, [prometheus](https://prometheus.io/) is configured exposing an endpoint in order to retrieve platform metrics.
