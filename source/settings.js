const vscode = require('vscode');

function getSettings() {
    const config = vscode.workspace.getConfiguration('fortify');
    const continuationCharacter = config.get('continuationCharacter');

    // Validate continuationCharacter length
    if (continuationCharacter.length !== 1) {
        vscode.window.showWarningMessage('Continuation character must be a single character. Only the first letter of the string will be used.');
    }

    return {
        lineCarryOverLastColumnFixedForm: config.get('lineCarryOverLastColumnFixedForm'),
        lowercasing: config.get('lowercasing'),
        commentCharacter: config.get('commentCharacter'),
        continuationCharacter: continuationCharacter,
        commentLines: config.get('commentLines'),
        tabLength: config.get('tabLength')
    };
}

module.exports = {
    getSettings
};