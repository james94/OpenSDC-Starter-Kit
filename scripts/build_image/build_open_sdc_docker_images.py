import subprocess
import os

def run_docker_bake():
    # Get the directory of the current script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up to the project root directory
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

    # Define the relative path to sdc_entries
    ENTRIES_PATH = os.path.join(PROJECT_ROOT, 'src', 'build_image', 'sdc_backend', 'sdc_entries')

    print(f"ENTRIES_PATH = {ENTRIES_PATH}")

    # Define the path to the docker-bake.hcl file
    BAKE_DIR = os.path.join(PROJECT_ROOT, 'docker')
    BAKE_FILE = os.path.join(BAKE_DIR, 'docker-bake.hcl')

    # Change working directory to where docker-bake.hcl is located
    os.chdir(BAKE_DIR)

    # Define the command with the --allow flag to avoid confirmation prompts
    command = [
        "docker", "buildx", "bake",
        f"--allow=fs.read={ENTRIES_PATH}",
        f"--allow=fs.read={PROJECT_ROOT}",
        "-f", BAKE_FILE
    ]

    try:
        subprocess.run(command, check=True)
        print("Docker buildx bake executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Docker buildx bake: {e}")
        exit(1)

if __name__ == "__main__":
    run_docker_bake()
