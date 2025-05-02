# ========================================================================
# Class: fortify_class
# ========================================================================
# Purpose:
# Creates the fortify_class class, which contains all the needed objects
# to format a Fortran file
# ========================================================================
from read_file import read_file
from print_file import print_file
from period_spacing import period_spacing
from paren_spacing import paren_spacing
from relational_op_spacing import relational_op_spacing
from comma_spacing import comma_spacing
from colon_spacing import colon_spacing
from star_spacing import star_spacing
from plus_spacing import plus_spacing
from semicolon_spacing import semicolon_spacing
from structured_indent import structured_indent
from line_breakup import line_breakup
from line_carry_over import line_carry_over
from remove_extra_space import remove_extra_space
from slash_spacing import slash_spacing
from debug import debug
from format import format


class fortify_class:
    # Constructor to initialize object attributes
    def __init__(self):
        # User defined variables
        self.continuation_char = '&'
        self.tab_len = 3
        self.last_col = 10000
        self.comment = '!'
        self.lowercasing = True
        self.indent = "indent"
        self.as_is = "as_is"
        self.first_col = "first_column"
        self.comment_behavior = self.first_col
        self.no_format = "no format"

        # Intrinsic to Fortran or Python
        self.ff_column_len = 6  # Reserved space for fixed format
        self.free_form = True
        self.empty = ''
        self.space = ' '
        self.newline = '\n'
        self.semicolon = ';'
        self.tab = '\t'

        # Structered indent counters and bools
        self.indenter = 0
        self.skip = False
        self.first_case = False
        self.select_indent = False
        self.class_happened = False
        self.skip_select = False
        self.select_indenter = 0
        self.ifdefdent = 0
        self.elsedent = 0
        self.endifdent = 0
        self.inside_submod = False
        self.cont_happened = False

        # Fortran data types (not a complete list yet)
        self.data_types = [
            'integer',
            'real',
            'complex',
            'character',
            'logical',
            'double precision',
            'doubleprecision',
        ]
        self.common_types = [
            'namelist',
            'data',
            'common',
            'structure'
        ]


        # Logical expressions
        self.iftypes = ['.and.', '.not.']
        self.iftypes2 = ['.eq.', '.ge.', '.gt.', '.le.', '.lt.', '.ne.', '.or.']

        # Formatting functions
        self.read_file = read_file  # Read and stoe the file_lines of the file to format
        self.print_file = print_file
        self.format = format
        self.code_line = ''
        self.lines = []
        self.remove_extra_space = remove_extra_space
        self.period_spacing = period_spacing
        self.comma_spacing = comma_spacing
        self.colon_spacing = colon_spacing
        self.paren_spacing = paren_spacing
        self.slash_spacing = slash_spacing
        self.semicolon_spacing = semicolon_spacing
        self.relational_op_spacing = relational_op_spacing
        self.star_spacing = star_spacing
        self.plus_spacing = plus_spacing
        self.structured_indent = structured_indent
        self.line_carry_over = line_carry_over
        self.line_breakup = line_breakup
        self.debug = debug
        self.function = [
            'function',
            'subroutine',
        ]

        # Keywords for indenting
        self.keywords_increase = [
            'do\n',
            'do ',
            'do',
            'function ',
            'function\n',
            'function',
            'subroutine',
            'if\n',
            'if ',
            'if(',
            'if',
            'abstract interface',
            'interface',
            'module procedure',
            'module',
            'program',
            'select',
            'case',
            'associate',
            'structure',
            'type is',
            'type ::',
            'type,',
            'type',
            'where',
            'block',
            'class is',
            'class default',
            'map',
            'union\n',
            'union ',
            'forall',
            'critical',
            'submodule',
            'rank',
            'enum,',
            'change team'
        ]
        self.keywords_decrease = [
            'continue',
            'end',
            'enddo',
            'endfunction',
            'endif',
            'endinterface',
            'endmodule',
            'endprogram',
            'endselect',
            'endstructure',
            'endsubroutine',
            'endtype',
            'endwhere',
            'endblock',
            'endmap',
            'endunion',
            'endforall',
            'endcritical',
            'endsubmodule',
            'endprocedure',
            'endenum',
            'endteam'
        ]

    def is_where_oneliner(self, line):
        line = line.strip().lower()
        if not line.startswith('where'):
            return False
        # Find the first '(' after 'where'
        first_paren = line.find('(')
        if first_paren == -1:
            return False

        count = 0
        for i in range(first_paren, len(line)):
            if line[i] == '(':
                count += 1
            elif line[i] == ')':
                count -= 1
                if count == 0:
                    # After this position, check if there's real code
                    after = line[i+1:].lstrip()
                    if after and not after.startswith(';') and not after.startswith('!'):
                        return True
                    else:
                        return False
        return False