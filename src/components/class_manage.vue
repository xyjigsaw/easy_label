<template>
  <div>
    <el-row>
      <el-col :span="12">
        <div class="grid-content bg-purple">
          <el-button type="primary" icon="el-icon-plus" @click="addLabelVisible = true">Add Class</el-button>
        </div>
      </el-col>
      <el-col :span="12"><div class="grid-content bg-purple-light"></div></el-col>
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

    <el-table :data="tableData" style="width: 100%">
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
          <el-button size="mini" type="danger" @click="deleteClass(scope.$index, scope.row)">Delete</el-button>
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

        tableData: [],
        classNameList: [],
        classColorList: [],

        addLabelVisible: false,
        addLabelName: '',
        addLabelColor: '',
        addLabelDes: '',

      };
    },
    methods: {
      fetch_class() {
        let url_data={
          p_id: this.p_id,
        };
        this.$axios.post('/api/fetch_class', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.tableData = response.data['data'];
            this.classNameList = [];
            this.classColorList = [];
            for(let i = 0; i < this.tableData.length; i++){
              this.classNameList.push(this.tableData[i]['label']);
              this.classColorList.push(this.tableData[i]['color']);
            }

          }
        }).catch(err => {
          this.$notify.error({
            title: 'Error',
            message: err
          });
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
          let url_data={
            addLabelName: this.addLabelName,
            addLabelColor: this.addLabelColor,
            addLabelDes: this.addLabelDes,
            p_id: this.p_id,
          };
          this.$axios.post('/api/add_class', url_data).then(response => {
            if (response.data['message'] === 'success') {
              this.$notify({
                title: 'Success',
                message: 'Class submitted successfully',
                type: 'success'
              });
              this.fetch_class();
            }else{
              this.$notify.error({
                title: 'Error',
                message: 'Unknown error'
              });
            }
          }).catch(err => {
            this.$notify.error({
              title: 'Error',
              message: err
            });
          });
          this.addLabelVisible = false;
          this.addLabelName = '';
          this.addLabelColor = '';
          this.addLabelDes = '';
        }
      },

      deleteClass(index, row){
        let url_data={
          c_id: row['c_id'],
        };
        this.$axios.post('/api/delete_class', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.$notify({
              title: 'Success',
              message: 'Deleted successfully',
              type: 'success'
            });
            this.fetch_class();
          }
        }).catch(err => {
          this.$notify.error({
            title: 'Error',
            message: err
          });
        });
      }
    },

    created() {
      this.fetch_class();
    },
  };
</script>

<style scoped>

</style>
