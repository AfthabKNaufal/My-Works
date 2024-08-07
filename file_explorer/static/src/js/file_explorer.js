/** @odoo-module */
import { registry} from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
const { Component, mount} = owl
import { jsonrpc } from "@web/core/network/rpc_service";
import {
    onWillRender,
    onWillStart,
    toRaw,
    useEffect,
    useExternalListener,
    useState,
} from "@odoo/owl";
import { renderToFragment } from "@web/core/utils/render";

let dir_loc = []

export class FileExplorer extends Component {
	setup(){
    	this.action = useService("action");
    	this.rpc = this.env.services.rpc
    	this.state = useState({ files: [] ,remote_expand_files:[], file_list:[], remote_sub_file: [], files_details: [], file_expand: [], host_id:'',user_name:'',pass: '',port:'',draggedFile: null});
    	 onWillStart(async () => {
            await this.loadFiles();
//               console.log("aaaaa")
        });
	}
	async loadFiles() {
        try {
            const response = await jsonrpc('/file_explorer/get_files', {});
            this.state.files = response.files;
//            console.log("hellooo",this)
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }
    async onClickFile(ev){
        let directory_path = ev.srcElement.parentElement.id
//        console.log("eeeeeee",ev.srcElement.parentElement.id)
        const response = await jsonrpc('/file_explorer/get_file_detailed',{directory_path})
        this.state.files_details = response.files;
//         console.log("sssss",this.state.files_details)
    }
    async onClickExpand(ev) {
//    console.log("Expand:", ev.target.id);
    if (ev.target.id === 'false') {
        ev.target.attributes.src.nodeValue = '/file_explorer/static/src/img/arrow-down.png';
        ev.target.addEventListener('click', this.onClickShrink);

        let path = ev.target.parentElement.id;
        dir_loc.push(path);
        this.props.path = dir_loc;

        const response = await jsonrpc('/file_explorer/file_expand', {path});
        this.state.file_expand = response.files;

        const parentElement = ev.srcElement.parentElement;

        if (!parentElement) {
//            console.error("Parent element is null");
            return;
        }

        this.state.file_expand.forEach((file, i) => {
            const div = document.createElement('div');
            div.id = file.path;
            div.className = 'expand-element'; // Add a class to the element
            div.style.position = 'relative';
            div.style.left = '20px';
            div.style.top = '-3px';
            div.style.bottom = '10px';

            const imgRight = document.createElement('img');
            imgRight.src = '/file_explorer/static/src/img/arrow-right.png';
            imgRight.style.width = '13px';
            imgRight.style.height = '13px';
            imgRight.style.marginRight = '8px';
            imgRight.style.position = 'relative';
            imgRight.style.left = '20px';
            imgRight.style.top = '10px';
            imgRight.className = 'right-side-img';
            imgRight.id = 'false';
            imgRight.onclick = (ev) => this.onClickExpand(ev);

            const imgFolder = document.createElement('img');
            imgFolder.src = '/file_explorer/static/src/img/folder.png';
            imgFolder.style.width = '24px';
            imgFolder.style.height = '24px';
            imgFolder.style.marginRight = '8px';
            imgFolder.style.position = 'relative';
            imgFolder.style.left = '20px';
            imgFolder.style.top = '10px';
            imgFolder.className = 'folder-img';
            imgFolder.onclick = (ev) => this.onClickFile(ev);

            const span = document.createElement('span');
            span.className = 'expand_file_name';
            span.textContent = file.name;

            div.appendChild(imgRight);
            div.appendChild(imgFolder);
            div.appendChild(span);

            parentElement.appendChild(div);
        });

        ev.target.id = true;
    }
}
        async onClickShrink(ev) {
//    console.log("Shrink:", ev.target.id);
    if (ev.target.id === 'true') {
        ev.target.attributes.src.nodeValue = '/file_explorer/static/src/img/arrow-right.png';

        const parentElement = ev.srcElement.parentElement;
//        console.log("Shrink parent:", parentElement);
        if (!parentElement) {
            console.error("Parent element is null");
            return;
        }

        // Remove only the elements with the class 'expand-element'
        const elementsToRemove = [];
        for (let i = 0; i < parentElement.children.length; i++) {
            const child = parentElement.children[i];
            if (child.classList.contains('expand-element')) {
                elementsToRemove.push(child);
            }
        }

        elementsToRemove.forEach(element => parentElement.removeChild(element));

        ev.target.id = 'false';
    }

}
        async onClickConnect(ev){
//            console.log('connect',this)
            let host = this.state.host_id;
            let user = this.state.user_name;
            let password = this.state.pass;
            let port_number = this.state.port;
            const response = await jsonrpc('/fileexplorer/connect', {'host':host,'user':user,'password':password,'port_number':port_number});
//            console.log("connect_return",response.files_list)
            this.state.file_list = response.files_list
            console.log(this.state.file_list)
        }
        async onClickFile_remote(ev)
        {
            let host = this.state.host_id;
            let user = this.state.user_name;
            let password = this.state.pass;
            let port_number = this.state.port;
//            console.log("haiiiii",ev.srcElement.parentElement.id)
            let path = ev.srcElement.parentElement.id
            const response = await jsonrpc('/fileexplorer/filedetails_remote',{'host':host,'user':user,'password':password,'port_number':port_number,'path': path});
//            console.log("remote_files",response)
            this.state.remote_sub_file = response.remote_files
            console.log("yolo",this.state.remote_sub_file)
        }
        async onClickExpandResponse(ev){
            console.log(ev.target.id)
            if (ev.target.id === 'false') {
                ev.target.attributes.src.nodeValue = '/file_explorer/static/src/img/arrow-down.png';
                ev.target.addEventListener('click', this.onClickShrinkResponse);
                let host = this.state.host_id;
                let user = this.state.user_name;
                let password = this.state.pass;
                let port_number = this.state.port;
                let path = ev.srcElement.parentElement.id
                const response = await jsonrpc('/fileexplorer/file_expand_remote',{'host':host,'user':user,'password':password,'port_number':port_number,'path': path});
                console.log("mmmmmmmmmm",response.expand_file)
                this.state.remote_expand_files = response.expand_file
                const parentElement = ev.srcElement.parentElement;

            if (!parentElement) {
    //            console.error("Parent element is null");
                return;
            }

            this.state.remote_expand_files.forEach((file, i) => {
                const div = document.createElement('div');
                div.id = file.path;
                div.className = 'expand-element'; // Add a class to the element
                div.style.position = 'relative';
                div.style.left = '20px';
                div.style.top = '-3px';
                div.style.bottom = '10px';

                const imgRight = document.createElement('img');
                imgRight.src = '/file_explorer/static/src/img/arrow-right.png';
                imgRight.style.width = '13px';
                imgRight.style.height = '13px';
                imgRight.style.marginRight = '8px';
                imgRight.style.position = 'relative';
                imgRight.style.left = '20px';
                imgRight.style.top = '10px';
                imgRight.className = 'right-side-img';
                imgRight.id = 'false';
                imgRight.onclick = (ev) => this.onClickExpandResponse(ev);

                const imgFolder = document.createElement('img');
                imgFolder.src = '/file_explorer/static/src/img/folder.png';
                imgFolder.style.width = '24px';
                imgFolder.style.height = '24px';
                imgFolder.style.marginRight = '8px';
                imgFolder.style.position = 'relative';
                imgFolder.style.left = '20px';
                imgFolder.style.top = '10px';
                imgFolder.className = 'folder-img';
                imgFolder.onclick = (ev) => this.onClickFile_remote(ev);

                const span = document.createElement('span');
                span.className = 'expand_file_name';
                span.textContent = file.name;

                div.appendChild(imgRight);
                div.appendChild(imgFolder);
                div.appendChild(span);

                parentElement.appendChild(div);
            });
                ev.target.id = true;
            }
        }

         async onClickShrinkResponse(ev) {
         console.log('haiii')
////    console.log("Shrink:", ev.target.id);
    if (ev.target.id === 'true') {
        ev.target.attributes.src.nodeValue = '/file_explorer/static/src/img/arrow-right.png';

        const parentElement = ev.srcElement.parentElement;
//        console.log("Shrink parent:", parentElement);
        if (!parentElement) {
            console.error("Parent element is null");
            return;
        }

        // Remove only the elements with the class 'expand-element'
        const elementsToRemove = [];
        for (let i = 0; i < parentElement.children.length; i++) {
            const child = parentElement.children[i];
            if (child.classList.contains('expand-element')) {
                elementsToRemove.push(child);
            }
        }

        elementsToRemove.forEach(element => parentElement.removeChild(element));

        ev.target.id = 'false';
    }
    }
//     onDragStart(ev) {
//        this.state.draggedFile = ev.target.id;
//    }
//
//    async onDrop(ev) {
//        ev.preventDefault();
//        const targetPath = ev.target.id;
//
//        if (this.state.draggedFile && targetPath) {
//            let host = this.state.host_id;
//            let user = this.state.user_name;
//            let password = this.state.pass;
//            let port_number = this.state.port;
//
//            try {
//                await jsonrpc('/fileexplorer/copy_file', {
//                    'host': host,
//                    'user': user,
//                    'password': password,
//                    'port_number': port_number,
//                    'source_path': this.state.draggedFile,
//                    'target_path': targetPath
//                });
//
//                console.log(`File ${this.state.draggedFile} copied to ${targetPath}`);
//                this.state.draggedFile = null;
//            } catch (error) {
//                console.error('Error copying file:', error);
//            }
//        }
//    }
//
//    onDragOver(ev) {
//        ev.preventDefault();
//    }
}

FileExplorer.template = "client_action.file_explorer"
registry.category("actions").add("file_explorer", FileExplorer)


