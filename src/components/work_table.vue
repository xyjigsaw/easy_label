<template>
  <div>
    <el-container>
      <el-main style="padding: 0;">

        <el-row :gutter="12" type="flex" justify="center" style="background-color: #FFFFFF; padding: 10px;margin: 5px 5px 0 5px;">
          <el-col :span="3"><div class="grid-content bg-purple">
            <el-button type="danger" icon="el-icon-back" circle @click="back2project"></el-button>
            <p style="font-size: 8px; color: #F56C6C; text-align: center; margin: 0;">Exit</p>
          </div></el-col>
          <el-col :span="3"><div class="grid-content bg-purple">
            <el-button type="warning" icon="el-icon-collection-tag" circle @click="editClass"></el-button>
            <p style="font-size: 8px; color: #ebb563; text-align: center; margin: 0;">Class</p>
          </div></el-col>
          <el-col :span="3"><div class="grid-content bg-purple">
            <el-button icon="el-icon-search" circle @click="see_all"></el-button>
            <p style="font-size: 8px; color: #606266; text-align: center; margin: 0;">Preview</p>
          </div></el-col>
          <el-col :span="3"><div class="grid-content bg-purple">
            <el-button type="info" icon="el-icon-message" circle @click="logVis = true"></el-button>
            <p style="font-size: 8px; color: #909399; text-align: center; margin: 0;">Log</p>
          </div></el-col>
          <el-col :span="3"><div class="grid-content bg-purple">
            <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
            <p style="font-size: 8px; color: #67C23A; text-align: center; margin: 0;">Save</p>
          </div></el-col>
        </el-row>

        <div id="class_ls">
        </div>

        <div id="operation" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px; font-size: 15px;">
          <p v-show="!edit_fid">Click <i class="el-icon-edit"></i> In The Table On The Right To Start</p>
          <el-button v-if="edit_fid" type="text">Version: {{ tableData[edit_table_pos]['version'] }} </el-button>
          <el-button v-if="edit_fid" type="text">{{ tableData[edit_table_pos]['file_name'] }}</el-button>
          <div id="text_detail" @mouseup="selectText" @click="deleteEntity"></div>
        </div>
      </el-main>

      <el-aside width="330px" style="height: 1000px;background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px 5px 5px 0;">
        <el-row>
          <el-button type="text">{{ name }}</el-button>
          <el-button type="text">Users: {{ onlineUsers }}</el-button>
        </el-row>
        <el-table
          :data="tableData.slice((currentPage - 1) * pageSize, currentPage*pageSize)"
          border
          :highlight-current-row="true"
          style="width: 100%; font-size: 10px">
          <el-table-column fixed prop="file_name" label="Name"></el-table-column>
          <el-table-column fixed prop="version" label="Ver." width="48"></el-table-column>
          <el-table-column fixed prop="is_edit" label="Lock" width="48"></el-table-column>

          <el-table-column
            fixed="right"
            label="Edit"
            width="60">
            <template slot-scope="scope">
              <el-button icon="el-icon-edit" type="primary" @click="editFile(scope.$index, scope.row)" size="mini"></el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="partition" style="margin-top:15px;">
          <el-row>
            <el-pagination background
                           hide-on-single-page
                           @next-click="handleNextClick"
                           :current-page.sync="currentPage"
                           :page-size="pageSize"
                           layout="total, prev, next"
                           :total="parseInt(total)">
            </el-pagination>
          </el-row>
        </div>

      </el-aside>
    </el-container>

    <el-drawer
      :with-header="false"
      :visible.sync="logVis"
      :direction="logDirection">
      <div class="log_content">
          <el-card class="box-card" style="margin: 10px; width:48%;box-shadow: 0 0 5px #dddddd; float: left;">
            <div class="log-table" style="padding-left: 40px; padding-right: 40px; margin: auto">
              <el-table :data="logTable" height="160" stripe style="width: 100%; text-align: center; font-size: 5px;"
                        :row-style="{height:'8px'}" :cell-style="{padding:'5px 0'}">
                <el-table-column prop="Event" label="Local Event" width="110"></el-table-column>
                <el-table-column prop="entity_list_len" label="Number of Entity" width="150"></el-table-column>
                <el-table-column prop="info" label="Info"></el-table-column>
                <el-table-column prop="f_id" label="File ID" width="120"></el-table-column>
              </el-table>
            </div>
          </el-card>

          <el-card class="box-card" style="margin: 10px; width:48%;box-shadow: 0 0 5px #dddddd; float: left;">
            <div class="log-table" style="padding-left: 40px; padding-right: 40px; margin: auto">
              <el-table :data="wsTable" height="160" stripe style="width: 100%; text-align: center; font-size: 5px;"
                        :row-style="{height:'8px'}" :cell-style="{padding:'5px 0'}">
                <el-table-column prop="subject" label="Remote Event" width="120"></el-table-column>
                <el-table-column prop="info" label="Info from other users"></el-table-column>
              </el-table>
            </div>
          </el-card>

      </div>
    </el-drawer>
  </div>
