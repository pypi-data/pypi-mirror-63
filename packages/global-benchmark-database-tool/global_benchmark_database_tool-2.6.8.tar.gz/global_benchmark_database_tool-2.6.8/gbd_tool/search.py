# Global Benchmark Database (GBD)
# Copyright (C) 2019 Markus Iser, Luca Springer, Karlsruhe Institute of Technology (KIT)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gbd_tool.util import eprint
from tatsu import parse, exceptions
import pprint


def find_hashes(database, query=None, resolve=[]):
    statement = "SELECT DISTINCT {} FROM local {} WHERE {} GROUP BY local.hash"
    s_attributes = "local.hash"
    s_tables = ""
    s_conditions = "1=1"
    tables = { "local" }
    
    if query is not None and query:
        try:
            ast = parse(GRAMMAR, query)
        except exceptions.FailedParse as err:
            eprint(err)
            eprint("Parser Exception: The query-parser threw an exception (try using more brackets)")
            return list() 
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(ast)
        s_conditions = build_where(ast)
        tables.update(collect_tables(ast))

    if resolve is not None:
        if len(resolve) == 0:
            resolve.append("local")
        s_attributes = "local.hash, " + ", ".join(['GROUP_CONCAT(DISTINCT({}.value))'.format(table) for table in resolve])
        tables.update(resolve)

    s_tables = " ".join(['INNER JOIN {} ON local.hash = {}.hash'.format(table, table) for table in tables if table != "local"])

    eprint(statement.format(s_attributes, s_tables, s_conditions))

    return database.query(statement.format(s_attributes, s_tables, s_conditions))


def build_where(ast):
    result = ""
    if ast["q"] is not None:
        result = build_where(ast["q"])
    elif ast["qop"] is not None:
        result = '(' + build_where(ast["left"]) + " " + ast["qop"] + " " + build_where(ast["right"]) + ')'
    elif ast["sop"] is not None:
        eprint(ast["right"])
        result = ast["left"] + ".value " + ast["sop"] + " \"" + ast["right"] + "\""
    elif ast["aop"] is not None:
        result = build_where(ast["left"]) + " " + ast["aop"] + " " + build_where(ast["right"])
    elif ast["bracket_term"] is not None:
        result = '(' + build_where(ast["bracket"]) + ')'
    elif ast["top"] is not None:
        result = build_where(ast["left"]) + " " + ast["top"] + " " + build_where(ast["right"])
    elif ast["value"] is not None:
        result = "CAST(" + ast["value"] + ".value AS FLOAT)"
    elif ast["constant"] is not None:
        result = ast["constant"]
    return result


def collect_tables(ast):
    result = set()
    if ast["q"] is not None:
        result.update(collect_tables(ast["q"]))
    elif ast["qop"] is not None:
        result.update(collect_tables(ast['left']))
        result.update(collect_tables(ast['right']))
    elif ast["sop"] is not None:
        result.add(ast["left"])
    elif ast["aop"] is not None:
        result.update(collect_tables(ast["left"]))
        result.update(collect_tables(ast["right"]))
    elif ast["bracket_term"] is not None:
        result.update(collect_tables(ast["bracket_term"]))
    elif ast["top"] is not None:
        result.update(collect_tables(ast['left']))
        result.update(collect_tables(ast['right']))
    elif ast["value"] is not None:
        result.add(ast["value"])
    return result


GRAMMAR = r'''
    @@grammar::EXP
    @@ignorecase::True

    start = q:query $ ;

    query = '(' q:query ')' | left:query qop:('and' | 'or') right:query | scon | acon;

    scon = left:colname sop:('=' | '!=') right:alnum | left:colname sop:('like') right:likean ;
        
    acon = left:term aop:('=' | '!=' | '<' | '>' | '<=' | '>=' ) right:term ;

    term = value:colname | constant:num | '(' left:term top:('+'|'-'|'*'|'/') right:term ')' ;

    num = /[0-9\.\-]+/ ;
    alnum = /[a-zA-Z0-9_\.\-\/]+/ ;
    likean = /[\%]?[a-zA-Z0-9_\.\-\/]+[\%]?/;
    colname = /[a-zA-Z][a-zA-Z0-9_]+/ ;
'''
