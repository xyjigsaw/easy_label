<template>
  <div>
    <el-container>
    <el-main>
      <div class="operation">
        <el-row>
          <el-col :span="12">
            <el-input v-model="paper_id" placeholder="input paper id or choose id in id-table"></el-input>
          </el-col>
          <el-col :span="5">
            <el-button type="primary" plain @click="get_paper_by_id(paper_id)">Search</el-button>
          </el-col>
          <el-col :span="5">
            <el-button type="primary" plain @click="show_id_table = !show_id_table">Show ID</el-button>
          </el-col>
        </el-row>
      </div>
      <br>
      <div class="tables">
        <el-table
          :data="tableData.filter(data => !tableSearch || data.res_entity.toLowerCase().includes(tableSearch.toLowerCase()))"
          :row-class-name="tableRowClassName"
          v-loading="loading_detail"
          :row-style="{height:'20px'}"
          element-loading-text="Loading"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)">
          <el-table-column
            prop="paper_id"
            label="paper_id"
            sortable>
          </el-table-column>
          <el-table-column
            prop="question"
            label="question"
            sortable>
          </el-table-column>
          <el-table-column
            prop="origin_res"
            label="origin_res"
            width="400">
          </el-table-column>
          <el-table-column
            prop="res_entity"
            label="res_entity"
            sortable>
          </el-table-column>
          <el-table-column
            prop="entity_name"
            label="entity_name"
            sortable>
          </el-table-column>
          <el-table-column
            prop="entity_description"
            label="entity_description"
            :show-tooltip-when-overflow="true"
            sortable>
          </el-table-column>
          <el-table-column label="operation" width="230">
            <template slot="header" slot-scope="scope">
              <el-input
                v-model="tableSearch"
                size="mini"
                placeholder="Search By Entity id"/>
            </template>
            <template slot-scope="scope">
              <el-row :gutter="10">
                <el-col :span="5">
                  <el-button
                    size="small"
                    type="danger"
                    icon="el-icon-close"
                    plain
                    @click="handleRow(scope.$index, scope.row, '0')"></el-button>
                </el-col>
                <el-col :span="5">
                  <el-button
                    size="small"
                    type="success"
                    icon="el-icon-check"
                    plain
                    @click="handleRow(scope.$index, scope.row, '1')"></el-button>
                </el-col>
              </el-row>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-main>

    <el-aside v-show="!show_id_table" width="300px" style="height: 1000px;background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px 5px 5px 0;">
      <el-table
        :data="all_paper_id"
        v-loading="loading_detail"
        element-loading-text="Loading"
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)">
        style="width: 100%">
        <el-table-column
          prop="paper_id"
          label="paper_id"
          width="120"
          sortable>
        </el-table-column>
        <el-table-column
          prop="total"
          label="total"
          sortable>
        </el-table-column>

        <el-table-column label="GO">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              plain
              @click="get_paper_by_id(scope.row['paper_id'])">GO</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-aside>
    </el-container>
  </div>
</template>

<script>
import Vue from "vue";

export default {
  name: "qa_ner",
  data() {
    return {
      all_paper_id: [],
      dpaqn_id: '',
      paper_id: '',
      tableData: [],
      tableSearch: '',
      show_id_table: true,
      loading_detail: false,
    }
  },
  created() {
    this.get_all_paper_id();
  },

  methods: {
    get_all_paper_id(){
      this.loading_detail = true;
      this.$axios.get('/api/fetch_all_paper_id').then(response => {
        this.all_paper_id = response.data['data'];
        this.loading_detail = false;
      }).catch(err => {
        this.$notify.error({title: 'Error', message: err});
      });
    },

    get_paper_by_id(pid){
      let url_data={
        paper_id: pid
      };
      this.loading_detail = true;
      this.$axios.get('/api/fetch_dqa_paper', {params: url_data}).then(response => {
        this.tableData = response.data['data'];
        console.log(this.tableData);
        this.loading_detail = false;
      }).catch(err => {
        this.$notify.error({title: 'Error', message: err});
      });
    },

    handleRow(index, row, flag){
      row['mark'] = flag
      console.log(row);
      let url_data = new FormData();
      url_data.append('dpaqn_id', row['dpaqn_id']);
      url_data.append('mark', row['mark']);
      this.$axios.put('/api/update_dqa_mark', url_data).then(response => {
        this.$notify({title: 'Success', message: 'Submitted successfully', type: 'success'});
      }).catch(err => {
        this.$notify.error({title: 'Error', message: err});
      });
    },

    tableRowClassName({row, rowIndex}) {
      console.log(row)
      if (row['mark'] === "0") {
        return 'warning-row';
      } else if (row['mark'] === "1") {
        return 'success-row';
      }
      return 'null-row';
    },


    back2home(){
      this.$confirm('Are you sure to leave?', 'Warning', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        this.$router.push("/home/dashboard");
      }).catch(() => {
      });
    },


  },


}
</script>

<style>
.el-table .warning-row {
  background: #fde6f4;
}

.el-table .success-row {
  background: #f0f9eb;
}

.el-table .null-row {
  background: #ffffff;
}
</style>
