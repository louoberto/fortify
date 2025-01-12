// filepath: /C:/Users/Lou/tools/fortify/source/extension.js
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
        const scriptPath = path.join(__dirname, 'driver.py');

        const config = settings.getSettings();
        const commentLines = config.commentLines;
        const lowercasing = config.lowercasing;
        const lineCarryOver = config.lineCarryOver;
        const lineCarryOverLastColumnFreeForm = config.lineCarryOverLastColumnFreeForm;
        const lineCarryOverLastColumnFixedForm = config.lineCarryOverLastColumnFixedForm;
        const commentCharacter = config.commentCharacter;
        const continuationCharacter = config.continuationCharacter;
        const tabLength = config.tabLength;

        exec(`python "${scriptPath}" "${filePath}" ${lineCarryOverLastColumnFreeForm} ${lineCarryOverLastColumnFixedForm} ${lowercasing} ${lineCarryOver} ${commentCharacter} ${continuationCharacter} ${commentLines} ${tabLength}`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Error: ${stderr}`);
                outputChannel.appendLine(`Error: ${stderr}`);
                return;
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