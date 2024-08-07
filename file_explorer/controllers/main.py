import os

import paramiko

from odoo import http
from odoo.http import  request, route
from odoo.tools.safe_eval import json


class FileExplorer(http.Controller):
    @route('/fileexplorer/connect', auth='user', type='json')
    def file_explorer_submit(self, **kwargs):
        print("sdassdsddddddddd",kwargs)
        host = kwargs['host']
        user_name = kwargs['user']
        password = kwargs['password']
        port = kwargs['port_number']
        # print("data", kwargs)
        # try:
        result = request.env['ftp.integration'].connect_ssh(host, user_name, password, port)
        print('akkkskskkksk', result)
        return {'files_list': result['directories']}
        # except Exception as e:
        #     return json.dumps({'status': 'error', 'message_control': str(e)})

        # return False

    @http.route('/file_explorer/get_files', type='json', auth='user')
    def get_files(self):
        # print("controller")
        file_directory = '/'
        if not os.path.exists(file_directory):
            return {'files': []}
        files = os.listdir(file_directory)
        file_list = [{'name': f, 'path': os.path.join(file_directory, f), 'expand': 'false'} for f in files]
        print(file_list)
        return {'files': file_list}

    @http.route('/file_explorer/get_file_detailed', type='json', auth='user')
    def get_file_details(self, directory_path):
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

    @http.route('/file_explorer/file_expand', type='json', auth='user')
    def file_expand(self, path):
        print("mnmnmnmn")
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

    @http.route('/fileexplorer/filedetails_remote', type='json', auth='user')
    def remote_file_details(self, **kwargs):
        print(kwargs)
        path = kwargs['path']
        host = kwargs['host']
        user_name = kwargs['user']
        password = kwargs['password']
        port = kwargs['port_number']
        print(path)
        result = request.env['ftp.integration'].get_remote_subfiles(host, user_name, password, port, path)
        print("resulttttt",result)
        return {'remote_files': result}

    @http.route('/fileexplorer/file_expand_remote', type='json', auth='user')
    def remote_file_expand(self, **kwargs):
        print(kwargs)
        path = kwargs['path']
        host = kwargs['host']
        user_name = kwargs['user']
        password = kwargs['password']
        port = kwargs['port_number']
        result = request.env['ftp.integration'].get_remote_files_expand(host, user_name, password, port, path)
        return {'expand_file': result}

    # def copy_file(self, host, user, password, port_number, source_path, target_path):
    #     try:
    #         ssh = paramiko.SSHClient()
    #         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #         ssh.connect(host, port_number, user, password)
    #
    #         sftp = ssh.open_sftp()
    #         source_file = sftp.file(source_path, mode='r')
    #         target_file = sftp.file(target_path, mode='w')
    #
    #         target_file.write(source_file.read())
    #
    #         source_file.close()
    #         target_file.close()
    #         sftp.close()
    #         ssh.close()
    #
    #         return {'result': 'success'}
    #     except Exception as e:
    #         return {'error': str(e)}

