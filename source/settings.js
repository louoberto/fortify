const vscode = require('vscode');

function getSettings() {
    const config = vscode.workspace.getConfiguration('fortify');
    const continuationCharacter = config.get('continuationCharacter');

    // Validate continuationCharacter length
    if (continuationCharacter.length !== 1) {
        vscode.window.showErrorMessage('Continuation character must be a single character.');
        throw new Error('Continuation character must be a single character.');
    }

    return {
        lastColumnFreeForm: config.get('lastColumnFreeForm'),
        lastColumnFixedForm: config.get('lastColumnFixedForm'),
        lowercasing: config.get('lowercasing'),
        lineCarryOver: config.get('lineCarryOver'),
        commentCharacter: config.get('commentCharacter'),
        continuationCharacter: continuationCharacter,
        commentLines: config.get('commentLines'),
        tabLength: config.get('tabLength')
    };
}

module.exports = {
    getSettings
};