import argparse
import shlex

parser = argparse.ArgumentParser(exit_on_error=False)

shell_parsers = parser.add_subparsers(dest="command", required=True)

quit_parser = shell_parsers.add_parser("quit")

insert_node_parser = shell_parsers.add_parser("insert-node")
insert_node_parser.add_argument("type", default="article", type=str)
insert_node_parser.add_argument("url", type=str)

create_node_type_parser = shell_parsers.add_parser("create-node-type")
create_node_type_parser.add_argument("name", type=str)

insert_relationship_parser = shell_parsers.add_parser("insert-relationship")
insert_relationship_parser.add_argument("source-node-id", type=int)
insert_relationship_parser.add_argument("type", type=str)
insert_relationship_parser.add_argument("target-node-id", type=int)

create_relationship_type_parser = shell_parsers.add_parser(
    "create-relationship-type"
)
create_relationship_type_parser.add_argument("name", type=str)

delete_parser = shell_parsers.add_parser("delete")
delete_parser.add_argument(
    "entity", choices=["edge", "edge_type", "node", "node_type"], type=str
)
delete_parser.add_argument("id", type=int)

get_all_parser = shell_parsers.add_parser("get-all")
get_all_parser.add_argument(
    "entity", choices=["edge", "edge_type", "node", "node_type"], type=str
)

get_parser = shell_parsers.add_parser("get")
get_parser.add_argument(
    "entity", choices=["edge", "edge_type", "node", "node_type"], type=str
)
get_parser.add_argument("id", type=int)

get_node_asset_folder_parser = shell_parsers.add_parser("get-node-asset-folder")
get_node_asset_folder_parser.add_argument("id", type=int)

open_node_asset_folder_parser = shell_parsers.add_parser(
    "open-node-asset-folder"
)
open_node_asset_folder_parser.add_argument("id", type=int)

upload_node_asset_parser = shell_parsers.add_parser("upload-node-asset")
upload_node_asset_parser.add_argument("id", type=int)
upload_node_asset_parser.add_argument("file", type=int)

match_node_parser = shell_parsers.add_parser("match-node")
match_node_parser.add_argument("match", type=str)

set_node_parser = shell_parsers.add_parser("set-node")
set_node_parser.add_argument("--content", type=str)
set_node_parser.add_argument("--type", type=str)
set_node_parser.add_argument("--url", type=str)
set_node_parser.add_argument("id", type=int)

set_node_content_parser = shell_parsers.add_parser("set-node-content")
set_node_content_parser.add_argument("id", type=int)

update_node_type_parser = shell_parsers.add_parser("update-node-type")
update_node_type_parser.add_argument("--name", type=str)
update_node_type_parser.add_argument("--scheme", type=str)
update_node_type_parser.add_argument("--scheme-font", type=str)
update_node_type_parser.add_argument("name", type=str)

set_node_type_scheme_parser = shell_parsers.add_parser("set-node-type-scheme")
set_node_type_scheme_parser.add_argument("name", type=str)

set_node_type_scheme_font_parser = shell_parsers.add_parser(
    "set-node-type-scheme-font"
)
set_node_type_scheme_font_parser.add_argument("name", type=str)

set_edge_parser = shell_parsers.add_parser("set-edge")
set_edge_parser.add_argument("--type", type=str)
set_edge_parser.add_argument("--source-node-id", type=int)
set_edge_parser.add_argument("--target-node-id", type=int)
set_edge_parser.add_argument("id", type=int)

update_edge_type_parser = shell_parsers.add_parser("update-edge-type")
update_edge_type_parser.add_argument("current-name", type=str)
update_edge_type_parser.add_argument("new-name", type=str)


def execute(command):
    if not command:
        return

    try:
        args = parser.parse_args(shlex.split(command))
    except (argparse.ArgumentError, SystemExit) as exception:
        print(exception)
        return

    match args.command:
        case "insert-node":
            pass
        case "create-node-type":
            pass
        case "insert-relationship":
            pass
        case "create-relationship-type":
            pass
        case "delete":
            pass
        case "get-all":
            pass
        case "get":
            pass
        case "get-node-asset-folder":
            pass
        case "open-node-asset-folder":
            pass
        case "upload-node-asset":
            pass
        case "match-node":
            pass
        case "set-node":
            pass
        case "set-node-content":
            pass
        case "update-node-type":
            pass
        case "set-edge":
            pass
        case "update-edge-type":
            pass


def shell():
    while True:
        command = input("$ ").strip()

        if command in ["quit"]:
            return

        execute(command)


def run(args):
    if args.shell:
        execute(args.shell)
        return

    shell()
