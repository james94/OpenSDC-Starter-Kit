import os
import subprocess
import sys

def run_docker_container():
    # Set default values
    script = "bash"
    if len(sys.argv) > 1:
        script = f"run --script {sys.argv[1]}"

    image_name = os.environ.get('IMAGE_NAME', 'open_sdc/sdc_backend:latest').lower()
    name = os.environ.get('NAME', 'sdc_backend')

    # Allow local X11 connections
    subprocess.run(['xhost', 'local:docker'])

    # Prepare docker run command
    cmd = [
        'docker', 'run', '-it', '--rm', '--privileged',
        f'--add-host={name}:127.0.0.1',
        '--network=host',
        f'--name={name}',
        f'-h={name}',
        '--gpus=all',
        '--ipc=host',
        f'-e=STARTING_DIR={os.getcwd()}',
        f'-e=DISPLAY={os.environ.get("DISPLAY", "")}',
        f'-e=DBUS_SESSION_BUS_ADDRESS={os.environ.get("DBUS_SESSION_BUS_ADDRESS", "")}',
        '-v=/tmp/.X11-unix:/tmp/.X11-unix',
        f'-v={os.path.expanduser("~")}/.Xauthority:{os.path.expanduser("~")}/.Xauthority',
        '-v=/var/log/open_sdc:/var/log/open_sdc',
        f'-v={os.path.expanduser("~")}:{os.path.expanduser("~")}',
        '-v=/var/lib/apport:/var/lib/apport',
        image_name,
        script,
        f'--homedir={os.path.expanduser("~")}'
    ]

    # Execute docker run command
    subprocess.run(cmd)
    

if __name__ == "__main__":
    run_docker_container()
