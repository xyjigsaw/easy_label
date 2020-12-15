
<template>
  <div class="hello">
    <el-container>
    <el-main>
      <h1>{{ msg }}</h1>
      <el-row :gutter="12" type="flex" justify="center">
        <el-col :span="3" v-if="is_edit !== true"><div class="grid-content bg-purple">
          <el-input v-model="input_name" placeholder="name"></el-input>
        </div></el-col>
        <el-col :span="3" v-if="is_edit !== true"><div class="grid-content bg-purple">
          <el-input v-model="input_affiliation" placeholder="affiliation"></el-input>
        </div></el-col>
        <el-col :span="2" v-if="is_edit !== true"><div class="grid-content bg-purple">
          <el-input v-model="input_limit" placeholder="limit(optional)"></el-input>
        </div></el-col>
        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-input v-model="input_id" placeholder="fund id"></el-input>
        </div></el-col>
        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-button type="primary" plain @click="search_by_id_portal">Search</el-button>
        </div></el-col>
        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-button type="success" plain @click="rand_search">Random</el-button>
        </div></el-col>
        <el-col :span="1" v-if="showTable && is_edit !== true"><div class="grid-content bg-purple">
          <el-button type="warning" icon="el-icon-plus" circle @click="addLabelVisible = true"></el-button>
          <p style="font-size: 8px; color: #E6A23C; text-align: center">Add Class</p>
        </div></el-col>
        <el-col :span="1" v-if="showTable && is_edit !== true"><div class="grid-content bg-purple">
          <el-button type="primary" icon="el-icon-edit" circle @click="edit"></el-button>
          <p style="font-size: 8px; color: #409EFF; text-align: center">Edit</p>
        </div></el-col>


        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-button icon="el-icon-search" circle @click="see_all"></el-button>
          <p style="font-size: 8px; color: #606266; text-align: center">Preview</p>
        </div></el-col>
        <el-col :span="2" v-if="showTable && is_edit === true"><div class="grid-content bg-purple">
          <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
          <p style="font-size: 8px; color: #67C23A; text-align: center">Save</p>
        </div></el-col>
        <el-col :span="2" v-if="showTable && is_edit !== true"><div class="grid-content bg-purple">
          <el-button type="info" icon="el-icon-right" circle @click="exit"></el-button>
          <p style="font-size: 8px; color: #909399; text-align: center">Exit</p>
        </div></el-col>

        <el-col :span="3" style="margin-top: 10px;"><div class="grid-content bg-purple">
          <el-switch
            v-model="entity_rel"
            ctive-color="#67C23A"
            inactive-color="#ff4949"
            active-text="entity"
            inactive-text="relation">
          </el-switch>
        </div></el-col>

        <el-col :span="3" style="margin-top: 10px;"><div class="grid-content bg-purple">
          <el-switch
            v-model="data_version"
            ctive-color="#67C23A"
            inactive-color="#ff4949"
            active-text="baike"
            inactive-text="edu"
            @change="change_version">
          </el-switch>
        </div></el-col>

        <el-col :span="3" style="margin-top: 10px;"><div class="grid-content bg-purple">
          <el-switch
            v-model="autoMarkSelection"
            active-color="#13ce66"
            inactive-color="#dddddd"
            active-text="AUTO MARK">
          </el-switch>
        </div></el-col>
      </el-row>


      <el-dialog title="Add Class Label" :visible.sync="addLabelVisible" width="30%">

        <el-form>
          <el-form-item label="Input Class Name">
            <el-input v-model="addLabelName" autocomplete="off"></el-input>
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


      <div id="class_ls" v-show="is_edit !== true && entity_rel">
      </div>

      <div class="labelGroup" v-show="entity_rel != true">
        <el-button type="info" size="large" plain>Event: {{ cur_rel_ls['event']['word'] }}</el-button>
        <el-button type="info" size="medium" plain>Time: {{ cur_rel_ls['time']['word'] }}</el-button>
        <el-button type="info" size="medium" plain>Affiliation: {{ cur_rel_ls['affiliation']['word'] }}</el-button>
        <el-button type="primary" round @click="justAdd">Add</el-button>
      </div>



      <br>
      <div id="all_info"
           v-loading="loading_detail"
           element-loading-text="Loading"
           element-loading-spinner="el-icon-loading"
           element-loading-background="rgba(0, 0, 0, 0.8)">
        <span id="profile_all"></span>
        <div id="detail_info" @mouseup='selectText' @click='spanEvent'></div>
      </div>


      <div v-if="showTable && is_edit !== true">
        <!-- 分页器 -->
        <div class="block" style="margin-top:15px;">
          <el-switch @change="click_check" style="display:flex; float: left; margin: auto; padding: 0 0 0 10px;" v-model="switch_color" active-color="#13ce66" inactive-color="#409EFF"> </el-switch>
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
            <el-button icon="el-icon-search" circle @click="see_all"></el-button>
            <p style="font-size: 8px; color: #606266; text-align: center">Preview</p>
          </el-col>
          <el-col :span="2">
            <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
            <p style="font-size: 8px; color: #67C23A; text-align: center">Save</p>
          </el-col>
        </el-row>
      </div>

    </el-main>
    <el-aside v-show="!entity_rel" width="450px" style="height: 1000px;background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px 5px 5px 0;">
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
      first_mount: true,

      input_name: '',
      input_affiliation: '',
      input_limit: '',
      input_id: '',

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
      checkList: [],
      check_max: 100,

      switch_color: false,

      //for editing
      is_edit: false,
      current_id: null,
      current_data: null,

      //add class
      template_string: '',
      labelIns: null,
      addLabelName: '',
      addLabelColor: '',
      addLabelVisible: false,

      cur_words: [],

      cur_rel_ls: {'event': '', 'time': '', 'affiliation': ''},
      cur_type_ls: [],
      relTable: [],

      entity_rel: true,
      data_version: true,

      loading_detail: false,

      autoMarkSelection: true,
    }
  },

  created(){
    this.rand_search();
    let arr = [];
    let that = this;
    document.onkeydown = function(e) {
      let digitalShift = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+']
      if(arr.length > 0) { // a-z按键长按去重
        if(arr.indexOf(e.key.toLowerCase()) >= 0) {
          return
        }
      }
      arr.push(e.key.toLowerCase())
      this.keydown = arr.join('+');
      if(digitalShift.indexOf(this.keydown[this.keydown.length - 1]) > -1){
        let keyPos = digitalShift.indexOf(this.keydown[this.keydown.length - 1]);
        this.keydown = '';
        if(keyPos <= that.entityClass.length){
          this.checkList = [that.entityClass[keyPos]];
          that.labelIns.checkList = this.checkList;
          that.labelIns.click_check();
          this.keydown = '';
          that.$notify({title: that.entityClass[keyPos], message: 'You have switched to class ' + that.entityClass[keyPos] + '.', type: 'success'
          });
        }
      }
    }
    document.onkeyup = function (e) {
      arr.splice(arr.indexOf( e.key.toLowerCase() ),1);
      this.keydown = arr.join('+');
    }
    this.keydown = '';
  },
  methods: {
    search_by_id_portal(){
      this.loading_detail = true;
      this.search_by_id()
      this.msg = 'Researcher Edit Mode';
      this.is_edit = true;
      this.switch_color = false;
      this.checkList = [];
      this.check_max = 1;
      this.currentPage_save = this.currentPage;
      this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
      this.cur_type_ls = [];
      if(this.first_mount){

      }else{
        this.labelIns.checkList = this.checkList;
        this.labelIns.check_max = this.check_max;
      }
    },
    rand_search(){
      this.loading_detail = true;
      this.search(1);
      this.msg = 'Researcher Edit Mode';
      this.is_edit = true;
      this.switch_color = false;
      this.checkList = [];
      this.check_max = 1;
      this.currentPage_save = this.currentPage;
      this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
      this.cur_type_ls = [];
      if(this.first_mount){

      }else{
        this.labelIns.checkList = this.checkList;
        this.labelIns.check_max = this.check_max;
      }
    },
    search(is_rand_search) {
      // 由于 main.js 里定义了每个请求前缀，此处的 / 即为 /api/，
      // 经过 vue.config.js 配置文件的代理设置，会自动转为 http://127.0.0.1:8000，从而解决跨域问题
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
        version: this.data_version ? "0" : "1",
      };

      let tagged_data = [];
      this.$axios.post('/api/research_post', url_data).then(response => {
        if (response.data) {
          if(this.first_mount){
            //for entity class
            this.entityClass = [];
            this.entityClass = [];
            this.checkList = [];
            this.template_string = '';
            for(let i = 0; i < response.data['entity_class'].length; i++){
              this.entityClass.push(response.data['entity_class'][i]['label']);
              this.entityColor.push(response.data['entity_class'][i]['color']);
              this.addClassLabelStr(response.data['entity_class'][i]['label'], response.data['entity_class'][i]['color'])
            }
            this.mount_labels(this.template_string, '#class_ls');
            this.first_mount = false;
          }else{
            this.labelIns.checkList = this.checkList;
            this.labelIns.check_max = this.check_max;
          }
          //for content
          this.total = response.data['data'].length;
          for(let i = 0; i < response.data['data'].length; i++){
            let origin_content = response.data['data'][i]['Content'];
            let cur_content = response.data['data'][i]['Content'];
            let entity_str = response.data['data'][i]['Entity_list'];
            let entity_str_ls = eval(entity_str);
            //let entity_str_ls = entity_str.split('|');
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
          this.relTable = this.tableData[0]['Mark_relation'];
          console.log(this.tableData[0]);
          this.handleCurrentChange(1); //page:0
          //console.log(this.tableData);
          this.loading_detail = false;
        }
      }).catch(err => {
        this.$message.error('Sorry, not found in database. The Result is empty.');
        this.showTable = false;
        this.input_name = '';
        this.input_affiliation = '';
        this.input_limit = '';
      });
    },

    search_by_id() {
      if(this.input_id===''){
        return ;
      }

      let url_data={
        fund_id: this.input_id.trim(),
        version: this.data_version ? "0" : "1",
      };
      let tagged_data = [];
      this.$axios.post('/api/research_post_by_id', url_data).then(response => {
        if (response.data) {
          if(this.first_mount){
            //for entity class
            this.entityClass = [];
            this.entityClass = [];
            this.checkList = [];
            this.template_string = '';
            for(let i = 0; i < response.data['entity_class'].length; i++){
              this.entityClass.push(response.data['entity_class'][i]['label']);
              this.entityColor.push(response.data['entity_class'][i]['color']);
              this.addClassLabelStr(response.data['entity_class'][i]['label'], response.data['entity_class'][i]['color'])
            }
            this.mount_labels(this.template_string, '#class_ls');
            this.first_mount = false;
          }else{
            this.labelIns.checkList = this.checkList;
            this.labelIns.check_max = this.check_max;
          }
          //for content
          this.total = response.data['data'].length;
          for(let i = 0; i < response.data['data'].length; i++){
            let origin_content = response.data['data'][i]['Content'];
            let cur_content = response.data['data'][i]['Content'];
            let entity_str = response.data['data'][i]['Entity_list'];
            let entity_str_ls = eval(entity_str);
            //let entity_str_ls = entity_str.split('|');
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
          this.relTable = this.tableData[0]['Mark_relation'];
          console.log(this.tableData[0]);
          this.handleCurrentChange(1); //page:0
          //console.log(this.tableData);
          this.loading_detail = false;
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
        //let split_json = strToJson(entity_str_ls[j]);
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
      this.click_check();
    },

    click_check(){
      //console.log(this.checkList);
      for(let i=0; i < this.entityClass.length; i++){
        let obj = document.getElementsByClassName(this.entityClass[i]);
        if(this.checkList.indexOf(this.entityClass[i]) > -1){
          //obj.style.color= entityColor[i];
          for(let j=0; j<obj.length; j++){
            obj.item(j).style.color=this.entityColor[i];
            obj.item(j).style.fontWeight="bold";
            if(!this.switch_color){
              obj.item(j).style.backgroundColor=this.entityColor[i];
              obj.item(j).style.color="white";
              obj.item(j).style.padding="2px 4px 2px 4px";
              obj.item(j).style.borderRadius="4px";
            }else{
              obj.item(j).style.backgroundColor='transparent';
              obj.item(j).style.color=this.entityColor[i];
              obj.item(j).style.padding="0";
              obj.item(j).style.borderRadius="0px";
              obj.item(j).style.cursor="default";
            }
          }
        }else{
          if(!this.is_edit){
            for(let j=0; j<obj.length; j++){
              obj.item(j).style.color="black";
              obj.item(j).style.fontWeight="normal";
              obj.item(j).style.backgroundColor='transparent';
              obj.item(j).style.padding="0";
              obj.item(j).style.borderRadius="0px";
              obj.item(j).style.cursor="default";
            }
          }else{
            for(let j=0; j<obj.length; j++){
              obj.item(j).style.backgroundColor='transparent';
              obj.item(j).style.color=this.entityColor[i];
              obj.item(j).style.fontWeight="bold";
              obj.item(j).style.padding="2px 4px 2px 4px";
            }
          }

        }
      }

    },

    edit(){
      if(this.tableData != null){
        this.msg = 'Edit Mode';
        this.is_edit = true;
        this.switch_color = false;
        this.checkList = [];
        this.check_max = 1;
        this.currentPage_save = this.currentPage;
        this.labelIns.checkList = this.checkList;
        this.labelIns.check_max = this.check_max;
        this.see_all();
      }else{
        return;
      }
    },

    see_all(){
      this.checkList = this.entityClass;
      this.labelIns.checkList = this.checkList;
      this.click_check();
      this.checkList = [];
      this.labelIns.checkList = this.checkList;
    },

    save(){
      //this.see_all();
      this.$confirm('It cannot be changed after submission.', 'Confirm', {
        confirmButtonText: 'Save',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        let url_data={
          e_id: this.current_id,
          res: this.current_data,
          version: this.data_version ? "0" : "1",
        };
        this.$axios.post('/api/research_submit', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.tableData_save[this.currentPage_save - 1] = this.tableData[0];
            this.$message({
              message: 'Submit successfully for entity list!',
              type: 'success'
            });
          }else{
            this.$message.error('Submit failed for entity list!');
          }
        }).catch(err => {
          this.$message.error('Submit failed for entity list!\n' + err);
        });

        let url_data2={
          e_id: this.current_id,
          res: {'Relation_list': this.relTable},
          version: this.data_version ? "0" : "1",
        };
        this.$axios.post('/api/research_rel_submit', url_data2).then(response => {
          if (response.data['message'] === 'success') {
            this.$message({
              message: 'Submit successfully for relation list!',
              type: 'success'
            });
            this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
            this.cur_type_ls = [];
          }else{
            this.$message.error('Submit failed for relation list!');
          }
        }).catch(err => {
          this.$message.error('Submit failed for relation list!\n' + err);
        });
        this.exit();

      }).catch(() => {
      });
    },

    exit(){
      //location.reload();
      this.msg = 'Researcher NER';
      //this.tableData = this.tableData_save;
      //this.currentPage = this.currentPage_save;
      this.total = this.total_save;
      // this.is_edit = false;
      this.checkList = this.entityClass;
      this.labelIns.check_max = 100;
      this.labelIns.checkList = this.entityClass;
      this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
      this.cur_type_ls = [];

      this.handleCurrentChange(this.currentPage);

    },

    selectText(){
      if(this.entity_rel){
        try{
          let selected=window.getSelection().toString();
          if(this.is_edit && selected!=null){
            let base = 0;
            let container = window.getSelection().getRangeAt(0).startContainer;
            while(container.previousSibling){
              base += container.previousSibling.textContent.length;
              container = container.previousSibling;
            }
            let anchorOffset = window.getSelection().anchorOffset;
            let focusOffset = window.getSelection().focusOffset;
            let start_num = Math.min(anchorOffset, focusOffset);
            let end_num = Math.max(anchorOffset, focusOffset);
            //console.log(this.current_data['Entity_list']);

            let r_cnt = count_r(this.current_data['origin_content'].substr(0, base + end_num + 1), this.cur_words);
            base += r_cnt;
            console.log('base: ' + base);
            console.log('r: ' + r_cnt);
            if(start_num < end_num && end_num - start_num === selected.length && this.checkList.length === 1){
              console.log('Selected text: ' + selected);
              let cur_content = this.current_data['origin_content'];
              let entity_str_ls = eval(this.current_data['Entity_list']);

              if(this.autoMarkSelection){
                if(selected.indexOf(' ') > -1) return;
                console.log('start', start_num, ' end: ', end_num)
                let marginChar = [',', '.', ':', ';', '?', '!', ' ', '(', ')', '>', '<', '"', '*', '%', '-', '_', '\n', '。']
                let selectedPosList = [];
                let tmpPos = 0;
                if(cur_content.indexOf(selected) < selected.length){
                  selectedPosList.push(cur_content.indexOf(selected));
                }
                while(tmpPos > -1){
                  tmpPos = cur_content.indexOf(selected, tmpPos + selected.length);
                  selectedPosList.push(tmpPos);
                }
                let allStartNum = [];
                for(let i = 0; i < entity_str_ls.length; i++){
                  allStartNum.push(entity_str_ls[i]['start']);
                }
                for(let i = 0; i < selectedPosList.length - 1; i++){
                  if(allStartNum.indexOf(selectedPosList[i]) === -1){
                    //if(marginChar.indexOf(cur_content[selectedPosList[i] - 1]) > -1 && marginChar.indexOf(cur_content[selectedPosList[i] + selected.length]) > -1 ||
                    //  selectedPosList[i] === 0 && marginChar.indexOf(cur_content[selectedPosList[i] + selected.length]) > -1){
                    //}

                    if(this.check_entity(entity_str_ls, selectedPosList[i], selectedPosList[i] +selected.length)){
                      entity_str_ls.push({'start': selectedPosList[i],
                        'end': selectedPosList[i] + selected.length, 'word': selected, 'type': this.checkList[0]});
                    }else{
                      console.log({'start': selectedPosList[i],
                        'end': selectedPosList[i] + selected.length, 'word': selected, 'type': this.checkList[0]});
                    }
                  }
                }
              }else{
                entity_str_ls.push({'start': base + start_num,
                  'end': base + end_num, 'word': selected, 'type': this.checkList[0]});
              }

              cur_content = this.genContent(entity_str_ls, cur_content);
              this.tableData = [{'Content': cur_content, 'id': this.current_id,
                'Affiliation': this.current_data['Affiliation'], 'AuthorName': this.current_data['AuthorName'],
                'origin_content': this.current_data['origin_content'], 'Entity_list': entity_str_ls}];
              this.showTable = true;
              this.handleCurrentChange(1); //page:0
            }else if(base === 0 && this.checkList.length === 1){
              return;
            }else{
              return;
            }
          }
        }catch(err){
          this.$message.error(err);
        }
      }

    },

    check_entity(entity_str_ls, start, end){
      for(let i = 0; i < entity_str_ls.length; i++){
        if(entity_str_ls[i]['start'] <= start && start < entity_str_ls[i]['end'] ||
          entity_str_ls[i]['start'] < end && end <= entity_str_ls[i]['end']){
          //console.log(entity_str_ls[i]['word'], end, entity_str_ls[i]['start'], entity_str_ls[i]['end'])
          return false;
        }
      }
      return true;
    },

    spanEvent(){
      if(this.is_edit){
        if(this.entity_rel){
          let spanObj=document.elementFromPoint(event.clientX, event.clientY);
          let spanClass = spanObj.getAttribute("class");
          if(this.checkList.length === 1 && spanClass === this.checkList[0]){
            let startNum = parseInt(spanObj.getAttribute("data-startNum"));
            let endNum = parseInt(spanObj.getAttribute("data-endNum"));
            console.log('Click Span: ' + spanObj.innerHTML + ' ' + startNum + ' ' + endNum);
            this.removeEntity(startNum, endNum, spanObj.innerHTML);
          }
        }else{
          let spanObj=document.elementFromPoint(event.clientX, event.clientY);
          let spanClass = spanObj.getAttribute("class");
          let startNum = parseInt(spanObj.getAttribute("data-startNum"));
          let endNum = parseInt(spanObj.getAttribute("data-endNum"));
          if(!isNaN(startNum)){
            console.log('Click Span: ' + spanObj.innerHTML + ' ' + startNum + ' ' + endNum + ' ' + spanClass);
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
      }
    },

    removeEntity(startNum, endNum, spanWord){
      let cur_content = this.current_data['origin_content'];
      let entity_str_ls = eval(this.current_data['Entity_list']);
      for(let i = entity_str_ls.length-1; i >= 0; i--){
        //if(entity_str_ls[i]['start'] === startNum && entity_str_ls[i]['end'] === endNum){
        //  entity_str_ls.splice(i,1);
        //}

        if(this.autoMarkSelection){
          if(entity_str_ls[i]['end'] - entity_str_ls[i]['start'] === endNum - startNum
            && entity_str_ls[i]['word'] === spanWord){
            entity_str_ls.splice(i,1);
          }
        }else{
          if(entity_str_ls[i]['start'] === startNum && entity_str_ls[i]['end'] === endNum){
            entity_str_ls.splice(i,1);
          }
        }
      }
      cur_content = this.genContent(entity_str_ls, cur_content);
      this.tableData = [{'Content': cur_content, 'id': this.current_id,
        'Affiliation': this.current_data['Affiliation'], 'AuthorName': this.current_data['AuthorName'],
        'origin_content': this.current_data['origin_content'], 'Entity_list': entity_str_ls}];
      this.showTable = true;
      this.handleCurrentChange(1); //page:0
    },

    addClassLabel(){
      this.addLabelName = this.addLabelName.trim();
      this.addLabelName = this.addLabelName.toLowerCase();
      this.addLabelName = this.addLabelName.charAt(0).toUpperCase() + this.addLabelName.slice(1);
      this.addLabelColor = this.addLabelColor.toUpperCase();
      if(this.addLabelName === '' || this.addLabelColor === null || this.addLabelColor === ''){
        this.$message({
          message: 'Input Error',
          type: 'warning'
        });
      }else if(this.addLabelName.length > 10) {
        this.$message({
          message: 'Too Long!',
          type: 'warning'
        });
      }else if(this.entityClass.indexOf(this.addLabelName) > -1 || this.entityColor.indexOf(this.entityColor) > -1){
        this.$message({
          message: 'Class or Color has existed!',
          type: 'warning'
        });
      }else{
        let url_data={
          addLabelName: this.addLabelName,
          addLabelColor: this.addLabelColor,
        };
        this.$axios.post('/api/research_class_submit', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.$message({
              message: 'Class submitted successfully',
              type: 'success'
            });
            setTimeout("window.location.reload()",1000);
          }else{
            this.$message.error('Submit failed!');
          }
        }).catch(err => {
          this.$message.error('Submit failed!\n' + err);
        });
      }
      this.addLabelVisible = false;
      this.addLabelName = '';
      this.addLabelColor = '';
    },

    addClassLabelStr(label, color){
      this.template_string +=
        '<el-checkbox label="' + label + '" style="padding:8px; border-radius:5px; background-color:' + color +
        ';font-weight: bold;"></el-checkbox>';
    },

    mount_labels(template_str, elementID){
      let that = this;
      let classLabel = Vue.extend({
        template: '<el-checkbox-group class="labelGroup" v-model="checkList" @change="click_check" :max="check_max" style="position: static;">' + template_str +
          '<el-button icon="el-icon-rank" @click="change_pos" style="padding: 10px; margin: 10px;"></el-button></el-switch></el-checkbox-group></el-checkbox-group>',
        data: function () {
          return {
            checkList: that.checkList,
            check_max: that.check_max,
          };
        },
        methods: {
          click_check(){
            that.checkList = this.checkList;
            that.check_max = this.check_max;
            that.click_check();
          },
          change_pos(){
            let obj = document.getElementsByClassName("labelGroup");
            if(obj.item(0).style.position === 'fixed'){
              obj.item(0).style.position='static';
            }else if(obj.item(0).style.position === 'static'){
              obj.item(0).style.position='fixed';
            }
          },
        }
      });
      this.labelIns = new classLabel();
      if(this.first_mount){
        this.labelIns.$mount(elementID);
      }else{
        this.labelIns.$forceUpdate();
      }
    },

    deleteRow(index, rows) {
      rows.splice(index, 1);
    },

    justAdd(){
      this.relTable.push({'event': this.cur_rel_ls['event'], 'time': this.cur_rel_ls['time'], 'affiliation': this.cur_rel_ls['affiliation']});
      this.cur_rel_ls = {'event': '', 'time': '', 'affiliation': ''};
      this.cur_type_ls = [];
    },

    change_version(){
      this.$message({
        message: 'Data Partition Changed!',
        type: 'warning'
      });
    },

  },
  watch: {
    data_version(val, oldVal) {
      this.rand_search()
    }
  }
}

function strToJson(str){
  return eval('(' + str + ')');
}
function sort_entity(a, b){
  return a.start - b.start;
}
function count_r(str, words){
  let regex = new RegExp("\r", 'g');
  let result = str.match(regex);
  let regex2 = new RegExp("&.*?;", 'g');
  let result2 = str.match(regex2);
  let len = 0;
  if(result){
    len += result.length;
  }
  if(result2){
    console.log(result2);
    for(let i = 0; i < result2.length; i++) {
      if(words.indexOf(result2[i].slice(1, -1)) === -1 && result2[i].length < 10){
        len += result2[i].length - 1;
      }
    }
  }
  return len;
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

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
