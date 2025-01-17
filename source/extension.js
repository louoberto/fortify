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
        outputChannel.appendLine(`'Config:', ${config}`);
        const lowercasing = config.lowercasing !== undefined ? config.lowercasing : true;
        const lineCarryOver = config.lineCarryOver !== undefined ? config.lineCarryOver : true;
        const lineCarryOverLastColumnFreeForm = config.lineCarryOverLastColumnFreeForm !== undefined ? config.lineCarryOverLastColumnFreeForm : 10000;
        const lineCarryOverLastColumnFixedForm = config.lineCarryOverLastColumnFixedForm !== undefined ? config.lineCarryOverLastColumnFixedForm : 72;
        const commentCharacter = config.commentCharacter !== undefined ? config.commentCharacter : '!';
        const commentLines = config.commentLines !== undefined ? config.commentLines : 'first_column';
        const continuationCharacter = config.continuationCharacter !== undefined ? config.continuationCharacter : '&';
        const tabLength = config.tabLength !== undefined ? config.tabLength : 3;
        const removeSpacing = config.removeSpacing !== undefined ? config.removeSpacing : true;
        const noFormat = config.noFormat !== undefined ? config.noFormat : 'do not format';

        exec(
            `python "${scriptPath}" "${filePath}" ` +
            `--last_column_free_form ${lineCarryOverLastColumnFreeForm} ` +
            `--last_column_fixed_form ${lineCarryOverLastColumnFixedForm} ` +
            `--lowercasing ${lowercasing} ` + 
            `--line_carry_over ${lineCarryOver} ` +
            `--comment_character ${commentCharacter} ` +
            `--continuation_character ${continuationCharacter} ` +
            `--comment_lines "${commentLines}" ` +
            `--tab_length ${tabLength} ` + 
            `--remove_spacing ${removeSpacing} ` +
            `--no_format "${noFormat}"`,
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