# import os
#
# import paramiko
# from scp import SCPClient
#
# from odoo import http
# from odoo.http import request, route
#
#
# class FileExplorer(http.Controller):
#
#     @http.route('/fileexplorer/copy_to_remote', type='json', auth='user')
#     def copy_to_remote(self, **kwargs):
#         print("Received kwargs:", kwargs)
#         source_path = kwargs.get('path')
#         target_path = kwargs.get('target_path')
#         host = kwargs.get('host')
#         port = kwargs.get('port_number')
#         username = kwargs.get('user')
#         password = kwargs.get('password')
#         direction = kwargs.get('direction')  # Upload or Download
#
#         # Create an SSH client
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#         # Connect to the server
#         ssh.connect(host, port, username, password)
#
#         # Create target directory on remote server if it doesn't exist (for upload)
#         if direction == 'upload':
#             stdin, stdout, stderr = ssh.exec_command(f'mkdir -p {target_path}')
#             stdout.channel.recv_exit_status()  # Ensure the command was executed
#
#         # Create an SCP client
#         with SCPClient(ssh.get_transport()) as scp:
#             if direction == 'upload':
#                 if os.path.isdir(source_path):
#                     # Upload directory recursively to the remote server
#                     scp.put(source_path, target_path, recursive=True)
#                     print(f"Directory {source_path} copied to {target_path} on remote server.")
#                 else:
#                     # Upload file to the remote server
#                     scp.put(source_path, target_path)
#                     print(f"File {source_path} copied to {target_path} on remote server.")
#             elif direction == 'download':
#                 # Ensure the target directory exists on the local machine
#                 if not os.path.exists(target_path):
#                     os.makedirs(target_path)
#
#                 if self.remote_is_dir(ssh, source_path):
#                     # Ensure the target path ends with a slash if it's a directory
#                     if not target_path.endswith('/'):
#                         target_path += '/'
#                     # Download directory recursively from the remote server
#                     scp.get(source_path, target_path, recursive=True)
#                     print(f"Directory {source_path} copied to {target_path} on local machine.")
#                 else:
#                     # Download file from the remote server
#                     scp.get(source_path, target_path)
#                     print(f"File {source_path} copied to {target_path} on local machine.")
#             else:
#                 print("Invalid direction. Use 'upload' or 'download'.")
#
#         # Close the connection
#         ssh.close()
#
#     def remote_is_dir(self, ssh, path):
#         stdin, stdout, stderr = ssh.exec_command(f'if [ -d "{path}" ]; then echo "directory"; else echo "file"; fi')
#         result = stdout.read().decode().strip()
#         return result == "directory"
#
