<template>
  <div>
    <el-row justify="space-around" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding: 10px;margin: 5px;">
      <el-col :span="6">
        <el-button type="text">Project Name: {{ name }}</el-button>
      </el-col>

      <el-col :span="2">
        <el-button type="text">Files: {{ total }}</el-button>
      </el-col>

      <el-col :span="2">
        <el-button type="text">Classes: {{ tableData.length }}</el-button>
      </el-col>

      <el-col :span="2" :offset="3">
        <el-button type="danger" plain icon="el-icon-back" @click="back2project">Exit</el-button>
      </el-col>

      <el-col :span="2">
        <el-button type="success" plain icon="el-icon-edit-outline" @click="tagFile">Mark</el-button>
      </el-col>

      <el-col :span="2">
        <el-button type="primary" plain icon="el-icon-plus" @click="addLabelVisible = true">Add Class</el-button>
      </el-col>

    </el-row>

    <el-dialog title="Add Class Label" :visible.sync="addLabelVisible" width="30%">
      <el-form>
        <el-form-item label="Input Class Name">
          <el-input v-model="addLabelName" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="addLabelDes" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Choose Color">
          <el-color-picker v-model="addLabelColor"></el-color-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addLabelVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addClassLabel">Submit</el-button>
      </div>
    </el-dialog>

    <el-dialog title="Update Class Label" :visible.sync="rLabelVisible" width="30%">
      <el-form>
        <el-form-item label="New Class Name (Not recommended to modify)">
          <el-input v-model="rLabelName" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="rLabelDes" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Choose Color">
          <el-color-picker v-model="rLabelColor"></el-color-picker>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="rLabelVisible = false">Cancel</el-button>
        <el-button type="primary" @click="updateClassLabel">Submit</el-button>
      </div>
    </el-dialog>

    <el-table :data="tableData" style="box-shadow: 0 0 5px #dddddd; padding: 10px;margin: 5px; width: auto;">
      <el-table-column label="Class Label">
        <template slot-scope="scope">
          <i class="el-icon-collection-tag"></i>
          <span style="margin-left: 10px">{{ scope.row.label}}</span>
        </template>
      </el-table-column>

      <el-table-column label="Color">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>Color: {{ scope.row.color }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium" type="info" :color=scope.row.color border-color="transparent">{{ scope.row.color }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>

      <el-table-column label="Description">
        <template slot-scope="scope">
          <i class="el-icon-notebook-2"></i>
          <span style="margin-left: 10px">{{ scope.row.description}}</span>
        </template>
      </el-table-column>

      <el-table-column label="Operation">
        <template slot-scope="scope">
          <el-button size="mini" icon="el-icon-edit" @click="clickUpdateClass(scope.$index, scope.row)">Edit</el-button>
          <el-button size="mini" type="danger" icon="el-icon-delete" @click="deleteClass(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        p_id: this.$route.query.p_id,
        name: this.$route.query.name,
        path: this.$route.query.path,
        total: this.$route.query.total,

        tableData: [],
        classNameList: [],
        classColorList: [],

        addLabelVisible: false,
        addLabelName: '',
        addLabelColor: '',
        addLabelDes: '',

        rLabelVisible: false,
        rLabelName: '',
        rLabelColor: '',
        rLabelDes: '',
        rRow: null,

      };
    },
    methods: {
      fetch_class() {
        let url_data={
          p_id: this.p_id
        };
        this.$axios.get('/api/fetch_class', {params: url_data}).then(response => {
          this.tableData = response.data['data'];
          this.classNameList = [];
          this.classColorList = [];
          for(let i = 0; i < this.tableData.length; i++){
            this.classNameList.push(this.tableData[i]['label']);
            this.classColorList.push(this.tableData[i]['color']);
          }
        }).catch(err => {
          this.$notify.error({title: 'Error', message: err});
        });
      },

      addClassLabel(){
        this.addLabelName = this.addLabelName.trim();
        this.addLabelName = this.addLabelName.toLowerCase();
        this.addLabelName = this.addLabelName.charAt(0).toUpperCase() + this.addLabelName.slice(1);
        this.addLabelColor = this.addLabelColor.toUpperCase();
        this.addLabelDes = this.addLabelDes.trim();
        if(this.addLabelName === '' || this.addLabelColor === null || this.addLabelColor === ''){
          this.$notify({
            title: 'Warning',
            message: 'Input is empty.',
            type: 'warning'
          });
        }else if(this.addLabelName.length > 10) {
          this.$notify({
            title: 'Warning',
            message: 'Too Long',
            type: 'warning'
          });
        }else if(this.classNameList.indexOf(this.addLabelName) > -1 || this.classColorList.indexOf(this.addLabelColor) > -1){
          this.$notify({
            title: 'Warning',
            message: 'Class or color has existed!',
            type: 'warning'
          });
        }else{
          let url_data = new FormData();
          url_data.append('addLabelName', this.addLabelName);
          url_data.append('addLabelColor', this.addLabelColor);
          url_data.append('addLabelDes', this.addLabelDes)
          url_data.append('p_id', this.p_id)
          this.$axios.post('/api/add_class', url_data).then(response => {
            this.$notify({title: 'Success', message: 'Added successfully', type: 'success'});
            this.fetch_class();
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
          });
          this.addLabelVisible = false;
          this.addLabelName = '';
          this.addLabelColor = '';
          this.addLabelDes = '';
        }
      },

      deleteClass(index, row){
        this.$confirm('Delete this class, continue?', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          let url_data={
            c_id: row['c_id'],
          };
          this.$axios.delete('/api/delete_class', {params: url_data}).then(response => {
            this.$notify({title: 'Success', message: 'Deleted successfully', type: 'success'});
            this.fetch_class();
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
          });
        }).catch(() => {});
      },

      clickUpdateClass(index, row){
        this.rLabelName = row['label'];
        this.rLabelColor = row['color'];
        this.rLabelDes = row['description'];
        this.rRow = row;
        this.rLabelVisible = true;
      },

      updateClassLabel() {
        let tmpNameList = [].concat(this.classNameList);
        let tmpColorList = [].concat(this.classColorList);
        tmpNameList.remove(this.rRow['label']);
        tmpColorList.remove(this.rRow['color']);

        this.rLabelName = this.rLabelName.trim();
        this.rLabelName = this.rLabelName.toLowerCase();
        this.rLabelName = this.rLabelName.charAt(0).toUpperCase() + this.rLabelName.slice(1);
        this.rLabelColor = this.rLabelColor.toUpperCase();
        this.rLabelDes = this.rLabelDes.trim();
        if(this.rLabelName === '' || this.rLabelColor === null || this.rLabelColor === ''){
          this.$notify({title: 'Warning', message: 'Input is empty.', type: 'warning'});
        }else if(this.addLabelName.length > 10) {
          this.$notify({title: 'Warning', message: 'Too Long', type: 'warning'});
        }else if(tmpNameList.indexOf(this.rLabelName) > -1 || tmpColorList.indexOf(this.rLabelColor) > -1){
          this.$notify({title: 'Warning', message: 'Class or color has existed!', type: 'warning'});
        }else{
          let url_data = new FormData();
          url_data.append('rLabelName', this.rLabelName);
          url_data.append('rLabelColor', this.rLabelColor);
          url_data.append('rLabelDes', this.rLabelDes)
          url_data.append('c_id', this.rRow['c_id'])
          this.$axios.put('/api/update_class', url_data).then(response => {
            this.$notify({title: 'Success', message: 'Updated successfully', type: 'success'});
            this.fetch_class();
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
          });
          this.rLabelVisible = false;
          this.rLabelName = '';
          this.rLabelColor = '';
          this.rLabelDes = '';
        }
      },

      back2project(){
        this.$router.push("/home/project_manage");
      },

      tagFile() {
        this.$router.push({path: '/home/work_table',
          query: {p_id: this.$route.query.p_id, name: this.$route.query.name, path: this.$route.query.path, total: this.$route.query.total}});
      },

    },

    created() {
      this.fetch_class();
    },
  };

  Array.prototype.remove = function(val) {
    let index = this.indexOf(val);
    if (index > -1) {
      this.splice(index, 1);
    }
  };

</script>

<style scoped>

</style>
