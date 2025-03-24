import click


@click.command()
@click.option('--name', default='World', help='The person to greet.')
@click.option('--times', default=1, help='Number of times to greet.')
def greet(name, times):
    """
    A simple program that greets a person by name.
    """
    for x in range(times):
        click.echo(f"Hello, {name}!")


if __name__ == '__main__':
    greet()

"""
Click is a Python package for creating command-line interfaces. It uses decorators to
define commands, options, and arguments.

** Methods
click.command(): Decorator to turn a function into a command.
click.option(): Decorator to add options (flags or parameters with values) to a command.
click.argument(): Decorator to add arguments (positional parameters) to a command.
click.echo(): Function to print output to the console.
click.group(): Decorator to create a group of commands.
Context.invoke(): Method to invoke another command within a command.
Context.forward(): Method to forward the current context to another command.

** Attributes
allow_extra_args: Attribute to allow extra arguments not defined in the command.
context_settings: Attribute to configure the context of the command.
params: Attribute containing the parameters (options and arguments) of the command.
name: Attribute representing the name of the command.
help: Attribute containing the help text for the command.
callback: Attribute referencing the function to be called when the command is executed.
"""

"""
"if __name__ == '__main__':" in Python to ensure that the code within that block
only runs when the script is executed directly (as a main program)
"""
