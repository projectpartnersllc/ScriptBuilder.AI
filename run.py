import multiprocessing
import subprocess
import sys
import os
import time

def run_backend():
    """Run the FastAPI backend server."""
    subprocess.run([sys.executable, "backend.py"])

def run_frontend():
    """Run the Streamlit frontend."""
    time.sleep(2)  # Small delay to ensure backend is up
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py"])

def main():
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Create multiprocessing processes
    backend_process = multiprocessing.Process(target=run_backend)
    frontend_process = multiprocessing.Process(target=run_frontend)

    try:
        # Start both processes
        backend_process.start()
        frontend_process.start()

        # Wait for processes to complete
        frontend_process.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Terminate any remaining processes
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
