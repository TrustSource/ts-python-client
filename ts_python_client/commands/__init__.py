# SPDX-FileCopyrightText: 2022 EACG GmbH
#
# SPDX-License-Identifier: Apache-2.0


import click


def parse_cmd_opts_from_args(cmd: click.Command, args: [str]):
    ctx = cmd.context_class(cmd)
    with ctx:
        parser = cmd.make_parser(ctx)
        values, _, order = parser.parse_args(args)

    opts = {k: d for (k, d), ty in zip(values.items(), order) if isinstance(ty, click.Option)}
    return opts

