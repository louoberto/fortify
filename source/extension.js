const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');


function activate(context) {
  let disposable = vscode.commands.registerCommand('fortify.format', function () {
      const scriptPath = path.join(__dirname, 'driver.py');
      exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
          if (error) {
              vscode.window.showErrorMessage(`Error: ${stderr}`);
              return;
          }
          vscode.window.showInformationMessage(stdout);
      });
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};