</template>

<script>
  import Vue from 'vue'
  export default {
    data() {
      return {
        ws: null,
        wsTable: [],

        p_id: this.$route.query.p_id,
        name: this.$route.query.name,
        path: this.$route.query.path,

        tableData: [],
        currentPage: 1,
        pageSize: 8,
        total: this.$route.query.total,

        classNameList: [],
        classColorList: [],

        labelIns: null,
        checkList: [],
        check_max: 1,

        edit_fid: null,
        edit_text: '',
        edit_entity_list: [],
        edit_table_pos: null,
        raw_text: null,

        logVis: false,
        logDirection: 'btt',
        logTable: [],

        onlineUsers: null,
      };
    },
    methods: {
      lazy_fetch_file(anchor){
        let url_data={
          p_id: this.p_id,
          anchor: anchor,
          pageSize: this.pageSize,
        };
        this.$axios.post('/api/fetch_file', url_data).then(response => {
          if (response.data['message'] === 'success') {
            this.tableData = this.tableData.concat(response.data['data']);
          }
        }).catch(err => {
          this.$notify.error({title: 'Error', message: err});
        });
      },

      init_page() {
        this.ws = new WebSocket(this.$route.meta.ws_port);
        this.ws.onmessage = this.getMessage;
        this.ws.onopen=this.openMessage;

        let url_data={
          p_id: this.p_id,
        };
        this.$axios.post('/api/fetch_class', url_data).then(response => {
          if (response.data['message'] === 'success') {
            if(response.data['data'].length === 0){
              this.$confirm('There is no class label in database.', 'WARNING', {
                confirmButtonText: 'Add Class',
                cancelButtonText: 'Exit',
                type: 'warning'
              }).then(() => {
                this.$router.push({path: '/home/class_manage', query: {p_id: this.$route.query.p_id, name: this.$route.query.name, path: this.$route.query.path, total: this.$route.query.total}});
              }).catch(() => {
                this.$router.push("/home/project_manage");
              });
            }

            this.classNameList = [];
            this.classColorList = [];

            let class_str = '';
            for(let i = 0; i < response.data['data'].length; i++){
              this.classNameList.push(response.data['data'][i]['label']);
              this.classColorList.push(response.data['data'][i]['color']);
              class_str = this.addClassLabelStr(class_str, response.data['data'][i]['label'], response.data['data'][i]['color']);
            }
            this.checkList = [];
            this.gen_labels(class_str, '#class_ls');
            this.lazy_fetch_file(0);

          }
        }).catch(err => {
          this.$notify.error({title: 'Error', message: err});
        });
      },

      handleNextClick(){
        if(this.tableData.length < this.total){
          this.lazy_fetch_file(this.currentPage * this.pageSize);
        }
      },

      addClassLabelStr(template_string, label, color){
        template_string +=
          '<el-checkbox label="' + label + '" style="padding:8px; border-radius:5px; background-color:' + color +
          ';font-weight: bold;"></el-checkbox>';
        return template_string;
      },

      gen_labels(template_str, elementID){
        let that = this;
        let classLabel = Vue.extend({
          template: '<el-checkbox-group v-model="checkList" @change="click_check" :max="check_max" ' +
            'style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding: 8px;margin: 0 5px;">' + template_str +
            '</el-checkbox-group>',
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
            }
          }
        });

        this.labelIns = new classLabel();
        this.labelIns.$mount(elementID);

      },

      editFile(index, info){
        if(info['is_edit'] === 1){
          this.$notify({
            title: 'Warning',
            message: 'This file is being edited.',
            duration: 4000,
            type: 'warning'
          });
          return;
        }

        if(this.edit_fid){
          this.change_status(this.edit_table_pos, 0, true);
          this.$notify({
            title: 'Warning',
            message: 'Please save the previous file before switching files. If it has been saved, please ignore.',
            duration: 5000,
            type: 'info'
          });
        }
        this.edit_fid = info['f_id'];
        this.edit_text = info['text'];
        this.edit_entity_list = eval(info['entity_list']);
        this.raw_text = this.edit_entity_list.length === 0;
        this.checkList = [];
        this.labelIns.checkList = this.checkList;
        for(let i = 0; i < this.tableData.length; i++){
          if(this.tableData[i]['f_id'] === this.edit_fid){
            this.edit_table_pos = i;
          }
        }
        this.change_status(this.edit_table_pos, 1, true);
        let decorated_text = this.genContent(this.edit_entity_list, this.edit_text);
        this.display_content(decorated_text);

        this.logTable.unshift({'Event': "Mark", 'f_id': this.edit_fid, 'info': 'Edit file to mark entity',
          'entity_list_len': this.edit_entity_list.length});
      },

      display_content(decorated_text){
        decorated_text = decorated_text.replace(/\n/g, '\n<hr/>');
        document.getElementById("text_detail").innerHTML="<div style=\"box-shadow: 0 0 2px #dddddd; margin: 10px; padding:20px; border-radius: 5px; " +
          "line-height: 26px; text-align: left\">" + decorated_text + "</div>";
        this.click_check();
      },

      sort_entity(a, b){
        return a.start - b.start;
      },

      click_check(){
        for(let i=0; i < this.classNameList.length; i++){
          let obj = document.getElementsByClassName(this.classNameList[i]);
          if(this.checkList.indexOf(this.classNameList[i]) > -1){
            for(let j=0; j<obj.length; j++){
              obj.item(j).style.color=this.classColorList[i];
              obj.item(j).style.fontWeight="bold";
              obj.item(j).style.backgroundColor=this.classColorList[i];
              obj.item(j).style.color="white";
              obj.item(j).style.padding="1px 3px";
              obj.item(j).style.borderRadius="3px";
            }
          }else{
            for(let j=0; j<obj.length; j++){
              obj.item(j).style.backgroundColor='transparent';
              obj.item(j).style.color=this.classColorList[i];
              obj.item(j).style.fontWeight="bold";
              obj.item(j).style.padding="1px 3px";
            }
          }
        }
      },

      genContent(entity_str_ls, cur_content){
        entity_str_ls.sort(this.sort_entity);
        let split_ls = [];
        for(let j = 0; j < entity_str_ls.length; j++){
          let start_str = entity_str_ls[j]['start'];
          let end_str = entity_str_ls[j]['end'];
          let type_str = entity_str_ls[j]['type'];
          split_ls.push([type_str, parseInt(start_str), parseInt(end_str)]);
        }
        for(let j = split_ls.length - 1; j >= 0; j--){
          let [type, startNum, endNum] = split_ls[j];
          for(let k = 0; k < this.classNameList.length; k++){
            if(type===this.classNameList[k]){
              cur_content = cur_content.substring(0, startNum) + '<span class="' + type + '" style="color:' + this.classColorList[k]+
                '; font-weight: bold;  cursor: pointer;" data-startNum="' + startNum + '" data-endNum="' + endNum + '">'
                + cur_content.substring(startNum, endNum) + '</span>' + cur_content.substring(endNum)
            }
          }
        }
        return cur_content;
      },

      see_all(){
        this.checkList = this.classNameList;
        this.labelIns.checkList = this.checkList;
        this.click_check();
        this.checkList = [];
        this.labelIns.checkList = this.checkList;
        this.logTable.unshift({'Event': "Preview", 'f_id': this.edit_fid, 'info': 'Preview all entity',
          'entity_list_len': this.edit_entity_list.length});
      },

      editClass() {
        if(this.onlineUsers > 1){
          this.$notify({
            title: 'Warning',
            message: 'There are other users editing.',
            type: 'warning'
          });
        }else{
          this.$router.push({path: '/home/class_manage',
            query: {p_id: this.$route.query.p_id, name: this.$route.query.name, path: this.$route.query.path, total: this.$route.query.total}});
        }
      },

      save(){
        if(this.edit_fid === null){
          this.$notify({
            title: 'Info',
            message: 'Nothing to Save',
            type: 'info'
          });
          return;
        }
        this.$confirm('Submit current changes?', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          let url_data={
            f_id: this.edit_fid,
            entity_list: this.edit_entity_list,
          };
          this.$axios.post('/api/submit_entity_list', url_data).then(response => {
            if (response.data['message'] === 'success') {
              this.tableData[this.edit_table_pos]['version']++;
              this.tableData[this.edit_table_pos]['entity_list'] = this.edit_entity_list;
              this.$notify({
                title: 'Success',
                message: 'Entity submitted successfully',
                type: 'success'
              });
              this.logTable.unshift({'Event': "Save", 'f_id': this.edit_fid, 'info': 'Save to database successfully',
                'entity_list_len': this.edit_entity_list.length});

              let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'entity_list': this.edit_entity_list,
                  'version': this.tableData[this.edit_table_pos]['version'], 'pos': this.edit_table_pos}, 'subject': 'save'}
              this.sendMessage(JSON.stringify(wsInfo));

            }else{
              this.$notify.error({title: 'Error', message: 'Unknown Error'});
            }
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
            this.logTable.unshift({'Event': "Save", 'f_id': this.edit_fid, 'info': 'Cannot Save to database',
              'entity_list_len': this.edit_entity_list.length});
          });
        }).catch(() => {
        });
      },

      back2project(){
        this.$router.push("/home/project_manage");
      },

      count_str_len(text, str){
        let regex = new RegExp(str, 'g');
        let result = text.match(regex);
        return !result ? 0 : result.length
      },

      selectText(){
        try{
          let selected=window.getSelection().toString();
          selected = selected.trim();
          if(selected != null){
            let range = window.getSelection().getRangeAt(0);
            let base = 0;
            let preElement = range.startContainer;
            while(preElement.previousSibling){
              base += preElement.previousSibling.textContent.length;
              preElement = preElement.previousSibling;
            }
            let start_num = Math.min(window.getSelection().anchorOffset, window.getSelection().focusOffset);
            let end_num = Math.max(window.getSelection().anchorOffset, window.getSelection().focusOffset);
            //console.log(base, this.raw_text, start_num, end_num, selected)
            if((this.raw_text || base > 0 || (!this.raw_text && base === 0))
              && start_num < end_num && end_num - start_num === selected.length && this.checkList.length === 1){
              this.edit_entity_list.push({'start': base + start_num,
                'end': base + end_num, 'word': selected, 'type': this.checkList[0]});
              let decorated_text = this.genContent(this.edit_entity_list, this.edit_text);
              this.display_content(decorated_text);
              this.raw_text = false;
              this.logTable.unshift({'Event': "Mark", 'f_id': this.edit_fid,
                'info': 'Selected: ' + selected + ', Start: ' + start_num + ', End: ' + end_num,
                'entity_list_len': this.edit_entity_list.length});
            }else if(base === 0 && this.checkList.length === 1){
            }else{
            }
          }else{
          }
        }catch(err){
          this.$message.error(err);
        }
      },

      deleteEntity(){
        let spanObj=document.elementFromPoint(event.clientX, event.clientY);
        let spanClass = spanObj.getAttribute("class");
        if(this.checkList.length === 1 && spanClass === this.checkList[0]) {
          let startNum = parseInt(spanObj.getAttribute("data-startNum"));
          let endNum = parseInt(spanObj.getAttribute("data-endNum"));
          let cur_content = this.edit_text;
          for(let i = this.edit_entity_list.length-1; i >= 0; i--){
            if(this.edit_entity_list[i]['start'] === startNum && this.edit_entity_list[i]['end'] === endNum){
              this.edit_entity_list.splice(i,1);
            }
          }
          if(this.edit_entity_list.length === 0){this.raw_text = true;}
          let decorated_text = this.genContent(this.edit_entity_list, cur_content);
          this.display_content(decorated_text);
          this.logTable.unshift({'Event': "Unmark", 'f_id': this.edit_fid,
            'info': 'Class: ' + spanClass + ', Start: ' + startNum + ', End: ' + endNum,
            'entity_list_len': this.edit_entity_list.length});
        }
      },

      change_status(pos, status, send_msg){
        if(this.edit_fid){
          let url_data={
            f_id: this.edit_fid,
            status: status,
          };
          this.$axios.post('/api/change_status', url_data).then(response => {
            if (response.data['message'] === 'success') {
              this.tableData[pos]['is_edit'] = status;
              let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'status': status, 'pos': pos}, 'subject': 'lock'}
              if(send_msg){
                this.sendMessage(JSON.stringify(wsInfo));
              }
            }
          }).catch(err => {
          });
        }
      },

      getMessage(info) {
        let info_data = JSON.parse(info.data);
        let msg = info_data['message'];
        console.log(info_data);

        if(info_data['subject'] === 'lock' && msg['p_id'] === this.p_id && msg['pos'] <= this.tableData.length){
          this.tableData[msg['pos']]['is_edit'] = msg['status'];
          if(msg['status'] === 1){
            this.wsTable.unshift({'subject': 'File Lock', 'info': this.tableData[msg['pos']]['file_name'] + ' is locked.'});
          }else{
            this.wsTable.unshift({'subject': 'File Unlock', 'info': this.tableData[msg['pos']]['file_name'] + ' is unlocked.'});
          }
        }

        if(info_data['subject'] === 'save' && msg['p_id'] === this.p_id && msg['pos'] <= this.tableData.length){
          this.tableData[msg['pos']]['entity_list'] = msg['entity_list'];
          this.tableData[msg['pos']]['version'] = msg['version'];
          this.wsTable.unshift({'subject': 'Remote Info Sync', 'info': this.tableData[msg['pos']]['file_name'] + 'Updated, Version: '+ msg['version']});
        }

        if(info_data['subject'] === 'total' && msg['p_id'] === this.p_id){
          this.onlineUsers=msg['num'];
          this.wsTable.unshift({'subject': 'Login', 'info': 'User ' + msg['socket_ID'] + ' login, Total: ' + msg['num']});
        }
      },

      sendMessage(info) {
        this.ws.send(info);
      },

      openMessage() {
        let wsInfo = {'message': {'p_id': this.p_id}, 'subject': 'online'}
        this.ws.send(JSON.stringify(wsInfo));
      },

    },

    created() {
      this.init_page();
    },

    beforeDestroy() {
      if(this.edit_fid){
        this.change_status(this.edit_table_pos, 0, true);
      }
      let wsInfo = {'message': {'p_id': this.p_id}, 'subject': 'offline'}
      this.sendMessage(JSON.stringify(wsInfo));
    },

  };

</script>

