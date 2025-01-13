# ========================================================================
# Class: fortify_class
# ========================================================================
# Purpose:
# Creates the fortify_class class, which contains all the needed objects
# to format a Fortran file
# ========================================================================
from read_file import read_file
from print_file import print_file
from if_logicals_spacing import if_logicals_spacing
from paren_spacing import paren_spacing
from relational_op_spacing import relational_op_spacing
from comma_spacing import comma_spacing
from star_spacing import star_spacing
from plus_spacing import plus_spacing
from structured_indent import structured_indent
from line_carry_over import line_carry_over
from remove_extra_space import remove_extra_space
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
        self.do_carry_over = True
        self.indent = "indent"
        self.as_is = "as_is"
        self.first_col = "first_column"
        self.comment_behavior = self.first_col
        self.remove_spacing = True

        # Intrinsic to Fortran or Python
        self.ff_column_len = 6  # Reserved space for fixed format
        self.free_form = True
        self.empty = ''
        self.space = ' '
        self.newline = '\n'
        self.tab = '\t'

        # Fortran data types (not a complete list yet)
        self.data_types = [
            'integer',
            'real',
            'complex',
            'character',
            'logical',
            'double precision',
        ]

        # Logical expressions
        self.iftypes = ['.and.', '.not.']
        self.iftypes2 = ['.eq.', '.ge.', '.gt.', '.le.', '.lt.', '.ne.', '.or.']

        # Formatting functions
        self.read_file = read_file  # Read and stoe the file_lines of the file to format
        self.print_file = print_file
        self.format = format
        self.remove_extra_space = remove_extra_space
        self.if_logicals_spacing = if_logicals_spacing
        self.comma_spacing = comma_spacing
        self.paren_spacing = paren_spacing
        self.relational_op_spacing = relational_op_spacing
        self.star_spacing = star_spacing
        self.plus_spacing = plus_spacing
        self.structured_indent = structured_indent
        self.line_carry_over = line_carry_over

        # Keywords for indenting
        self.keywords_increase = [
            'contains',
            'do',
            ': do', # Still don't know what this one was doing
            'function',
            'if',
            'interface',
            'module',
            'program',
            'recursive function',
            'select',
            'structure',
            'subroutine',
            'type',
            'type,',
            'where',
        ]
        self.keywords_decrease = [
            'enddo',
            'end do',
            'endfunction',
            'end function',
            'endif',
            'end if',
            'endinterface',
            'end interface',
            'endmodule',
            'end module',
            'endprogram',
            'end program',
            'endselect',
            'end select',
            'endstructure',
            'end structure',
            'endsubroutine',
            'end subroutine',
            'endtype',
            'end type',
            'endwhere',
            'end where',
            'end',
            'continue'
        ]
