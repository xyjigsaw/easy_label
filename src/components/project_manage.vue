<template>
  <div>
    <el-row justify="space-around" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding: 10px;margin: 5px;">
      <el-button type="primary" icon="el-icon-folder-add" @click="addProjectVisible = true" :disabled="!parse_done">Add Project</el-button>
    </el-row>

    <el-dialog title="Add Project" :visible.sync="addProjectVisible" width="30%">
      <el-form>
        <el-form-item label="Input Project Name">
          <el-input v-model="addProjectName" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>

      <div>
        <el-checkbox-group v-model="sectionList" :min=3 size="medium">
          <el-checkbox-button v-for="item in sectionName" :label="item" :key="item"
                              :disabled="item === 'abstract' || item=== 'introduction' || item=== 'conclusion'">{{item}}</el-checkbox-button>
        </el-checkbox-group>
      </div>
      <br>
      <el-upload
        class="upload-zip"
        ref="upload"
        drag
        action="/api/file_upload"
        :limit=1
        :file-list="fileList"
        :on-change="autoAddProjectName"
        :on-success="handleSuccess"
        :on-error="handleError"
        :auto-upload="false"
        accept=".zip"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Drag ZIP here, or <em>Click</em></div>
        <div class="el-upload__tip" slot="tip">ZIP Only & No Spaces In ZIP Name</div>
      </el-upload>

      <div slot="footer" class="dialog-footer">
        <el-button @click="addProjectVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addProject">Submit</el-button>
      </div>
    </el-dialog>

    <el-dialog title="Add More Files" :visible.sync="moreFileVisible" width="30%">
      <el-card shadow="always">
        <el-button type="text">Project: {{moreFileInfo['name']}}</el-button>
        <el-button type="text">Path: {{moreFileInfo['path']}}</el-button>
        <el-button type="text">Created Time: {{moreFileInfo['time']}}</el-button>
      </el-card>
      <br>
      <div>
        <el-checkbox-group v-model="sectionList" :min=3 size="medium">
          <el-checkbox-button v-for="item in sectionName" :label="item" :key="item"
                              :disabled="item === 'abstract' || item=== 'introduction' || item=== 'conclusion'">{{item}}</el-checkbox-button>
        </el-checkbox-group>
      </div>
      <br>
      <br>
      <el-upload
        class="upload-zip-add"
        ref="upload_add"
        drag
        action="/api/file_upload"
        :limit=1
        :file-list="moreList"
        :on-success="handleSuccessAdd"
        :on-error="handleErrorAdd"
        :auto-upload="false"
        accept=".zip"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Drag ZIP here, or <em>Click</em></div>
        <div class="el-upload__tip" slot="tip">ZIP < 100MB & No Spaces In ZIP Name</div>
      </el-upload>

      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelAddFile">Cancel</el-button>
        <el-button type="primary" @click="moreFile2Project">Submit</el-button>
      </div>
    </el-dialog>

    <el-dialog title="Project Log" :visible.sync="logVisible" width="80%">
      <el-table :data="project_log">
        <el-table-column width="500" property="name" label="name" sortable></el-table-column>
        <el-table-column width="500" property="log" label="log"></el-table-column>
      </el-table>
    </el-dialog>

    <div class="table-div" style="box-shadow: 0 0 5px #dddddd;margin: 5px;">
      <el-table
        :data="tableData.filter(data => !tableSearch || data.name.toLowerCase().includes(tableSearch.toLowerCase()))"
        :row-class-name="tableRowClassName"
        border
        highlight-current-row
        v-loading="loading"
        element-loading-text="Parsing PDF, Please Do not Leave, 5s/PDF"
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)">
        <el-table-column label="ID" prop="p_id" width="280"></el-table-column>
        <el-table-column label="Project Name" sortable prop="name"></el-table-column>
        <el-table-column label="Project Path" prop="path"></el-table-column>
        <el-table-column label="Files" sortable prop="total" width="90"></el-table-column>
        <el-table-column label="Created Time" prop="time"></el-table-column>
        <el-table-column
          width="580"
          align="right">
          <template slot="header" slot-scope="scope">
            <el-input
              v-model="tableSearch"
              size="mini"
              placeholder="Search By Name"/>
          </template>
          <template slot-scope="scope">
            <el-button size="mini" type="success" icon="el-icon-edit-outline" @click="tagFile(scope.$index, scope.row)" v-show="scope.row['parse_done'] === '1'">Mark</el-button>
            <el-button size="mini" type="warning" icon="el-icon-collection-tag" @click="editClass(scope.$index, scope.row)" v-show="scope.row['parse_done'] === '1'">Class</el-button>
            <el-button size="mini" type="primary" icon="el-icon-plus" @click="addFile(scope.$index, scope.row)" v-show="scope.row['parse_done'] === '1'" :disabled="!parse_done">Add</el-button>
            <el-button size="mini" type="danger" icon="el-icon-delete" @click="deleteProject(scope.$index, scope.row)" v-show="scope.row['parse_done'] === '1'">Delete</el-button>
            <el-button size="mini" type="info" icon="el-icon-info" @click="showLog(scope.$index, scope.row)" v-show="scope.row['parse_done'] === '1'">Log</el-button>
            <el-button size="mini" icon="el-icon-download" @click="download_project(scope.$index, scope.row)" v-show="scope.row['parse_done'] === '1'">Download</el-button>
            <el-button size="medium" type="danger" icon="el-icon-loading" @click="refresh_page" plain v-show="scope.row['parse_done'] === '0'">Parsing Now, CLICK to refresh.</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        fileList: [],
        filePath: '',

        tableSearch: '',
        tableData: [],
        loading: false,
        projectNameList: [],

        addProjectName: '',
        addProjectVisible: false,

        moreFileInfo: '',
        moreFileVisible: false,
        moreList: [],

        sectionList: ['abstract', 'introduction', 'conclusion'],
        sectionName: ['abstract', 'introduction', 'conclusion', 'others'],

        parse_done: true,

        project_log: [],
        logVisible: false
      }
    },

    created(){
      this.fetch_project();
    },

    methods: {
      refresh_page(){
        location. reload();
      },

      fetch_project(){
        this.$axios.get('/api/fetch_project').then((response)=> {
          this.tableData = response.data['data'];
          for(let i = 0; i < this.tableData.length; i++){
            this.tableData[i]['total'] *= 1;
          }
          this.projectNameList = [];
          for(let i = 0; i < this.tableData.length; i++){
            this.projectNameList.push(this.tableData[i]['name']);
            if(this.tableData[i]['parse_done'] === '0'){
              this.parse_done = false;
            }
          }
        }).catch((err)=> {
          this.$notify.error({title: 'Error', message: err});
        });
      },

      autoAddProjectName(file, fileList){
        if(this.addProjectName.trim() === ''){
          this.addProjectName = String(fileList[0].name.slice(0, -4));
        }
      },

      addProject(){
        this.addProjectName = this.addProjectName.trim();
        this.addProjectName = this.addProjectName.replace(/\s+/g, '_')
        if(this.addProjectName === '') {
          this.$notify({
            title: 'Warning',
            message: 'Project name is empty.',
            type: 'warning'
          });
        }else if(this.projectNameList.indexOf(this.addProjectName) > -1){
          this.$notify({
            title: 'Warning',
            message: 'Project name has existed.',
            type: 'warning'
          });
        }else{
          this.$refs.upload.submit();
        }
      },

      handleSuccess(response_up, file, fileList) {
        this.filePath = response_up['filepath'];
        this.loading = true;
        this.addProjectVisible = false;
        let url_data={
          filePath: this.filePath,
          addProjectName: this.addProjectName,
          sectionList: this.sectionList.toString(),
        };
        this.$axios.get('/api/unzip', {params: url_data}).then(response => {
          if (response.data['message'] === 'success') {
            this.$notify({
              title: 'Success',
              message: 'Upload Successfully, Start Parsing',
              type: 'success'
            });
            this.loading = false;
            this.fileList = [];
            this.addProjectName = '';
            this.fetch_project();
          }else{
            this.$notify.error({title: 'Error', message: response.data['message']});
            this.fileList = [];
            this.addProjectName = '';
            this.loading = false;
          }
        }).catch(err => {
          this.$notify.error({title: 'Error', duration: 0, message: err});
          this.fileList = [];
          this.addProjectName = '';
          this.loading = false;
        });
      },

      handleError(err, file, fileList) {
        this.$notify.error({title: 'Error', duration: 0, message: err});
        this.addProjectName = '';
        this.fileList = [];
      },

      addFile(index, row){
        this.moreFileVisible = true;
        this.moreFileInfo = row;
      },

      cancelAddFile(){
        this.moreFileVisible = false;
        this.moreList = [];
        this.moreFileInfo = '';
      },

      moreFile2Project(){
        this.$refs.upload_add.submit();
      },

      handleSuccessAdd(response_up, moreFile, moreList) {
        this.loading = true;
        this.moreFileVisible = false;
        let url_data={
          p_id: this.moreFileInfo['p_id'],
          filePath: response_up['filepath'],
          projectName: this.moreFileInfo['name'],
          sectionList: this.sectionList.toString(),
        };
        this.$axios.get('/api/unzip_more', {params: url_data}).then(response => {
          if (response.data['message'] === 'success') {
            this.$notify({
              title: 'Success',
              duration: 0,
              message: 'Cost: ' + response.data['time'] + 's',
              type: 'success'
            });
            this.loading = false;
            this.moreList = [];
            this.fetch_project();
          }else{
            this.$notify.error({title: 'Error', message: response.data['message']});
            this.moreList = [];
            this.loading = false;
          }
        }).catch(err => {
          this.$notify.error({title: 'Error', duration: 0, message: err});
          this.moreList = [];
          this.moreFileInfo = '';
          this.loading = false;
        });
      },

      handleErrorAdd(err, moreFile, moreList) {
        this.$notify.error({title: 'Error', duration: 0, message: err});
        this.moreList = [];
        this.moreFileInfo = '';
      },

      editClass(index, row) {
        this.$router.push({path: '/home/class_manage', query: {p_id: row['p_id'], name: row['name'], path: row['path'], total: row['total']}});
      },

      tagFile(index, row) {
        this.$router.push({path: '/home/work_table', query: {p_id: row['p_id'], name: row['name'], path: row['path'], total:row['total']}});
      },

      deleteProject(index, row) {
        this.$confirm('Files and data will be deleted, continue?', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          let url_data={
            p_id: row['p_id'],
            path: row['path']
          };
          this.$axios.delete('/api/delete_project', {params: url_data}).then(response => {
            this.$notify({title: 'Success', message: 'Deleted successfully', type: 'success'});
            this.fetch_project();
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
          });
        }).catch(() => {
        });
      },

      showLog(index, row){
        this.project_log = [];
        if(row['log'] == null){
          this.project_log.push({'name': '', 'log': ''});
        }else{
          let log_ls = row['log'].split("@@@");
          for (let i = 0; i < log_ls.length; i++){
            if(log_ls[i] === "")continue;
            let item = log_ls[i].split("****")
            this.project_log.push({'name': item[0].substring(item[0].lastIndexOf('/') + 1, item[0].length), 'log': item[1]});
          }
        }
        this.logVisible = true;
      },

      download_project(index, row){
        let url_data={
          p_id: row['p_id'],
        };
        this.$axios.get('/api/download_project', {params: url_data}).then(response => {
          let FileSaver = require('file-saver');
          let content = JSON.stringify({'data': response['data']['data']});
          let blob = new Blob([content], {type: "text/plain;charset=utf-8"});
          FileSaver.saveAs(blob, row['name'] + ".json");
        }).catch(err => {
          this.$notify.error({title: 'Error', message: err});
        });
      },

      tableRowClassName({row, rowIndex}) {
        if (row['parse_done'] === "0") {
          return 'warning-row';
        } else if (row['parse_done'] === "1") {
          return 'success-row';
        }
        return 'warning-row';
      },

    },
  }
</script>
<style>
.el-table .warning-row {
  background: #fde6f4;
}

.el-table .success-row {

}

</style>
