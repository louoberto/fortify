const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');
const settings = require('./settings');

let outputChannel;

function activate(context) {
    outputChannel = vscode.window.createOutputChannel('Fortify Formatter');
    outputChannel.appendLine('Fortify Formatter activated');

    let disposable = vscode.commands.registerCommand('fortify.format', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found');
            return;
        }

        const document = editor.document;
        const filePath = document.fileName;
        const scriptPath = path.join(__dirname, 'fortify');
        const config = settings.getSettings();
        const lowercasing = config.lowercasing;
        const lineCarryOverLastColumnFreeForm = config.lineCarryOverLastColumnFreeForm;
        const lineCarryOverLastColumnFixedForm = config.lineCarryOverLastColumnFixedForm;
        const commentCharacter = config.commentCharacter;
        const commentLines = config.commentLines;
        const continuationCharacter = config.continuationCharacter;
        const tabLength = config.tabLength;

        exec(
            `python '${scriptPath}' '${filePath}' ` +
            `--last_column_free_form ${lineCarryOverLastColumnFreeForm} ` +
            `--last_column_fixed_form ${lineCarryOverLastColumnFixedForm} ` +
            `--lowercasing ${lowercasing} ` + 
            `--comment_character '${commentCharacter}' ` +
            `--continuation_character '${continuationCharacter}' ` +
            `--comment_lines '${commentLines}' ` +
            `--tab_length ${tabLength} `,
            (error, stdout, stderr) => {
                if (error) {
                // vscode.window.showErrorMessage(`Command execution failed.\nError: ${error.message}\nStderr: ${stderr}`);
                outputChannel.appendLine(`Error: ${error.message}`);
                outputChannel.appendLine(`Stderr: ${stderr}`);
                return;
            }
            if (stderr) {
                outputChannel.appendLine(`Stderr: ${stderr}`);
            }
            vscode.window.showInformationMessage(stdout);
            outputChannel.appendLine(stdout);
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};