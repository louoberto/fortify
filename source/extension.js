const vscode = require('vscode');
const { exec } = require('child_process');

function activate(context) {
  let disposable = vscode.commands.registerCommand('fortify.format', function () {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found.');
      return;
    }

    const document = editor.document;
    const text = document.getText();
    
    exec('python fortify.py', { input: text }, (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(`Fortify Error: ${stderr}`);
      } else {
        editor.edit(editBuilder => {
          const fullRange = new vscode.Range(
            document.positionAt(0),
            document.positionAt(text.length)
          );
          editBuilder.replace(fullRange, stdout);
        });
        vscode.window.showInformationMessage('Fortify successfully formatted your Fortran code!');
      }
    });
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
