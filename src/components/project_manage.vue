<template>
  <div>
    <el-row>
      <el-button type="primary" icon="el-icon-plus" @click="addProjectVisible = true">Add Project</el-button>
    </el-row>

    <el-dialog title="Add Project" :visible.sync="addProjectVisible" width="30%">
      <el-form>
        <el-form-item label="Input Project Name">
          <el-input v-model="addProjectName" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <el-upload
        class="upload-zip"
        ref="upload"
        drag
        action="/api/file_upload"
        :limit=1
        :file-list="fileList"
        :on-success="handleSuccess"
        :on-error="handleError"
        :auto-upload="false"
        accept=".zip"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Drag ZIP here, or <em>Click</em></div>
        <div class="el-upload__tip" slot="tip">ZIP Only and Size < 1GB</div>
      </el-upload>

      <div slot="footer" class="dialog-footer">
        <el-button @click="addProjectVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addProject">Submit</el-button>
      </div>
    </el-dialog>


    <el-table
      :data="tableData.filter(data => !tableSearch || data.name.toLowerCase().includes(tableSearch.toLowerCase()))"
      stripe
      border
      highlight-current-row
      v-loading="loading"
      element-loading-text="Analyzing..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
      style="width: 100%">
      <el-table-column label="ID" prop="p_id" width="270"></el-table-column>
      <el-table-column label="Project Name" prop="name"></el-table-column>
      <el-table-column label="Project Path" prop="path"></el-table-column>
      <el-table-column label="Total Files" prop="total" width="90"></el-table-column>
      <el-table-column label="Created Time" prop="time"></el-table-column>
      <el-table-column
        width="290"
        align="right">
        <template slot="header" slot-scope="scope">
          <el-input
            v-model="tableSearch"
            size="mini"
            placeholder="Search By Name"/>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" type="success" icon="el-icon-edit-outline" @click="tagFile(scope.$index, scope.row)">Mark</el-button>
          <el-button size="mini" type="warning" icon="el-icon-collection-tag" @click="editClass(scope.$index, scope.row)">Class</el-button>
          <el-button size="mini" type="danger" icon="el-icon-delete" @click="deleteProject(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
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

      }
    },

    created(){
      this.fetch_project();
    },

    methods: {
      fetch_project(){
        let url_data={
          p_id: '',
          name: '',
        };
        this.$axios.post('/api/fetch_project', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.tableData = response.data['data'];
            this.projectNameList = [];
            for(let i = 0; i < this.tableData.length; i++){
              this.projectNameList.push(this.tableData[i]['name']);
            }
          }
        }).catch(err => {
          this.$notify.error({
            title: 'Error',
            message: err
          });
        });
      },

      addProject(){
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
        if(response_up['message'] === 'success'){
          this.filePath = response_up['filepath'];
          this.loading = true;
          this.addProjectVisible = false;
          let url_data={
            filePath: this.filePath,
            addProjectName: this.addProjectName,
          };
          this.$axios.post('/api/unzip', url_data).then(response => {
            if (response.data['message'] === 'success') {
              this.$notify({
                title: 'Success',
                message: 'Cost: ' + response.data['time'] + 's',
                type: 'success'
              });
              this.loading = false;
              this.fileList = [];
              this.fetch_project();
            }else{
              this.$notify.error({
                title: 'Error',
                message: 'Unknown error'
              });
              this.fileList = [];
              this.loading = false;
            }
          }).catch(err => {
            this.$notify.error({
              title: 'Error',
              duration: 0,
              message: err
            });
            this.fileList = [];
            this.addProjectName = '';
            this.loading = false;
          });
        }else{
          this.$notify.error({
            title: 'Error',
            duration: 0,
            message: response_up['message']
          });
          this.fileList = [];
        }
      },

      handleError(err, file, fileList) {
        this.$notify.error({
          title: 'Error',
          duration: 0,
          message: err
        });
        this.fileList = [];
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
          this.$axios.post('/api/delete_project', url_data).then(response => {
            if (response.data['message'] === 'success') {
              this.$notify({
                title: 'Success',
                message: 'Deleted successfully',
                type: 'success'
              });
              this.fetch_project();
            }
          }).catch(err => {
            this.$notify.error({
              title: 'Error',
              message: err
            });
          });
        }).catch(() => {

        });
      },

    },
  }
</script>
