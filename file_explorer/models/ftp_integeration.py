from odoo import models, fields, api
from ftplib import FTP, error_perm
import paramiko


class FtpIntegration(models.Model):
    _name = 'ftp.integration'
    _description = 'FTP Integration'

    # name = fields.Char(string='Name')

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