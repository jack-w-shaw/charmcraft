# Copyright 2020 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

"""Provide all help texts."""

import textwrap
from operator import attrgetter

# max columns used in the terminal
TERMINAL_WIDTH = 72

# the summary of the whole program, already indented so it represents the real
# "columns spread", for easier human editing.
SUMMARY = """
    Charmcraft provides a streamlined, powerful, opinionated and
    flexible tool to develop, package and manage the lifecycle of
    Juju charm publication, focused particularly on charms written
    within the Operator Framework.
"""
# XXX Facundo 2020-07-13: we should add an extra (separated) line to the summary with:
#   See <url> for additional documentation.

# generic intro and outro texts
HEADER = """
Usage:
    charmcraft [help] <command>
"""

USAGE = """\
Usage: charmcraft [OPTIONS] COMMAND [ARGS]...
Try '{fullcommand} -h' for help.

Error: {error_message}
"""


def get_error_message(fullcommand, error_message):
    """Build a usage and error message."""
    return USAGE.format(fullcommand=fullcommand, error_message=error_message)


def _build_item(title, text, title_space):
    """Show an item in the help, generically a title and a text aligned.

    The title starts in column 4 with an extra ':'. The text starts in
    4 plus the title space; if too wide it's wrapped.
    """
    text_space = TERMINAL_WIDTH - title_space - 4
    wrapped_lines = textwrap.wrap(text, text_space)

    # first line goes with the title at column 4
    title += ':'
    result = ["    {:<{title_space}s}{}".format(title, wrapped_lines[0], title_space=title_space)]

    # the rest (if any) still aligned but without title
    for line in wrapped_lines[1:]:
        result.append(" " * (title_space + 4) + line)

    return result


def get_full_help(command_groups, global_options):
    """Produce the text for the default help.

    The default help has the following structure:

    - usage
    - summary (link to docs)
    - common commands listed and described shortly
    - all commands grouped, just listed
    - more help
    """
    textblocks = []

    # title
    textblocks.append(HEADER)

    # summary
    textblocks.append("Summary:" + SUMMARY)

    # column alignment is dictated by longest common commands names and groups names
    max_title_len = 0

    # collect common commands
    common_commands = []
    for group, _, commands in command_groups:
        max_title_len = max(len(group), max_title_len)
        for cmd in commands:
            if cmd.common:
                common_commands.append(cmd)
                max_title_len = max(len(cmd.name), max_title_len)

    for title, _ in global_options:
        max_title_len = max(len(title), max_title_len)

    # leave two spaces after longest title (also considering the ':')
    max_title_len += 3

    global_lines = ["Global options:"]
    for title, text in global_options:
        global_lines.extend(_build_item(title, text, max_title_len))
    textblocks.append("\n".join(global_lines))

    common_lines = ["Starter commands:"]
    for cmd in sorted(common_commands, key=attrgetter('name')):
        common_lines.extend(_build_item(cmd.name, cmd.help_msg, max_title_len))
    textblocks.append("\n".join(common_lines))

    grouped_lines = ["Commands can be classified as follows:"]
    for group, _, commands in sorted(command_groups):
        command_names = ", ".join(sorted(cmd.name for cmd in commands))
        grouped_lines.extend(_build_item(group, command_names, max_title_len))
    textblocks.append("\n".join(grouped_lines))

    textblocks.append(textwrap.dedent("""
        For more information about a command, run 'charmcraft help <command>'.
        For a summary of all commands, run 'charmcraft help --all'.
    """))

    # join all stripped blocks, leaving ONE empty blank line between
    text = '\n\n'.join(block.strip() for block in textblocks) + '\n'
    return text


def get_detailed_help(command_groups, global_options):
    """Produce the text for the detailed help.

    It has the following structure:

    - usage
    - summary (link to docs)
    - global options
    - all commands shown with description, grouped
    - more help
    """
    textblocks = []

    # title
    textblocks.append(HEADER)

    # summary
    textblocks.append("Summary:" + SUMMARY)

    # column alignment is dictated by longest common commands names and groups names
    max_title_len = 0
    for _, _, commands in command_groups:
        for cmd in commands:
            max_title_len = max(len(cmd.name), max_title_len)
    for title, _ in global_options:
        max_title_len = max(len(title), max_title_len)

    # leave two spaces after longest title (also considering the ':')
    max_title_len += 3

    global_lines = ["Global options:"]
    for title, text in global_options:
        global_lines.extend(_build_item(title, text, max_title_len))
    textblocks.append("\n".join(global_lines))

    textblocks.append("Commands can be classified as follows:")

    for _, group_description, commands in command_groups:
        group_lines = ["{}:".format(group_description)]
        for cmd in commands:
            group_lines.extend(_build_item(cmd.name, cmd.help_msg, max_title_len))
        textblocks.append("\n".join(group_lines))

    textblocks.append(textwrap.dedent("""
        For more information about a specific command, run 'charmcraft help <command>'.
    """))

    # join all stripped blocks, leaving ONE empty blank line between
    text = '\n\n'.join(block.strip() for block in textblocks) + '\n'
    return text


def get_command_help(command_groups, command, arguments):
    """Produce the text for each command's help.

    It has the following structure:

    - usage
    - summary
    - options
    - other related commands
    - footer
    """
    textblocks = []

    # separaate all arguments into the parameters and optional ones, just checking
    # if first char is a dash
    parameters = []
    options = []
    for name, title in arguments:
        if name[0] == '-':
            options.append((name, title))
        else:
            parameters.append(name)

    textblocks.append(textwrap.dedent("""\
        Usage:
            charmcraft {} [options] {}
    """.format(command.name, " ".join(parameters))))

    textblocks.append("Summary:{}".format(textwrap.indent(command.overview, '    ')))

    # column alignment is dictated by longest options title (plus ':' and two intercolumn spaces)
    max_title_len = max(len(title) for title, text in options) + 3

    # command options
    option_lines = ["Options:"]
    for title, text in options:
        option_lines.extend(_build_item(title, text, max_title_len))
    textblocks.append("\n".join(option_lines))

    # recommend other commands of the same group
    for group_name, _, command_classes in command_groups:
        if group_name == command.group:
            break
    else:
        raise RuntimeError("Internal inconsistency in commands groups")
    other_command_names = [c.name for c in command_classes if not isinstance(command, c)]
    if other_command_names:
        see_also_block = ["See also:"]
        see_also_block.extend(("    " + name) for name in sorted(other_command_names))
        textblocks.append('\n'.join(see_also_block))

    # footer
    textblocks.append("""
        For a summary of all commands, run 'charmcraft help --all'.
    """)

    # join all stripped blocks, leaving ONE empty blank line between
    text = '\n\n'.join(block.strip() for block in textblocks) + '\n'
    return text
