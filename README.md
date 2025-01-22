# Fortify
Fortran Formatting Tool

## Overview
Fortify is a Fortran formatting tool designed to help developers maintain consistent and readable code. It provides various features to handle spacing, indentation, and other formatting aspects of Fortran code.

![F77 Example](images/example1.png)

## Features
### Structure Indentation
Will properly indent and nest if, do, subroutine, program, and any other keyword statements that can be ended with an `end`. This works for both free format and fixed format files.

In the case of the do-continue F77 statement, it will find the matching goto-continue and unindent on that. This will work even in a do-loop that contains multiple do's that end on the same continue.

![F77 Example 2](images/example2.png)

**Note:** All fixed format files will have the first 6 columns reserved, while all free format files use every column

### Tab indentation length
You may set the tab length to either 2, 3, or 4. It is set to 3 by default.

### Logical/Relational/Math Operator Spacing
Adds spaces around operators such as `<`, `<=`, `>`, `>=`, `/=`, `==`, `//`, `+`, `-`, `*`, `/` as well as their text based counter to ensure proper spacing. This converts, for example, `x.gt.y` to `x .gt. y`.

Special care is taken for `+-` operators for cases such exponentiation (`D` and `E`), as well as cases where a minus (or plus) tends to be connected with the character. For example, the following will be maintained or enforced: `x = -5` instead of `x = - 5`.

### Tab character replacement
Converts the `\t` character to the default tab space.

### Comment spacing preservation
Will retain the original spacing between a line comment and a the code. This is done since it is a common practice to have comments lined up in a series after related code.

Lines which are only comments are kept on the first column and kept this way. This can be user defined.

### Skip line formatting option
If you wish for a line to skip formatting, simply add `no format` to a comment in-line (e.g. `! no format`). The phrase `no format` may appear anywhere in the comment.
**Warning:** this may cause intended side effects if placed on an indent identifier (e.g. if, do, endif, enddo lines).

## Free format features
### Comment line treatment
This allows comment-only lines (lines which only have comments them, no executable code) to moved around in 1 of 3 ways; either indent them with the rest of the code, leave them as is, or move them all to the first column. The default is indent. You can change this behavior in the settings. 

## Fixed format features
#### Continuation Character
In older Fortran, any character may become the continuation character. This formatter enforces the modern `&` in the 6th column, by default. You may change this if you wish.

#### Comment Character
In older Fortran, `*`, `C`, and `c` will change to become `!` by default. You may change this if you wish in the settings.

### Line Carry Over
Manages line continuation by finding appropriate places to break lines and carry over to the next line, ensuring code remains within the specified column width. The final usable line is default set to 72, but can be set to 132 in the settings.

## Other Features
### Code modernization techinques
By default, it will lower all non-string code. As Fortran is case-insensitive, this does change any code logic, and modernizes the all CAP past of older Fortran code. This may be changed in the user settings.

### Parenthesis Spacing
Removes spaces formatting for objects around and inside parentheses `( x )` -> `(x)`.

### Remove Extra Space
Removes unnecessary double spacing in a code line to maintain clean and readable code.

### Comma Spacing
Handles spacing around commas to ensure there is a space after each comma, improving readability.

### String Handling
Properly handles strings enclosed in single or double quotes, ensuring they are not broken or improperly formatted.

![Ignoring Strings](images/example3.png)

## User defined inputs
Many defaults are set to the modern Fortran standard, but are able to be re-defined by the user. These include:
| Variable | Default Value | Values | Format | Description | 
|----------|---------------|--------|-------------|-------------|
| Comment Character | `!`  | `(!, *, C, c)` | Fixed only |Change the first-column comment character. |
| Comment Lines | `indent` | `(first_column, as_is, indent)` | Free only | Determine behavior for how comment-only lines are positioned.|
| Continuation Character | `&` | any character | Fixed only | Can change the 6th column continuation character. |
| Last column length | `72` | `(72, 132)` |Fixed only | Sets the last usable column |
| Lowercase all non-string code  | `T` | `(T, F)` | Fixed and free | Lowercase all code |
| Tab Length  | `3`  | `(2, 3, 4)`|Fixed and free | Set the default tab length |


## Usage
To use Fortify, simply run the tool on your Fortran source files. The tool will automatically apply the formatting rules and update the files accordingly.

## Installation
To install Fortify, clone the repository and run the setup script:

```sh
git clone https://github.com/louoberto/fortify.git
cd fortify
export PATH=$PATH:$(pwd)/source
```
<!-- 
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. -->

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or issues, please ask a question on the Q&A or open an issue on the GitHub repository.
