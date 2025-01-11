# fortify
Fortran Formatting Tool

## Overview
Fortify is a Fortran formatting tool designed to help developers maintain consistent and readable code. It provides various features to handle spacing, indentation, and other formatting aspects of Fortran code.

## Features

### 1. Parenthesis Spacing
Handles formatting for objects around and inside parentheses `()` to ensure proper spacing.

### 2. Remove Extra Space
Removes unnecessary double spacing in a code line to maintain clean and readable code.

### 3. Relational Operator Spacing
Adds spaces around relational operators such as `<`, `<=`, `>`, `>=`, `/=`, `==`, and `//` to ensure proper spacing.

### 4. Comma Spacing
Handles spacing around commas to ensure there is a space after each comma, improving readability.

### 5. Logical Operator Spacing
Adds spaces between logical expressions, converting `x.gt.y` to `x .gt. y`.

### 6. Line Carry Over
Manages line continuation by finding appropriate places to break lines and carry over to the next line, ensuring code remains within a specified column width.

### 7. Plus Spacing
Handles spacing around the plus `+` operator to ensure proper spacing in various contexts.

### 8. String Handling
Properly handles strings enclosed in single or double quotes, ensuring they are not broken or improperly formatted.

### 9. Comment Handling
Maintains the integrity of comments, ensuring they are not altered or misplaced during formatting.

### 10. Tab to Space Conversion
Converts tab characters to spaces to maintain consistent indentation throughout the code.

### 11. Continuation Character Standardization
Standardizes the line continuation character to `&` for fixed format, ensuring consistency.

## Usage
To use Fortify, simply run the tool on your Fortran source files. The tool will automatically apply the formatting rules and update the files accordingly.

## Installation
To install Fortify, clone the repository and run the setup script:

```sh
git clone https://github.com/yourusername/fortify.git
cd fortify
python setup.py install
```