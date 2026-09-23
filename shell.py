import argparse
import shlex

from .file import File

current_file = File()
parser = argparse.ArgumentParser(exit_on_error=False)

shell_parsers = parser.add_subparsers(dest="command", required=True)

quit_parser = shell_parsers.add_parser("quit")

open_parser = shell_parsers.add_parser("open")
open_parser.add_argument("-f, --force", action="store_true")
open_parser.add_argument("path", type=str)

commit_parser = shell_parsers.add_parser("commit")
commit_parser.add_argument("path", default=None, type=str)

insert_node_parser = shell_parsers.add_parser("insert-node")
insert_node_parser.add_argument("type", default="article", type=str)
insert_node_parser.add_argument("url", type=str)

create_node_type_parser = shell_parsers.add_parser("create-node-type")
create_node_type_parser.add_argument("name", type=str)

insert_edge_parser = shell_parsers.add_parser("insert-edge")
insert_edge_parser.add_argument(
    "source-node-id", dest="source_node_id", type=int
)
insert_edge_parser.add_argument("type", type=str)
insert_edge_parser.add_argument(
    "target-node-id", dest="target_node_id", type=int
)

create_edge_type_parser = shell_parsers.add_parser("create-relationship-type")
create_edge_type_parser.add_argument("name", type=str)

delete_parser = shell_parsers.add_parser("delete")
delete_parser.add_argument(
    "entity", choices=["edge", "edge_type", "node", "node_type"], type=str
)
delete_parser.add_argument("id", type=str)

get_all_parser = shell_parsers.add_parser("get-all")
get_all_parser.add_argument(
    "entity", choices=["edge", "edge_type", "node", "node_type"], type=str
)
get_all_parser.add_argument("type", type=str)


get_parser = shell_parsers.add_parser("get")
get_parser.add_argument(
    "entity", choices=["edge", "edge_type", "node", "node_type"], type=str
)
get_parser.add_argument("id", type=str)

get_node_asset_directory_parser = shell_parsers.add_parser(
    "get-node-asset-directory"
)
get_node_asset_directory_parser.add_argument("id", type=int)

open_node_asset_directory_parser = shell_parsers.add_parser(
    "open-node-asset-directory"
)
open_node_asset_directory_parser.add_argument("id", type=int)

upload_node_asset_parser = shell_parsers.add_parser("upload-node-asset")
upload_node_asset_parser.add_argument("id", type=int)
upload_node_asset_parser.add_argument("asset", type=int)

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
update_node_type_parser.add_argument(
    "--scheme-font", dest="scheme_font", type=str
)
update_node_type_parser.add_argument(
    "current-name", dest="current_name", type=str
)

set_node_type_scheme_parser = shell_parsers.add_parser("set-node-type-scheme")
set_node_type_scheme_parser.add_argument("name", type=str)

set_node_type_scheme_font_parser = shell_parsers.add_parser(
    "set-node-type-scheme-font"
)
set_node_type_scheme_font_parser.add_argument("name", type=str)

set_edge_parser = shell_parsers.add_parser("set-edge")
set_edge_parser.add_argument("--type", type=str)
set_edge_parser.add_argument(
    "--source-node-id", dest="source_node_id", type=int
)
set_edge_parser.add_argument(
    "--target-node-id", dest="target_node_id", type=int
)
set_edge_parser.add_argument("id", type=int)

update_edge_type_parser = shell_parsers.add_parser("update-edge-type")
update_edge_type_parser.add_argument(
    "current-name", dest="current_name", type=str
)
update_edge_type_parser.add_argument("new-name", dest="new_name", type=str)


def execute(command):
    if not command:
        return

    try:
        args_list = shlex.split(command)
    except ValueError as exception:
        print(exception)
        return

    try:
        args = parser.parse_args(args_list)
    except (argparse.ArgumentError, SystemExit):
        return

    match args.command:
        case "open":
            current_file.open(args.path, args.force)
        case "commit":
            current_file.commit(args.path)
        case "insert-node":
            current_file.insert_node(args.url, args.type)
        case "create-node-type":
            current_file.create_node_type(args.name)
        case "insert-edge":
            current_file.insert_edge(
                args.source_node_id, args.type, args.target_node_id
            )
        case "create-edge-type":
            current_file.create_edge_type(args.name)
        case "delete":
            match args.entity:
                case "edge":
                    current_file.delete_edge_by_id(args.id)
                case "edge_type":
                    current_file.delete_edge_type_by_name(args.id)
                case "node":
                    current_file.delete_node_by_id(args.id)
                case "node_type":
                    current_file.delete_node_type_by_name(args.id)
        case "get-all":
            match args.entity:
                case "edge":
                    current_file.get_all_edges(args.type)
                case "edge_type":
                    current_file.get_all_edge_types()
                case "node":
                    current_file.get_all_nodes(args.type)
                case "node_type":
                    current_file.get_all_node_types()
        case "get":
            match args.entity:
                case "edge":
                    current_file.get_edge_by_id(args.id)
                case "edge_type":
                    current_file.get_edge_type_by_name(args.id)
                case "node":
                    current_file.get_node_by_id(args.id)
                case "node_type":
                    current_file.get_node_type_by_name(args.id)
        case "get-node-asset-directory":
            current_file.get_node_asset_directory(args.id)
        case "open-node-asset-directory":
            current_file.open_node_asset_directory(args.id)
        case "upload-node-asset":
            current_file.upload_node_asset(args.id, args.asset)
        case "match-node":
            current_file.match_nodes_by_url(args.url)
        case "set-node":
            current_file.set_node_by_id(
                args.id, args.url, args.type, args.content
            )
        case "set-node-content":
            # Should open default editor (vi, notepad.exe, etc.) and then
            # change content with current_file.set_node_by_id(content=content)
            pass
        case "update-node-type":
            current_file.update_node_type(
                args.current_name, args.name, args.scheme, args.scheme_font
            )
        case "set-node-type-scheme":
            # Should open default editor (vi, notepad.exe, etc.) and then
            # change scheme with current_file.update_node_type(scheme=scheme)
            pass
        case "set-node-type-scheme-font":
            # Should open default editor (vi, notepad.exe, etc.) and then
            # change scheme with current_file.update_node_type(scheme_font=scheme_font)
            pass
        case "set-edge":
            current_file.set_edge_by_id(
                args.id, args.source_node_id, args.type, args.target_node_id
            )
        case "update-edge-type":
            current_file.update_edge_type(args.current_name, args.name)


def shell():
    while True:
        try:
            command = input("$ ").strip()

            if command in ["quit"]:
                break

            execute(command)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
