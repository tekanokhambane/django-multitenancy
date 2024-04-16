#!/usr/bin/env python
import fileinput
import fnmatch
import os
import re
import sys
from argparse import ArgumentParser
from difflib import unified_diff
from django.core.management.templates import TemplateCommand
from django.core.management.utils import get_random_secret_key
from django.core.management import ManagementUtility

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        "This version of dajgno-Multitenacy requires Python {}.{} or above - you are running {}.{}\n".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)


def pluralize(value, arg="s"):
    return "" if value == 1 else arg




class CreateProject(TemplateCommand):
    description = "Creates the directory structure for a new Multitenancy project."
    

    def add_arguments(self, parser):
        parser.add_argument("project_name", help="Name for your Multitenancy project")
        parser.add_argument(
            '--sitename',
            help='Human readable name of your organisation or brand, e.g. "Mega Corp Inc."'
        )
        parser.add_argument(
            '--domain',
            help='Domain that will be used for your website in production, e.g. "www.example.com"'
        )
        parser.add_argument(
            '--database',
            help='The database name you will be using to connect your project.'
        )
        parser.add_argument(
            '--password',
            help='The password for your database'
        )
        parser.add_argument(
            '--port',
            help='The port for your database'
        )
        super().add_arguments(parser)

    def handle(self, **options):
        # pop standard args
        project_name = options.pop("name")
        target = options.pop("directory")


        # Make sure given name is not already in use by another python package/module.
        try:
            __import__(project_name)
        except ImportError:
            pass
        else:
            sys.exit(
                "'%s' conflicts with the name of an existing "
                "Python module and cannot be used as a project "
                "name. Please try another name." % project_name
            )

        # Create a random SECRET_KEY to put it in the main settings.
        options["secret_key"] = get_random_secret_key()

        # Handle custom template logic
        import multitenancy

        tenants_path = os.path.dirname(multitenancy.__file__)
        template_path = os.path.join(
            os.path.join(tenants_path, "project_template")
        )

        # Check if provided template is built-in to coderedcms,
        # otherwise, do not change it.
        options['template'] = template_path

        # Treat these files as Django templates to render the boilerplate.
        options["extensions"] = ["py", "md", "txt"]
        options["files"] = ["Dockerfile"]

        # Set options
        message = "Creating a Multitenant project called %(project_name)s"

        if options.get("sitename"):
            message += " for %(sitename)s"
        else:
            options["sitename"] = project_name

        if options.get("domain"):
            message += " (%(domain)s)"
            # Strip protocol out of domain if it is present.
            options["domain"] = options["domain"].split("://")[-1]
            # Figure out www logic.
            if options["domain"].startswith("www."):
                options["domain_nowww"] = options["domain"].split("www.")[-1]
            else:
                options["domain_nowww"] = options["domain"]
        else:
            options["domain"] = "localhost"
            options["domain_nowww"] = options["domain"]
        
        if  options.get("database"):
            message += " (%(database)s)"
        else:
            options["database"] = project_name

        if  options.get("password"):
            message += " (%(password)s)"
        else:
            options["password"] = "database password"

        if  options.get("port"):
            message += " (%(port)s)"
        else:
            options["port"] = "5432"

        
        # Print a friendly message
        print(
            message
            % {
                "project_name": project_name,
                "sitename": options.get("sitename"),
                "domain": options.get("domain"),
                "database":options.get("database"),
                "password":options.get("password"),
                "port":options.get("port"),
            }
        )

        # Run command
        super().handle("project", project_name, target, **options)

        # Be a friend once again.
        print(
            "Success! %(project_name)s has been created"
            % {"project_name": project_name}
        )

        nextsteps = """
Next steps:
    1. cd %(directory)s/
    2. python manage.py migrate_schemas
    3. python manage.py shell
    4. >> from multitenancy.utils import create_public_tenant
    5. public_tenant = create_public_tenant("localhost", "adminemail@example.com", "admin password")
    6. python manage.py runserver
    7. Go to http://localhost:8000/admin/ and start editing!
"""
        print(nextsteps % {"directory": target if target else project_name})


    
COMMANDS = {
    "start": CreateProject(),
}


def prog_name():
    return os.path.basename(sys.argv[0])


def help_index():
    print(
        "Type '%s help <subcommand>' for help on a specific subcommand.\n"
        % prog_name()
    )
    print("Available subcommands:\n")
    for name, cmd in sorted(COMMANDS.items()):
        print("    %s%s" % (name.ljust(20), cmd.help))


def unknown_command(command):
    print("Unknown command: '%s'" % command)
    print("Type '%s help' for usage." % prog_name())
    sys.exit(1)


def main():
    try:
        command_name = sys.argv[1]
    except IndexError:
        help_index()
        return

    if command_name == "help":
        try:
            help_command_name = sys.argv[2]
        except IndexError:
            help_index()
            return

        try:
            command = COMMANDS[help_command_name]
        except KeyError:
            unknown_command(help_command_name)
            return

        command.print_help(prog_name(), help_command_name)
        return

    try:
        command = COMMANDS[command_name]
    except KeyError:
        unknown_command(command_name)
        return

    command.run_from_argv(sys.argv)


if __name__ == "__main__":
    main()