from read_file import read_file
from convert_line_breaks import convert_line_breaks
from lowercasing import lowercasing
from convert_comment_char import convert_comment_char
from tab_to_spaces import tab_to_spaces
from print_file import print_file
from if_logicals_spacing import if_logicals_spacing
from paren_spacing import paren_spacing
from relational_op_spacing import relational_op_spacing
from comma_colon_spacing import comma_colon_spacing
from remove_extra_whitespace import remove_extra_whitespace
from star_spacing import star_spacing
from plus_spacing import plus_spacing
from minus_spacing import minus_spacing
from structured_indent import structured_indent
from line_carry_over import line_carry_over
from lineup_f90_line_continuations import lineup_f90_line_continuations


class fortify:
    # Constructor to initialize object attributes
    def __init__(self, continuation_char="&", ff_column_len=6, tab_len=3):
        # These are variables
        self.continuation_char = continuation_char  # Can make this user defined I suppose, but only for ff
        self.ff_column_len = ff_column_len  # Reserved space for fixed format
        self.tab_len = tab_len  # Make default tab space 3
        self.free_form = False
        self.space = " "
        self.comment_char = "!"
        self.data_types = [
            "integer",
            "real",
            "complex",
            "character",
            "logical",
            "double precision",
        ]  # Variable declartion types, referenced in multiple functions
        self.iftypes = [".and.", ".not."]  # These are 3 letter
        self.iftypes2 = [  # These are 2 letter
            ".eq.",
            ".ge.",
            ".gt.",
            ".le.",
            ".lt.",
            ".ne.",
            ".or.",
        ]
        # These are functions
        self.read_file = read_file  # Read and stoe the file_lines of the file to format
        if self.free_form:
            self.last_col = 131  # Last usable column in Fortran
        else:
            self.last_col = 77  # Last usable column in Fortran
        # These should have toggles below
        self.convert_line_breaks = (
            convert_line_breaks  # convert continuation to & for fixed format (.f) files
        )
        self.convert_comment_char = convert_comment_char  # Converts the comment character from C, c, and * to ! for fixed format (.f) files
        self.lowercasing = lowercasing  # Converts code to lowercase
        self.tab_to_spaces = tab_to_spaces
        self.remove_extra_whitespace = remove_extra_whitespace
        self.if_logicals_spacing = if_logicals_spacing
        self.paren_spacing = paren_spacing
        self.relational_op_spacing = relational_op_spacing
        self.comma_colon_spacing = comma_colon_spacing
        self.star_spacing = star_spacing
        self.plus_spacing = plus_spacing
        self.minus_spacing = minus_spacing
        self.print_file = print_file
        self.structured_indent = structured_indent
        self.line_carry_over = line_carry_over
        self.lineup_f90_line_continuations = lineup_f90_line_continuations

    keywords_increase = [
        "contains",
        "do",
        "function",
        "if",
        "interface",
        "module",
        "program",
        "recursive function",
        "select",
        "structure",
        "subroutine",
        "type",
        "type,",
        "where",
    ]
    keywords_decrease = [
        "enddo",
        "end do",
        "endfunction",
        "end function",
        "endif",
        "end if",
        "endinterface",
        "end interface",
        "endmodule",
        "end module",
        "endprogram",
        "end program",
        "endselect",
        "end select",
        "endstructure",
        "end structure",
        "endsubroutine",
        "end subroutine",
        "endtype",
        "end type",
        "endwhere",
        "end where",
    ]


#     if f90:
#         if lynes[-1][-1] != "\n":
#             lynes[-1] = lynes[-1] + "\n"
#             print("Added newline at end of file")
