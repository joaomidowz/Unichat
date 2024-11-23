import subprocess
import os

def run_backend():
    # Save the current working directory
    project_root = os.getcwd()

    # Change to the backend directory
    backend_dir = os.path.join(project_root, 'backend')
    if not os.path.exists(backend_dir):
        raise FileNotFoundError(f"Backend directory not found: {backend_dir}")
    os.chdir(backend_dir)

    # Use zsh to execute the command
    command = "node server.js"
    process = subprocess.Popen(command, shell=True, executable="/bin/zsh")

    # Return to the project root directory
    os.chdir(project_root)
    return process

def run_frontend():
    # Save the current working directory
    project_root = os.getcwd()

    # Change to the frontend directory
    frontend_dir = os.path.join(project_root, 'frontend')
    if not os.path.exists(frontend_dir):
        raise FileNotFoundError(f"Frontend directory not found: {frontend_dir}")
    os.chdir(frontend_dir)

    # Use zsh to execute the command
    command = "streamlit run Home.py"
    process = subprocess.Popen(command, shell=True, executable="/bin/zsh")

    # Return to the project root directory
    os.chdir(project_root)
    return process

if __name__ == "__main__":
    try:
        # Run backend and frontend in parallel
        backend_process = run_backend()
        frontend_process = run_frontend()

        # Wait for processes to complete
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        # Terminate both processes on interrupt
        backend_process.terminate()
        frontend_process.terminate()
        print("Processes terminated.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
