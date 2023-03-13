# SPDX-FileCopyrightText: 2022 EACG GmbH
#
# SPDX-License-Identifier: Apache-2.0


import click

class Command(click.Command):
    def parse_opts_from_args(self, args: [str]):
        ctx = self.context_class(self)
        with ctx:
            parser = self.make_parser(ctx)
            values, _, order = parser.parse_args(args)

        opts = {k: d for (k, d), ty in zip(values.items(), order) if isinstance(ty, click.Option)}
        return opts