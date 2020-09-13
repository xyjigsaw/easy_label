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

          <el-col :span="5"><div class="grid-content bg-purple">
            <el-switch
              style="display: block; margin-top: 1px;"
              v-model="autoHint"
              active-color="#13ce66"
              inactive-color="#dddddd"
              active-text="AUTO HINT"
              @change="autoHintMSG">
            </el-switch>
            <el-switch
              style="display: block; margin-top: 5px; margin-left: 10px;"
              v-model="autoMarkSelection"
              active-color="#13ce66"
              inactive-color="#dddddd"
              active-text="AUTO MARK">
            </el-switch>
          </div></el-col>

        </el-row>

        <div id="class_ls">
        </div>

        <div id="operation" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px; font-size: 15px;">
          <p v-show="!edit_fid">Click <i class="el-icon-edit"></i> In The Table On The Right To Start</p>
          <el-button v-if="edit_fid" type="text">Version: {{ tableData[edit_table_pos]['version'] }} </el-button>
          <el-button v-if="edit_fid" type="text">{{ tableData[edit_table_pos]['file_name'] }}</el-button>
          <div id="text_detail_group">
            <el-button v-if="edit_fid" type="text">Abstract</el-button>
            <div id="text_detail_0" @mouseup="selectText('text_detail_0')" @click="clickEntity('text_detail_0')"></div>
            <el-button v-if="edit_fid" type="text">Introduction</el-button>
            <div id="text_detail_1" @mouseup="selectText('text_detail_1')" @click="clickEntity('text_detail_1')"></div>
            <el-button v-if="edit_fid" type="text">Conclusion</el-button>
            <div id="text_detail_2" @mouseup="selectText('text_detail_2')" @click="clickEntity('text_detail_2')"></div>
          </div>
        </div>

      </el-main>

      <el-aside width="400px" style="height: 1000px;background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px 5px 5px 0;">
        <el-row>
          <el-button type="text">Project: {{ name }}</el-button>
          <el-button type="text">Users: {{ onlineUsers }}</el-button>
          <el-button type="primary" icon="el-icon-document" v-show="this.pdf_page_count > 0" @click="showPDF = ! showPDF" size="mini" plain></el-button>
        </el-row>

        <div v-show="this.showPDF && this.pdf_page_count > 0" class="pdf_div" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:2px; margin: 1px;">
          <pdf
            :src="pdfUrl"
            ref="ref"
            class="pdf"
            :page="pdf_cur_page"
            @num-pages="pdf_page_count=$event"
            @page-loaded="pdf_cur_page=$event"
            @loaded="loadPdfHandler">
          </pdf>
          <el-row>
            <el-button type="primary" icon="el-icon-caret-left" @click="changePdfPage(0)" size="mini" plain></el-button>
            <el-button type="primary" icon="el-icon-caret-right" @click="changePdfPage(1)" size="mini" plain></el-button>
          </el-row>
        </div>

        <el-table
          :data="tableData.slice((currentPage - 1) * pageSize, currentPage*pageSize)"
          border
          :highlight-current-row="true"
          :row-style="{height:'8px'}" :cell-style="{padding:'5px 0'}"
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
  import pdf from 'vue-pdf';
  import jsPlumb from "jsplumb";
  export default {
    components:{
      pdf
    },
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
        raw_text: [],

        markMode: true,

        autoMarkSelection: true,

        autoHint: true,
        hintList: [],

        logVis: false,
        logDirection: 'btt',
        logTable: [],

        onlineUsers: null,

        pdfUrl: '',
        pdf_cur_page: 1,
        pdf_page_count: 0,
        showPDF: true,
      };
    },
    methods: {
      lazy_fetch_file(anchor){
        let url_data={
          p_id: this.p_id,
          anchor: anchor,
          pageSize: this.pageSize,
        };
        this.$axios.get('/api/fetch_file', {params: url_data}).then(response => {
          this.tableData = this.tableData.concat(response.data['data']);
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
        this.$axios.get('/api/fetch_class', {params: url_data}).then(response => {
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
        this.see_PDF(info);
        this.showPDF = true;
        this.edit_fid = info['f_id'];
        this.edit_text = JSON.parse(info['text']);
        this.edit_entity_list = JSON.parse(info['entity_list']);

        for(let key in this.edit_entity_list){
          if(this.edit_entity_list.hasOwnProperty(key))
            this.raw_text.push(this.edit_entity_list[key].length === 0)
        }

        this.checkList = [];
        this.labelIns.checkList = this.checkList;
        for(let i = 0; i < this.tableData.length; i++){
          if(this.tableData[i]['f_id'] === this.edit_fid){
            this.edit_table_pos = i;
          }
        }
        this.change_status(this.edit_table_pos, 1, true);
        for(let elementID in this.edit_entity_list){
          if(this.edit_entity_list.hasOwnProperty(elementID)){
            let tmp_entity_str_ls = this.edit_entity_list[elementID];
            if(this.autoHint) {
              tmp_entity_str_ls = tmp_entity_str_ls.concat(this.getHint(elementID));
            }
            let decorated_text = this.genContent(tmp_entity_str_ls, this.edit_text[elementID]);
            this.display_content(decorated_text, elementID);
          }
        }
        this.logTable.unshift({'Event': "Mark", 'f_id': this.edit_fid, 'info': 'Edit file to mark entity',
          'entity_list_len': this.count_entity_num()});
      },

      count_entity_num(){
        let entity_list_len = 0;
        for(let key in this.edit_entity_list){
          if(this.edit_entity_list.hasOwnProperty(key)){
            entity_list_len += this.edit_entity_list[key].length;
          }
        }
        return entity_list_len;
      },

      display_content(decorated_text, elementID){
        decorated_text = decorated_text.replace(/\n/g, '\n<hr/>');
        document.getElementById(elementID).innerHTML="<div style=\"box-shadow: 0 0 2px #aeaeae; margin: 10px 10px 20px 10px; padding:20px; border-radius: 5px; " +
          "line-height: 26px; text-align: left; background-color: #f8f8f8\">" + decorated_text + "</div>";
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
          let word_str = entity_str_ls[j]['word'];
          split_ls.push([type_str, parseInt(start_str), parseInt(end_str), word_str]);
        }
        for(let j = split_ls.length - 1; j >= 0; j--){
          let [type, startNum, endNum, word] = split_ls[j];
          for(let k = 0; k < this.classNameList.length; k++){
            if(type === this.classNameList[k]){
              cur_content = cur_content.substring(0, startNum) + '<span class="' + type + '" style="color:' + this.classColorList[k]+
                '; font-weight: bold;  cursor: pointer;" data-startNum="' + startNum + '" data-endNum="' + endNum + '" data-word="' + word + '">'
                + cur_content.substring(startNum, endNum) + '</span>' + cur_content.substring(endNum);
            }
          }
          if(type === 'auto-hint'){
            cur_content = cur_content.substring(0, startNum) + '<span class="auto-hint" style="cursor:' + 'pointer'+
              '; border-bottom:2px solid #898989; " data-startNum="' + startNum + '" data-endNum="' + endNum + '" data-word="' + word + '">'
              + cur_content.substring(startNum, endNum) + '</span>' + cur_content.substring(endNum);
          }
        }
        return cur_content;
      },

      getHint(elementID){
        //this.hintList = {"text_detail_0": [], "text_detail_1": [], "text_detail_2": []};
        let url_data={
          text_detail: JSON.stringify(this.edit_text)
        };
        //this.$axios.get('/api/fetch_hint', {params: url_data}).then(response => {
        //  this.hintList = response.data['data'];
        //}).catch(err => {
        //  this.$notify.error({title: 'Error', message: err});
        //});
        this.hintList = {"text_detail_0": [{"end": 371, "type": "auto-hint", "word": "unified", "start": 364}], "text_detail_1": [{"end": 46, "type": "auto-hint", "word": "alignment", "start": 37}], "text_detail_2": []}
        this.removeRedundantHint(elementID);
        return this.hintList[elementID];
      },

      autoHintMSG(){
        this.$notify.info({
          title: 'Message',
          message: 'Changes will take effect after re entering the edit page.'
        });
      },

      removeRedundantHint(elementID){
        for(let i = this.hintList[elementID].length-1; i >= 0; i--){
          for(let j = 0; j < this.edit_entity_list[elementID].length; j++){
            if(this.hintList[elementID][i]['start'] === this.edit_entity_list[elementID][j]['start'] ||
              this.hintList[elementID][i]['end'] === this.edit_entity_list[elementID][j]['end']){
              this.hintList[elementID].splice(i,1);
              break;
            }
          }
        }
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
          let url_data = new FormData();
          url_data.append('f_id', this.edit_fid);
          url_data.append('entity_list', JSON.stringify(this.edit_entity_list));
          this.$axios.put('/api/update_entity_list', url_data).then(response => {
            this.tableData[this.edit_table_pos]['version']++;
            this.tableData[this.edit_table_pos]['entity_list'] = JSON.stringify(this.edit_entity_list);
            this.$notify({
              title: 'Success',
              message: 'Entity submitted successfully',
              type: 'success'
            });
            this.logTable.unshift({'Event': "Save", 'f_id': this.edit_fid, 'info': 'Save to database successfully',
              'entity_list_len': this.edit_entity_list.length});

            let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'entity_list': JSON.stringify(this.edit_entity_list),
                'version': this.tableData[this.edit_table_pos]['version'], 'pos': this.edit_table_pos}, 'subject': 'save'}
            this.sendMessage(JSON.stringify(wsInfo));
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

      selectText(elementID){
        try{
          if(this.markMode === true){
            let element_id_int = parseInt(elementID.charAt(elementID.length-1));
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
              if((this.raw_text[element_id_int] || base > 0 || (!this.raw_text[element_id_int] && base === 0))
                && start_num < end_num && end_num - start_num === selected.length && this.checkList.length === 1){

                if(this.autoMarkSelection){
                  let marginChar = [',', '.', ':', ';', '?', '!', ' ', '(', ')', '>', '<', '"', '*', '%', '-', '_', '\n']
                  let selectedPosList = [];
                  let tmpPos = 0;
                  while(tmpPos > -1){
                    tmpPos = this.edit_text[elementID].indexOf(selected, tmpPos + selected.length);
                    selectedPosList.push(tmpPos);
                  }
                  let allStartNum = [];
                  for(let i = 0; i < this.edit_entity_list[elementID].length; i++){
                    allStartNum.push(this.edit_entity_list[elementID][i]['start'])
                  }
                  for(let i = 0; i < selectedPosList.length - 1; i++){
                    if(allStartNum.indexOf(selectedPosList[i]) === -1){
                      if(marginChar.indexOf(this.edit_text[elementID][selectedPosList[i] - 1]) > -1 && marginChar.indexOf(this.edit_text[elementID][selectedPosList[i] + selected.length]) > -1){
                        this.edit_entity_list[elementID].push({'start': selectedPosList[i],
                          'end': selectedPosList[i] + selected.length, 'word': selected, 'type': this.checkList[0]});
                      }
                    }
                  }
                }else{
                  this.edit_entity_list[elementID].push({'start': base + start_num,
                    'end': base + end_num, 'word': selected, 'type': this.checkList[0]});
                }

                let decorated_text = this.genContent(this.edit_entity_list[elementID], this.edit_text[elementID]);
                this.display_content(decorated_text, elementID);
                this.raw_text[element_id_int] = false;
                this.logTable.unshift({'Event': "Mark", 'f_id': this.edit_fid,
                  'info': 'Selected: ' + selected + ', Start: ' + start_num + ', End: ' + end_num,
                  'entity_list_len': this.count_entity_num()});
              }else if(base === 0 && this.checkList.length === 1){
              }else{
              }
            }else{
            }
          }else{//relation mode
            let spanObj=document.elementFromPoint(event.clientX, event.clientY);
            console.log(spanObj);
          }

        }catch(err){
          this.$message.error(err);
        }
      },

      clickEntity(elementID){
        if(this.markMode === true){
          let element_id_int = parseInt(elementID.charAt(elementID.length-1));
          let spanObj=document.elementFromPoint(event.clientX, event.clientY);
          let spanClass = spanObj.getAttribute("class");
          if(this.checkList.length === 1 && spanClass === this.checkList[0]) {
            let startNum = parseInt(spanObj.getAttribute("data-startNum"));
            let endNum = parseInt(spanObj.getAttribute("data-endNum"));
            let cur_content = this.edit_text[elementID];
            for(let i = this.edit_entity_list[elementID].length-1; i >= 0; i--){
              if(this.edit_entity_list[elementID][i]['start'] === startNum && this.edit_entity_list[elementID][i]['end'] === endNum){
                this.edit_entity_list[elementID].splice(i,1);
              }
            }
            if(this.edit_entity_list[elementID].length === 0){this.raw_text[element_id_int] = true;}
            let decorated_text = this.genContent(this.edit_entity_list[elementID], cur_content);
            this.display_content(decorated_text, elementID);
            this.logTable.unshift({'Event': "Unmark", 'f_id': this.edit_fid,
              'info': 'Class: ' + spanClass + ', Start: ' + startNum + ', End: ' + endNum,
              'entity_list_len': this.count_entity_num()});
          }else if(this.checkList.length === 1 && spanClass === 'auto-hint'){//auto-hint
            let startNum = parseInt(spanObj.getAttribute("data-startNum"));
            let endNum = parseInt(spanObj.getAttribute("data-endNum"));
            let word = spanObj.getAttribute("data-word");
            let cur_content = this.edit_text[elementID];
            this.removeRedundantHint(elementID);
            this.edit_entity_list[elementID].push({'start': startNum,
              'end': endNum, 'word': word, 'type': this.checkList[0]});
            let decorated_text = this.genContent(this.edit_entity_list[elementID], cur_content);
            this.display_content(decorated_text, elementID);
            this.raw_text[element_id_int] = false;
            this.logTable.unshift({'Event': "Mark", 'f_id': this.edit_fid,
              'info': 'Selected: ' + word + ', Start: ' + startNum + ', End: ' + endNum,
              'entity_list_len': this.count_entity_num()});
          }
        }
      },

      change_status(pos, status, send_msg){
        if(this.edit_fid){
          let url_data = new FormData();
          url_data.append('f_id', this.edit_fid);
          url_data.append('status', status);
          this.$axios.put('/api/change_status', url_data).then(response => {
            this.tableData[pos]['is_edit'] = status;
            let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'status': status, 'pos': pos}, 'subject': 'lock'}
            if(send_msg){
              this.sendMessage(JSON.stringify(wsInfo));
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

      see_PDF(info) {
        let pdf_path = info['file_path'];
        pdf_path = btoa(pdf_path);
        this.pdfUrl = pdf.createLoadingTask(this.$route.meta.pdf_port + pdf_path);
        console.log(this.$route.meta.pdf_port + pdf_path);
        this.pdfUrl.promise.then(pdf => {
          this.pdf_page_count = pdf.numPages;
        }).catch(err => {
          console.log(err)
        });
      },

      loadPdfHandler(e) {
        this.pdf_cur_page = 1;
      },

      changePdfPage(val) {
        if(val === 0 && this.pdf_cur_page > 1) {
          this.pdf_cur_page --
        }
        if(val === 1 && this.pdf_cur_page < this.pdf_page_count) {
          this.pdf_cur_page ++;
        }
      },

    },

    created() {
      this.init_page();
      let arr = [];
      let that = this;
      document.onkeydown = function(e) {
        if(arr.length > 0) { // a-z按键长按去重
          if(arr.indexOf(e.key.toLowerCase()) >= 0) {
            return
          }
        }
        arr.push(e.key.toLowerCase())
        this.keydown = arr.join('+');
        if(this.keydown === 'shift+s') {
          this.keydown = '';
          that.save();
        }else if(this.keydown === 'shift+p'){
          this.keydown = '';
          that.see_all();
        }
      }
      document.onkeyup = function (e) {
        arr.splice(arr.indexOf( e.key.toLowerCase() ),1);
        this.keydown = arr.join('+');
      }
      this.keydown = '';
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

