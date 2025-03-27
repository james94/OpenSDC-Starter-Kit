##
# Docker Container Entrypoint Fundamentals
##

# 1. User and Group Management
# 2. Environment Setup
# 3. Command Handling
# 4. Script Execution

##
# Entrypoint Features
##

# 1. Argument Parsing
# 2. Root Privilege Checking
# 3. Home Directory Initialization
# 4. Bashrc Validation
# 5. Command Execution (bash, help, run)

import os
import sys
import argparse
import grp
import pwd
import subprocess

class DockerEntrypointError(Exception):
    pass

class DockerEntrypoint:
    def __init__(self):
        self.commands = ['bash', 'help', 'run']
        self.progname = 'open_sdcDocker'
        self._starting_uid = os.getuid()
        self._starting_gid = os.getgid()
        self._wanted_uid = self._starting_uid
        self._wanted_gid = self._starting_gid
        self.parser = self._create_argument_parser()
        self.args = self.parser.parse_args()

    @property
    def in_docker(self):
        return os.path.isfile('/.dockerenv')
    
    def run(self):
        try:
            self._check_root_privileges()
            self._initialize_homedir()
            self._setup_environment()
            self._validate_bashrc()
            self._execute_command()
        except DockerEntrypointError as e:
            self._eprint(f"Error: {str(e)}")
            sys.exit(1)
    
    def _check_root_privileges(self):
        if self._starting_uid != 0 or self._starting_gid != 0:
            raise DockerEntrypointError("You must be root to run this script")

    def _create_argument_parser(self):
        epilog = 'Supported Commands:\n\n' + '\n'.join(self.commands)
        parser = argparse.ArgumentParser(prog=self.progname, 
            description="OpenSDC Docker Entrypoint",
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('command', help='OpenSDC high level command to run', nargs='?', default='help', choices=self.commands)
        parser.add_argument('-i', '--interactive', help='run bash in interactive mode', action='store_true')
        parser.add_argument('-l', '--login', help='run bash login scripts', action='store_true')
        parser.add_argument('--homedir', help='home directory for user')
        parser.add_argument('--script', help='script to run')
        return parser

    def _initialize_homedir(self):
        if self.args.homedir:
            try:
                stat = os.stat(self.args.homedir)
                username = os.path.basename(self.args.homedir)
                self._wanted_uid = stat.st_uid
                self._wanted_gid = stat.st_gid
                self._setup_user_and_group(username)
            except OSError as e:
                raise DockerEntrypointError(f"Error initializing home directory: {str(e)}")

    def add_group(self, group_name, gid):
        try:
            grp.getgrnam(group_name)
            print(f"Group '{group_name}' already exists")
        except KeyError:
            self._run_command(f"groupadd -g {gid} {group_name}")

    def _setup_user_and_group(self, username):
        if self._wanted_gid != self._starting_gid:
            self.add_group(group_name=username, gid=self._wanted_gid)

        if self._wanted_uid != self._starting_uid:
            self._create_user_if_not_exists(username)
    
    def _create_user_if_not_exists(self, username):
        try:
            pwd.getpwuid(self._wanted_uid)
            print(f"User '{username}' already exists")
        except KeyError:
            self._run_command(f"useradd -g {self._wanted_gid} -u {self._wanted_uid} -s /bin/bash {username}")

    def _setup_environment(self):
        if self._wanted_uid != self._starting_uid or self._wanted_gid != self._starting_gid:
            os.environ['HOME'] = pwd.getpwuid(self._wanted_uid).pw_dir
            username = pwd.getpwuid(self._wanted_uid).pw_name
            os.environ['USER'] = username
            self._setup_groups(username)
    
    def _setup_groups(self, username):
        try:
            os.setgid(self._wanted_gid)
            if self.in_docker and "sudo" not in grp.getgrnam("sudo").gr_mem:
                self._run_command(f"usermod -a -G sudo {username}")

            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]

            if "sudo" in groups:
                group_ids = [g.gr_gid for g in grp.getgrall() if username in g.gr_mem]
                os.setgroups(group_ids)
            os.setuid(self._wanted_uid)
        except OSError as e:
            raise DockerEntrypointError(f"Error setting up groups: {str(e)}")

    def _validate_bashrc(self):
        if 'HOME' not in os.environ:
            raise DockerEntrypointError("Must set HOME using --homedir or docker run -e")

        bashrc_file = os.path.abspath(os.path.join(os.environ['HOME'], '.bashrc'))
        if not os.path.isfile(bashrc_file):
            raise DockerEntrypointError("Must mount homedir using docker run -v $HOME:$HOME and ensure a .bashrc file exists")

    def _execute_command(self):
        if self.args.command == 'bash':
            self._run_bash()
        elif self.args.command == 'help':
            self.parser.print_help()
        elif self.args.command == 'run':
            self._run_script()
        else:
            self.parser.print_help()

    def _run_bash(self):
        options = []
        if self.args.interactive:
            options.append('-i')
        if self.args.login:
            options.append('-l')
        try:
            os.execl("/usr/bin/bash", "bash", *options)
        except OSError as e:
            raise DockerEntrypointError(f"Error executing bash: {str(e)}")

    def _run_script(self):
        script = self.args.script
        if not script:
            raise DockerEntrypointError("You must specify a script using --script to run")
        
        scriptparts = script.split()
        if not os.path.isfile(scriptparts[0]):
            raise DockerEntrypointError(f"Script {scriptparts[0]} does not exist")
        
        if not os.stat(scriptparts[0]).st_mode & 0o111:
            raise DockerEntrypointError(f"Script {scriptparts[0]} is not executable")

        try:
            if len(scriptparts) == 1:
                os.execl(script, script)
            else:
                sys.exit(subprocess.call(scriptparts))
        except OSError as e:
            raise DockerEntrypointError(f"Error executing script: {str(e)}")

    @staticmethod
    def _eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
    
    @staticmethod
    def _run_command(command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise DockerEntrypointError(f"Error running command '{command}': {str(e)}")
    
if __name__ == "__main__":
    entrypoint = DockerEntrypoint()
    entrypoint.run()
