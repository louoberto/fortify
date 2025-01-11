# ========================================================================
# Function: fortify
# ========================================================================
# Purpose:
# Creates the fortify class, which contains all the needed objects
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


class fortify:
    # Constructor to initialize object attributes
    def __init__(self, continuation_char = '&', tab_len = 3):
        # These are variables
        self.continuation_char = continuation_char  # Can make this user defined I suppose, but only for ff
        self.ff_column_len = 6  # Reserved space for fixed format
        self.tab_len = tab_len  # Make default tab space 3
        self.free_form = False
        self.empty = ''
        self.space = ' '
        self.comment = '!'
        self.newline = '\n'
        self.tab = '\t'
        self.data_types = [
            'integer',
            'real',
            'complex',
            'character',
            'logical',
            'double precision',
        ]  # Variable declartion types, referenced in multiple functions
        self.iftypes = ['.and.', '.not.']  # These are 3 letter
        self.iftypes2 = [  # These are 2 letter
            '.eq.',
            '.ge.',
            '.gt.',
            '.le.',
            '.lt.',
            '.ne.',
            '.or.',
        ]
        # These are functions
        self.read_file = read_file  # Read and store the file_lines of the file to format
        self.if_logicals_spacing = if_logicals_spacing
        self.paren_spacing = paren_spacing
        self.relational_op_spacing = relational_op_spacing
        self.star_spacing = star_spacing
        self.plus_spacing = plus_spacing
        self.print_file = print_file
        self.structured_indent = structured_indent
        self.line_carry_over = line_carry_over
        self.comma_spacing = comma_spacing
        self.remove_extra_space = remove_extra_space

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
