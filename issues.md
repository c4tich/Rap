# Issues

1. No requirements and no package structure
- No requirements implies that the users don't know which libraries they have to install, so they have to run, see the ModuleError and install until all dependencies are installed
- No package structure means that you can't install the software as a package and versioning is very difficult

Solution: Used [`poetry`](https://python-poetry.org/docs/basic-usage/#initialising-a-pre-existing-project) which is a packaging and dependency management tool. With `poetry` we can pin down the dependencies so everyone can use the same version of the dependencies and generates a package that can be installed

2. Naming conventions
- The files in the project do not follow naming conventions in python

Solution: Refactor affected files

3. Documentation
- The project lacks documentation, and the only example is unclear to a new user. New users don't know what artists or styles can be chosen

Solution: Document the code and the options

4. Command line interface
- Using input arguments to the script is prone to errors. Furthermore, arguments can't be named so it's unclear what means a passed argument

Solution: Used [`click`](https://click.palletsprojects.com/en/8.1.x/) to define a command line interface to interact with the code. Provides helpful insights so users have more information when running the program 

5. Hardcoded and absolute paths:
- The software uses hardcoded and absolute paths which stop working as soon as the code is run outside of the developer's machine. Better to define paths relative to the project so that they work everywhere) 
