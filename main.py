"""
The entry point of the program.
"""
import argparse

import commands.build
import commands.chat
import commands.query
import commands.search
import commands.summarize

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

build_command = subparsers.add_parser("build")
build_command.add_argument("folder_path", type=str)
build_command.set_defaults(func=commands.build.run)

search_command = subparsers.add_parser("search")
search_command.add_argument("keyword", type=str)
search_command.set_defaults(func=commands.search.run)

summarize_command = subparsers.add_parser("summarize")
summarize_command.add_argument("file_path", type=str)
summarize_command.set_defaults(func=commands.summarize.run)

query_command = subparsers.add_parser("query")
query_command.add_argument("query", type=str)
query_command.set_defaults(func=commands.query.run)

chat_command = subparsers.add_parser("chat")
chat_command.set_defaults(func=commands.chat.run)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
