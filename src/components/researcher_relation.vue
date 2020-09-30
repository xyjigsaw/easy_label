<template>
  <div class="hello">
    <el-container>
    <el-main style="padding: 0;">
      <h1>{{ msg }}</h1>
      <el-row :gutter="12" type="flex" justify="center">
        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-button type="success" plain @click="rand_search">Random</el-button>
        </div></el-col>
        <el-col :span="1" v-if="showTable && is_edit !== true"><div class="grid-content bg-purple">
          <el-button type="primary" icon="el-icon-edit" circle @click="edit"></el-button>
          <p style="font-size: 8px; color: #409EFF; text-align: center">Edit</p>
        </div></el-col>

        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
          <p style="font-size: 8px; color: #67C23A; text-align: center">Save</p>
        </div></el-col>
      </el-row>

      <div class="labelGroup">
        <el-button type="info" size="large" plain>Event: {{ cur_rel_ls['event']['word'] }}</el-button>
        <el-button type="info" size="medium" plain>Time: {{ cur_rel_ls['time']['word'] }}</el-button>
        <el-button type="info" size="medium" plain>Affiliation: {{ cur_rel_ls['affiliation']['word'] }}</el-button>
        <el-button type="primary" round @click="justAdd">Add</el-button>
        <el-button icon="el-icon-rank" @click="change_pos" style="padding: 10px; margin: 10px;"></el-button>
      </div>
      <br>
      <div id="all_info">
        <span id="profile_all"></span>
        <div id="detail_info" @click='spanEvent'></div>
      </div>


      <div v-if="showTable && is_edit !== true">
        <!-- 分页器 -->
        <div class="block" style="margin-top:15px;">
          <el-pagination align='center' @current-change="handleCurrentChange"
                         :current-page="currentPage"
                         :page-size="pageSize"
                         layout="total, prev, pager, next"
                         :total="tableData.length">
          </el-pagination>
          <p>共47685条学者数据，当前显示{{ total }}条</p>
        </div>
      </div>

      <div v-if="showTable && is_edit === true">
        <el-row :gutter="6" type="flex" justify="center">
          <el-col :span="2">
            <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
            <p style="font-size: 8px; color: #67C23A; text-align: center">Save</p>
          </el-col>
        </el-row>
      </div>

    </el-main>


    <el-aside width="450px" style="height: 1000px;background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px 5px 5px 0;">
      <el-table
        class="tableClass"
        :data="relTable"
        stripe
        style="width: 100%; text-align: center; font-size: 5px;"
        :row-style="{height:'8px'}" :cell-style="{padding:'5px 0'}">
        <el-table-column
          type="index"
          label="ID"
          width="40">
        </el-table-column>
        <el-table-column
          prop="event.word"
          label="Event"
          width="100">
        </el-table-column>
        <el-table-column
          prop="time.word"
          label="Time"
          width="100">
        </el-table-column>
        <el-table-column
          prop="affiliation.word"
          label="Affiliation"
          width="100">
        </el-table-column>
        <el-table-column
          label="Edit"
          width="70">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="deleteRow(scope.$index, relTable)"
              type="text"
              size="small">
              remove
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-aside>
    </el-container>
  </div>
</template>

