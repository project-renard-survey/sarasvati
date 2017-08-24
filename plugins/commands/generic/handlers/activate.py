from sarasvati.commands import CommandResult, ActivateCommand
from sarasvati.exceptions import CommandException


def activate(api, args):
    title = args.arg or args.title

    if not title:
        raise CommandException("No title specified")

    thought = api.utilities.find_one_by_title(title)
    api.brain.commands.execute(ActivateCommand(thought))

    return CommandResult(thought, message="Thought '{}' activated".format(thought.title))
