import os

from scp import SCPClient, SCPException

from odoo import models, fields, api
from ftplib import FTP, error_perm
import paramiko


class FtpIntegration(models.Model):
    _name = 'ftp.integration'
    _description = 'FTP Integration'

    @api.model
    def get_directories_local(self):
        file_directory = '/'
        if not os.path.exists(file_directory):
            return {'files': []}
        files = os.listdir(file_directory)
        file_list = [{'name': f, 'path': os.path.join(file_directory, f), 'expand': 'false'} for f in files]
        print(file_list)
        return {'files': file_list}

    @api.model
    def get_file_detailed_local(self, directory_path):
        base_directory = directory_path
        if directory_path is None:
            directory_path = ''

        full_path = os.path.join(base_directory, directory_path)
        print(f"Directory path: {full_path}")

        if not os.path.exists(full_path):
            return {'files': []}

        files = os.listdir(full_path)
        print(f"Files in directory: {files}")

        file_list = []
        for f in files:
            file_path = os.path.join(full_path, f)
            if os.path.isdir(file_path):
                file_type = 'directory'
            else:
                file_type = 'txt'
            file_list.append({'name': f, 'path': os.path.join(directory_path, f), 'type': file_type})

        print(f"File list: {file_list}")
        return {'files': file_list}

    @api.model
    def file_expand_local(self, path):
        base_directory = path
        if path is None:
            directory_path = ''

        full_path = os.path.join(base_directory, path)
        print(f"Directory path: {full_path}")

        if not os.path.exists(full_path):
            return {'files': []}

        files = os.listdir(full_path)
        print(f"Files in directory: {files}")

        file_list = []
        for f in files:
            file_path = os.path.join(full_path, f)
            if os.path.isdir(file_path):
                file_list.append({'name': f, 'path': os.path.join(path, f), 'type': 'directory', 'expand': 'false'})

        print(f"File list: {file_list}")
        return {'files': file_list}

    @api.model
    def get_remote_file_details(self, host, user_name, password, port, path):
        # path = kwargs['path']
        # host = kwargs['host']
        # user_name = kwargs['user']
        # password = kwargs['password']
        # port = kwargs['port_number']
        print(path)
        result = self.env['ftp.integration'].get_remote_subfiles(host, user_name, password, port, path)
        print("resulttttt", result)
        return {'remote_files': result}

    @api.model
    def file_expand_remote(self, host, user, password, port_number, path):
        result = self.env['ftp.integration'].get_remote_files_expand(host, user, password, port_number, path)
        return {'expand_file': result}

    @api.model
    def connect_remote(self, host, user, password, port_number):
        result = self.env['ftp.integration'].connect_ssh(host, user, password, port_number)
        print('akkkskskkksk', result)
        return {'files_list': result['directories']}
        # except Exception as e:
        #     return json.dumps({'status': 'error', 'message_control': str(e)})

        # return False

    @api.model
    def copy_to_remote(self, host, user, password, port_number, source_path, target_path, direction):
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        ssh.connect(host, port_number, user, password)

        # Create target directory on remote server if it doesn't exist (for upload)
        if direction == 'upload':
            stdin, stdout, stderr = ssh.exec_command(f'mkdir -p {target_path}')
            stdout.channel.recv_exit_status()  # Ensure the command was executed

        # Create an SCP client
        with SCPClient(ssh.get_transport()) as scp:
            if direction == 'upload':
                if os.path.isdir(source_path):
                    # Upload directory recursively to the remote server
                    scp.put(source_path, target_path, recursive=True)
                    print(f"Directory {source_path} copied to {target_path} on remote server.")
                else:
                    # Upload file to the remote server
                    scp.put(source_path, target_path)
                    print(f"File {source_path} copied to {target_path} on remote server.")
            elif direction == 'download':
                # Ensure the target directory exists on the local machine
                if not os.path.exists(target_path):
                    os.makedirs(target_path)

                if self.remote_is_dir(ssh, source_path):
                    # Ensure the target path ends with a slash if it's a directory
                    if not target_path.endswith('/'):
                        target_path += '/'
                    # Download directory recursively from the remote server
                    scp.get(source_path, target_path, recursive=True)
                    print(f"Directory {source_path} copied to {target_path} on local machine.")
                else:
                    # Download file from the remote server
                    scp.get(source_path, target_path)
                    print(f"File {source_path} copied to {target_path} on local machine.")
            else:
                print("Invalid direction. Use 'upload' or 'download'.")

        # Close the connection
        ssh.close()

    def remote_is_dir(self, ssh, path):
        stdin, stdout, stderr = ssh.exec_command(f'if [ -d "{path}" ]; then echo "directory"; else echo "file"; fi')
        result = stdout.read().decode().strip()
        return result == "directory"

    def connect_ssh(self, host, username, password, port):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, port=port, username=username, password=password)

            # Get the current working directory
            stdin, stdout, stderr = ssh.exec_command('pwd')
            current_directory = stdout.read().decode().strip()

            # List details of the current directory and its subdirectories
            stdin, stdout, stderr = ssh.exec_command('ls -ld . */')
            output = stdout.read().decode()



            directories = self.parse_ls_output(output, current_directory)
            print('jdshdsigdsg',directories)
            return {'status': 'success', 'directories': directories}

        except Exception as e:
            return {'status': 'error', 'message': f"Connection failed: {str(e)}"}

    def parse_ls_output(self, output, current_directory):
        lines = output.split('\n')
        directories = []
        for line in lines[1:]:
            if line:
                parts = line.split()
                directory_name = ' '.join(parts[8:]).rstrip('/')
                directories.append({
                    'path': f"{current_directory}/{directory_name}",
                    'name': directory_name,
                    'expand': 'false'
                })
        print(directories)
        return directories

    def get_remote_subfiles(self, host, username, password, port, path):
        subfiles = []

        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the server
            ssh.connect(host, port, username, password)

            # Execute the command to list files in the directory
            stdin, stdout, stderr = ssh.exec_command(f'ls -l {path}')

            # Read the command output
            lines = stdout.readlines()

            for line in lines[1:]:  # Skip the first line as it is the total
                parts = line.split()
                file_type = 'directory' if parts[0][0] == 'd' else 'file'
                file_name = parts[-1]
                subfiles.append({'name': file_name, 'type': file_type, 'path': f"{path}/{file_name}"})

            # Close the connection
            ssh.close()

        except Exception as e:
            subfiles.append({'error': str(e)})
        print(subfiles)
        return subfiles

    def get_remote_files_expand(self, host, username, password, port, path):
        directories = []
        print("haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")

        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the server
            ssh.connect(host, port, username, password)

            # Execute the command to list files in the directory
            stdin, stdout, stderr = ssh.exec_command(f'ls -l {path}')

            # Read the command output
            lines = stdout.readlines()

            for line in lines[1:]:  # Skip the first line as it is the total
                parts = line.split()
                file_type = 'directory' if parts[0][0] == 'd' else 'file'
                file_name = parts[-1]

                # Only add directories to the list
                if file_type == 'directory':
                    directories.append({'name': file_name, 'type': file_type, 'path': f"{path}/{file_name}"})

            # Close the connection
            ssh.close()

        except Exception as e:
            print(f"An error occurred: {e}")

        return directories