<script>
import Vue from 'vue'
export default {
  name: 'Research',
  data () {
    return {
      msg: 'Researcher NER',

      input_name: '',
      input_affiliation: '',
      input_limit: '',

      showTable: false,
      tableData: null,
      currentPage: 0,
      total: 0,
      pageSize: 1,

      tableData_save: null,
      currentPage_save: null,
      total_save: null,

      entityClass: [],
      entityColor: [],

      is_edit: false,
      current_id: null,
      current_data: null,

      cur_words: [],

      cur_rel_ls: {'event': '', 'time': '', 'affiliation': ''},
      cur_type_ls: [],
      relTable: [],

    }
  },

  created(){
    this.rand_search();
  },
  methods: {
    rand_search(){
      this.search(1);
      this.msg = 'Researcher Relation Mark';
      this.is_edit = true;
      this.currentPage_save = this.currentPage;
      this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
      this.cur_type_ls = [];
    },

    search(is_rand_search) {
      if(is_rand_search === 0){
        if(this.input_name === '' && this.input_affiliation === ''){
          return;
        }
        if(this.input_limit===''){
          this.input_limit = 10;
        }
      }else{
        this.input_limit = 1;
        this.input_name = '';
        this.input_affiliation = '';
      }

      let url_data={
        name: this.input_name.trim(),
        affiliation: this.input_affiliation.trim(),
        limit: this.input_limit,
        rand_search: is_rand_search,
      };

      let tagged_data = [];
      this.$axios.post('/api/research_post', url_data).then(response => {
        if (response.data) {

          this.entityClass = [];
          this.entityClass = [];

          for(let i = 0; i < response.data['entity_class'].length; i++){
            this.entityClass.push(response.data['entity_class'][i]['label']);
            this.entityColor.push(response.data['entity_class'][i]['color']);
          }

          //for content
          this.total = response.data['data'].length;
          for(let i = 0; i < response.data['data'].length; i++){
            let origin_content = response.data['data'][i]['Content'];
            let cur_content = response.data['data'][i]['Content'];
            let entity_str = response.data['data'][i]['Entity_list'];
            let entity_str_ls = eval(entity_str);
            cur_content = this.genContent(entity_str_ls, cur_content);
            tagged_data.push({'Content': cur_content, 'id': response.data['data'][i]['id'],
              'Affiliation': response.data['data'][i]['Affiliation'], 'AuthorName': response.data['data'][i]['AuthorName'],
              'origin_content': origin_content, 'Entity_list': response.data['data'][i]['Entity_list'], 'Mark_relation': eval(response.data['data'][i]['Mark_relation'])});
          }
          this.tableData = tagged_data;
          this.showTable = true;

          this.tableData_save = this.tableData;
          this.currentPage_save = this.currentPage;
          this.total_save = this.total;

          this.handleCurrentChange(1); //page:0
          //console.log(this.tableData);
        }
      }).catch(err => {
        this.$message.error('Sorry, not found in database. The Result is empty.');
        this.showTable = false;
        this.input_name = '';
        this.input_affiliation = '';
        this.input_limit = '';
      });
    },

    genContent(entity_str_ls, cur_content){
      entity_str_ls.sort(sort_entity);
      let split_ls = [];
      for(let j = 0; j < entity_str_ls.length; j++){
        let split_json = entity_str_ls[j];
        let start_str = split_json['start'];
        let end_str = split_json['end'];
        let type_str = split_json['type'];
        split_ls.push([type_str, parseInt(start_str), parseInt(end_str)]);
      }
      for(let j = split_ls.length - 1; j >= 0; j--){
        let [type, startNum, endNum] = split_ls[j];
        for(let k=0; k < this.entityClass.length; k++){
          if(type===this.entityClass[k]){
            cur_content = cur_content.substring(0, startNum) + '<span class="' + type + '" style="color:' + this.entityColor[k]+
              '; font-weight: bold;  cursor: pointer;" data-startNum="' + startNum + '" data-endNum="' + endNum + '">'
              + cur_content.substring(startNum, endNum) + '</span>' + cur_content.substring(endNum)
          }
        }
      }
      return cur_content;
    },

    //page jumper
    handleCurrentChange(val) {
      this.currentPage = val;
      this.relTable = this.tableData[this.currentPage - 1]['Mark_relation'];
      console.log(this.tableData[this.currentPage - 1]);

      this.current_id = this.tableData[this.currentPage - 1]['id'];
      this.current_data = this.tableData[this.currentPage - 1];
      let el = eval(this.current_data['Entity_list']);
      for(let w = 0; w < el.length; w++){
        this.cur_words.push(el[w]['word']);
      }
      document.getElementById("profile_all").innerHTML="<span class='profile'>" + this.tableData[this.currentPage - 1]['id'] + "</span>\n" +
        "<span class='profile'>" + this.tableData[this.currentPage - 1]['AuthorName'] + "</span>\n" +
        "<span class='profile'>" + this.tableData[this.currentPage - 1]['Affiliation'] +
        "</span>";
      document.getElementById("detail_info").innerHTML="<div style=\"box-shadow: 0 0 2px #b1b1b1; margin: 10px; padding:20px; border-radius: 5px; " +
        "line-height: 30px;\">" + this.tableData[this.currentPage - 1]['Content'] + "</div>";

    },

    edit(){
      if(this.tableData != null){
        this.msg = 'Edit Mode';
        this.is_edit = true;
        this.currentPage_save = this.currentPage;
      }else{
      }
    },

    save(){
      this.$confirm('It cannot be changed after submission.', 'Confirm', {
        confirmButtonText: 'Save',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        let url_data={
          e_id: this.current_id,
          res: {'Relation_list': this.relTable},
        };
        this.$axios.post('/api/research_rel_submit', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.$message({
              message: 'Submit successfully!',
              type: 'success'
            });
            this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
            this.cur_type_ls = [];
          }else{
            this.$message.error('Submit failed!');
          }
        }).catch(err => {
          this.$message.error('Submit failed!\n' + err);
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Nothing happened!'
        });
      });
    },

    exit(){
      //location.reload();
      this.msg = 'Researcher NER';
      this.tableData = this.tableData_save;
      this.currentPage = this.currentPage_save;
      this.total = this.total_save;
      this.is_edit = false;
      this.handleCurrentChange(this.currentPage);
    },

    spanEvent(){
      if(this.is_edit){
        let spanObj=document.elementFromPoint(event.clientX, event.clientY);
        let spanClass = spanObj.getAttribute("class");
        let startNum = parseInt(spanObj.getAttribute("data-startNum"));
        let endNum = parseInt(spanObj.getAttribute("data-endNum"));
        if(!isNaN(startNum)){
          console.log('Click Span: ' + spanObj.innerHTML + ' ' + startNum + ' ' + endNum + ' ' + spanClass);
          //spanObj.style.backgroundColor=this.entityColor[this.entityClass.indexOf(spanClass)];
          //spanObj.style.color="white";
          //spanObj.style.padding="2px 4px 2px 4px";
          //spanObj.style.borderRadius="4px";
          if(spanClass === 'Time'){
            this.cur_rel_ls['time'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass};
          }else if(spanClass === 'Institut'){
            this.cur_rel_ls['affiliation'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass};
          }else{
            this.cur_rel_ls['event'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass};
          }
          if(this.cur_type_ls.indexOf(spanClass) === -1){
            if(spanClass === 'Time' || spanClass === 'Institut'){
              this.cur_type_ls.push(spanClass);
            }else{
              if(this.cur_type_ls.indexOf('others') === -1){
                this.cur_type_ls.push('others');
              }
            }

            if(this.cur_type_ls.length === 3){
              this.relTable.push({'event': this.cur_rel_ls['event'], 'time': this.cur_rel_ls['time'], 'affiliation': this.cur_rel_ls['affiliation']});
              this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
              this.cur_type_ls = [];
              console.log(this.relTable);
            }
          }
        }
      }
    },

    click_check(){

    },

    change_pos() {
      let obj = document.getElementsByClassName("labelGroup");
      if (obj.item(0).style.position === 'fixed') {
        obj.item(0).style.position = 'static';
      } else if (obj.item(0).style.position === 'static') {
        obj.item(0).style.position = 'fixed';
      }
    },

    deleteRow(index, rows) {
      rows.splice(index, 1);
    },

    justAdd(){
      this.relTable.push({'event': this.cur_rel_ls['event'], 'time': this.cur_rel_ls['time'], 'affiliation': this.cur_rel_ls['affiliation']});
      this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
      this.cur_type_ls = [];
    }

  }
}

function sort_entity(a, b){
  return a.start - b.start;
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style>
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>

<style>
.el-checkbox__input.is-checked+.el-checkbox__label{
  color: #FFF;
}

.profile{
  background-color: rgba(64,158,255,.1);
  color: #409eff;
  border-radius: 4px;
  box-sizing: border-box;
  border: 1px solid rgba(64,158,255,.2);
  padding: 0 10px;
  line-height: 30px;
  font-size: 20px;
}
</style>
