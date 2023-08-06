#!/usr/bin/python
# -*- coding: <utf-8> -*-
import pyodbc
from contextlib import contextmanager
from pprint import pprint
import os
import webbrowser
from jinja2 import Environment,FileSystemLoader
import time


def render(server_name, database_name, filename):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;")
            yield cnxn

        except Exception as e:
            print(e)


    # name of every project
    with connection() as conn:
        curr= conn.cursor()
        get_projects = "SELECT TOP(1000)[project_name] FROM[eltsnap_v2].[elt].[project]"
        curr.execute(get_projects)
        c= curr.fetchall()
        project_set=[proj[0] for proj in c]

    from collections import defaultdict

    project_package_set= defaultdict(list)
    #projects with packages
    with connection() as conn:
        curr=conn.cursor()
        for i in project_set:
            get_project_package = "select p.project_name, pp.sequence_number, pp.package_name from elt.project as p right join [elt].[project_package] as pp on p.project_id=pp.project_id where p.project_name='{0}' order by  pp.sequence_number;".format(i)
            curr.execute(get_project_package)
            c=curr.fetchall()
            project_package_set[i].append(c)
            project_package_columns=[col[0] for col in curr.description][1:]


    with connection() as conn:
        curr=conn.cursor()
        DataFlowPackage_ = "SELECT [src_connection],[src_query],[is_expression],[dst_connection] ,[dst_schema] ,[dst_table] ,[dst_truncate] ,[keep_identity] ,[package_name],[use_bulk_copy], [batch_size]" \
                           "  FROM [eltsnap_v2].[elt].[package_config_data_flow]"
        curr.execute(DataFlowPackage_)
        c=curr.fetchall()
        DF_table=c


    with connection() as conn:
        curr=conn.cursor()
        ForEachDF_ = "SELECT [foreach_connection] ,[foreach_query_expr],[src_connection],[src_query_expr],[dst_connection],[dst_schema],[dst_table],[dst_truncate],[keep_identity],[package_name]" \
                     ",[use_bulk_copy],[batch_size] FROM [eltsnap_v2].[elt].[package_config_foreach_data_flow]"
        curr.execute(ForEachDF_)
        c=curr.fetchall()
        ForEachDF=c


    with connection() as conn:
        curr=conn.cursor()
        ExecSql_= "SELECT [connection_manager],[query] ,[is_expression]   ,[return_row_count] ,[package_name] FROM [elt].[package_config_execute_sql]"
        curr.execute(ExecSql_)
        c=curr.fetchall()
        ExecSql=c

    with connection() as conn:
        curr=conn.cursor()
        ExecProc_= "SELECT [executable_expr],[arguments_expr],[working_directory],[place_values_in_ELT_Data],[package_name] FROM [eltsnap_v2].[elt].[package_config_execute_process]"
        curr.execute(ExecProc_)
        c=curr.fetchall()
        ExecProc=c


    with connection() as conn:
        curr=conn.cursor()
        JSONtt_= "SELECT [src_connection] ,[table_selection_option],[table_list],[flat_file_connection],[dst_connection],[package_name] FROM [eltsnap_v2].[elt].[package_config_json_table_transfer]"
        curr.execute(JSONtt_)
        c=curr.fetchall()
        JSONtt=c


    with connection() as conn:
        curr=conn.cursor()
        SemiS_= "SELECT [src_connection],[dst_connection],[dst_schema],[dst_tables_init_option],[package_name] FROM [eltsnap_v2].[elt].[package_config_semi_struct_load]"
        curr.execute(SemiS_)
        c=curr.fetchall()
        SemiS=c


    with connection() as conn:
        curr=conn.cursor()
        ForEachSQL_= "SELECT [foreach_connection],[foreach_query_expr],[query_connection],[query],[return_row_count],[package_name] FROM [eltsnap_v2].[elt].[package_config_foreach_execute_sql]"
        curr.execute(ForEachSQL_)
        c=curr.fetchall()
        ForEachSQL=c

    # project_enviroments
    enviroment_project = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        enviroment_project_st = "  select p.project_name, e.[environment_name] from [elt].[project] as p inner join [elt].[project_environment] as e on p.project_id=e.project_id;"
        curr.execute(enviroment_project_st)
        c = curr.fetchall()
        for e in c:
            enviroment_project[e[0]].append(e[1])

    # pprint(enviroment_project)
    # exit()
    with connection() as conn:
        curr=conn.cursor()
        connections_query= "SELECT  [connection_name] FROM [eltsnap_v2].[elt].[oledb_connection]"
        curr.execute(connections_query)
        c=curr.fetchall()
        connections=[m[0] for m in c]

    conns_projects= defaultdict(list)
    with connection() as conn:
        curr=conn.cursor()
        get_conections_by_projects= "SELECT *FROM [elt].[show projects using connection] (?)"
        for k in connections:
            curr.execute(get_conections_by_projects,k)
            c=curr.fetchall()
            c1=[p[0] for p in c]
            conns_projects[k].append(c1)

    conns_packages=defaultdict(list)
    with connection() as conn:
        curr=conn.cursor()
        get_conections_by_packages= "SELECT * FROM [elt].[show packages using connection] (?)"
        for k in connections:
            curr.execute(get_conections_by_packages,k)
            c=curr.fetchall()
            c1=[p[0] for p in c]
            conns_packages[k].append(c1)


    # for k,v in conns_projects.items():
    #     for i in v:
    #         for m in i:
    #             pprint(m)

    # pprint(conns_packages)
    # exit()

    import datetime
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'html')

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('HTML_template.html')

    with open(filename, 'w') as writer:
        writer.write(template.render(
            h1="Sample Projects Review",
            published = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
            project_name="Project Name",
            project_set=project_set,
            project_package_set=project_package_set,
            project_package_columns=project_package_columns,
            DF_table=DF_table,
            ExecSql=ExecSql,
            ForEachDF=ForEachDF,
            ExecProc=ExecProc,
            ForEachSQL=ForEachSQL,
            connections=connections,
            conns_projects=conns_projects,
            conns_packages=conns_packages,
            enviroment_project=enviroment_project,
            JSONtt=JSONtt,
            SemiS=SemiS
                ))

