#!/usr/bin/env python

import sys

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import argparse
from sfdc_cli.version import __version__, __desc__
print('here')
print('sfdc_cli.commands')

# from sfdc_cli.commands.ant_migration_tool import register
from sfdc_cli.commands import register
from sfdc_cli.commands import (
    register,
    ant_migration_tool,
    apex_execute,
    apex_test_coverage,
    apex_test_run,
    call_rest_api,
    coder_apex_page_generator,
    coder_apex_snippet_insert_data_from_soql,
    coder_apex_snippet_insert_ramdam_data,
    coder_apex_testclass_generator,
    coder_copy_aura,
    coder_permission_build,
    coder_permission_list,
    coder_snippet_soql,
    data_soql_query,
    data_tooling_query,
    download_attachment,
    folder_list,
    meta_attr,
    meta_cache,
    meta_delete,
    meta_new,
    meta_refresh,
    meta_refresh_aura,
    meta_refresh_dir,
    meta_retrieve,
    meta_template_apex,
    meta_template_component,
    meta_template_page,
    meta_template_trigger,
    meta_update,
    packagexml_local,
    packagexml_server,
    project_init,
    sobject_data_create,
    sobject_data_delete,
    sobject_data_get,
    sobject_data_update,
    sobject_export_xlsx,
    sobject_fields_desc,
    sobject_list,
    tools_json_format
)

def main():
    parser = argparse.ArgumentParser(description='%s v%s' %
                                     (__desc__, __version__))
    subparsers = parser.add_subparsers()
    register(parser, subparsers)

    # help
    def command_help(args):
        print(parser.parse_args([args.command, '--help']))

    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
