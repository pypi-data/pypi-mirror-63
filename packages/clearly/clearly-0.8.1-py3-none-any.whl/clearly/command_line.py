import logging

import click

logger = logging.getLogger(__name__)


class AliasedGroup(click.Group):
    """Used to allow calling shorten commands, as long as they're unique.
     Based on recipe from http://click.palletsprojects.com/en/7.x/advanced/

    """

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) > 1:
            ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))
        return click.Group.get_command(self, ctx, matches[0])


@click.group(cls=AliasedGroup)
@click.version_option()
def clearly():
    """Clearly command line tools."""
    pass


@clearly.command()
@click.argument('broker')
@click.option('--backend', '-b',
              help='Fetches task results from the result backend, like "redis://localhost"')
@click.option('--port', '-p', type=int, help='Listen port for Clearly Server')
@click.option('--max_tasks', '-t', type=int, help='Maximum number of tasks in memory')
@click.option('--max_workers', '-w', type=int, help='Maximum number of workers in memory')
@click.option('--debug', help='Enables debug logging', is_flag=True)
def server(**kwargs):
    """Starts the Clearly Server.

        BROKER: The broker being used by celery, like "amqp://localhost".
    """
    from clearly.server import start_server
    start_server(**{k: v for k, v in kwargs.items() if v},
                 blocking=True)


@clearly.command()
@click.argument('host', type=str, required=False)
@click.argument('port', type=int, required=False)
def client(**kwargs):
    """Starts a REPL shell, with a configured Clearly Client.

    It can be found under the name `clearlycli`.

        HOST: The host Clearly Server is running
        PORT: The port Clearly Server is running
    """
    from clearly.client import ClearlyClient
    clearlycli = ClearlyClient(**{k: v for k, v in kwargs.items() if v})

    # the first option was bpython, but unfortunately it is broken...
    # https://github.com/bpython/bpython/issues/758
    # from bpython import embed
    # embed(dict(clearlycli=clearlycli))

    from IPython import embed
    embed(using='', header='The clearly client is ready to use in `clearlycli`.')
