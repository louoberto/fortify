import vscode
import subprocess

def activate(context):
    # Register the format command
    context.subscriptions.append(
        vscode.commands.register_command('fortify.format', format_fortran_code)
    )

def format_fortran_code():
    # Call the standalone Python program
    try:
        result = subprocess.run(['python', 'source/fortify.py'], capture_output=True, text=True)
        vscode.window.show_information_message(result.stdout)
    except Exception as e:
        vscode.window.show_error_message(f"Error formatting Fortran code: {e}")

def deactivate():
    pass