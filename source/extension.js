// filepath: /C:/Users/Lou/tools/fortify/source/extension.js
const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

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

        exec(`python "${scriptPath}" "${filePath}"`, (error, stdout, stderr) => {
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