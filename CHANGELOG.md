# Changelog

## [1.1.0] - 2025-Jan-21
### Added
- Fixed a bug where indentation would not work with data type functions (e.g. `integer*4 function` or `integer(4) function`)
- Now properly indents this, but must be of the form: `data_type function`, `data_type*num function`, or `data_type(num) function`, where `data_type` is `integer, real, complex`, etc and `num = 1, 2, 4, 8`.

## [1.1.0] - 2025-Jan-21
### Added
- Fixed a lot of bugs with the extension not working well with VS Code's interface.
- User settings have been updated, tested, and have had testing added for all possible user combinations.
- Some minor bug fixes

## [1.0.2] - 2025-Jan-16
### Added
- Fixing bug where VS Code was treating the line-comment style as a command instead of a string

## [1.0.1] - 2025-Jan-16
### Added
- Fixed a bug where a double slash "//" string concat with printing with a space between

## [1.0.0] - 2025-Jan-12
### Added
- Initial release of Fortify v1.0.0