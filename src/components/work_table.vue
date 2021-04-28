<template>
  <div>
    <el-container v-loading="loadingNow"
                  element-loading-text="Loading Now..."
                  element-loading-spinner="el-icon-loading"
                  element-loading-background="rgba(0, 0, 0, 0.8)">
      <el-main style="padding: 0;">

        <el-row :gutter="12" type="flex" justify="center" style="background-color: #FFFFFF; padding: 10px;margin: 5px 5px 0 5px;">
          <el-col :span="2"><div class="grid-content bg-purple">
            <el-button type="danger" icon="el-icon-back" circle @click="back2project"></el-button>
            <p style="font-size: 8px; color: #F56C6C; text-align: center; margin: 0;">Exit</p>
          </div></el-col>
          <el-col :span="2"><div class="grid-content bg-purple">
            <el-button type="warning" icon="el-icon-collection-tag" circle @click="editClass"></el-button>
            <p style="font-size: 8px; color: #ebb563; text-align: center; margin: 0;">Class</p>
          </div></el-col>
          <el-col :span="2"><div class="grid-content bg-purple">
            <el-button icon="el-icon-search" circle @click="see_all"></el-button>
            <p style="font-size: 8px; color: #606266; text-align: center; margin: 0;">Preview</p>
          </div></el-col>
          <el-col :span="2"><div class="grid-content bg-purple">
            <el-button type="info" icon="el-icon-message" circle @click="logVis = true"></el-button>
            <p style="font-size: 8px; color: #909399; text-align: center; margin: 0;">Log</p>
          </div></el-col>
          <el-col :span="2"><div class="grid-content bg-purple">
            <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
            <p style="font-size: 8px; color: #67C23A; text-align: center; margin: 0;">Save</p>
          </div></el-col>
          <el-col :span="2"><div class="grid-content bg-purple">
            <el-button type="primary" icon="el-icon-question" circle @click="showHelp"></el-button>
            <p style="font-size: 8px; color: #409EFF; text-align: center; margin: 0;">Help</p>
          </div></el-col>

          <el-col :span="5" v-show="markMode"><div class="grid-content bg-purple">
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

          <el-col :span="5"><div class="grid-content bg-purple">
            <el-switch
              style="display: block; margin-top: 8px;"
              v-model="markMode"
              active-color="#13ce66"
              inactive-color="#409eff"
              active-text="Entity"
              inactive-text="Relation"
              >
            </el-switch>
          </div></el-col>

        </el-row>

        <div id="class_ls">
        </div>

        <div id="operation" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px; font-size: 15px;">
          <p v-show="!edit_fid">Click <i class="el-icon-edit"></i> In The Table On The Right To Start</p>
          <el-button v-if="edit_fid" type="text">Version: {{ tableData[edit_table_pos]['version'] }} </el-button>
          <el-button v-if="edit_fid" type="text">{{ tableData[edit_table_pos]['file_name'] }}</el-button>
          <el-button v-if="edit_fid" size="small" type="danger" icon="el-icon-close" plain @click="update_check(edit_fid, '0')"></el-button>
          <el-button v-if="edit_fid" size="small" type="success" icon="el-icon-check" plain @click="update_check(edit_fid, '1')"></el-button>
          <el-button v-if="edit_fid" size="small" type="info" icon="el-icon-minus" plain @click="update_check(edit_fid, 'Null')"></el-button>
          <div id="text_detail_group" v-if="edit_fid">
            <el-collapse v-model="activeNames">
              <el-collapse-item v-for="text_id in text_detail_ls" :name="text_id" :key="text_id"
                                :title="text_id.substr(text_id.lastIndexOf('_') + 1) === '0' ? '· ABSTRACT': '· Section ' + text_id.substr(text_id.lastIndexOf('_') + 1)">
                <div :id="text_id" @mouseup="selectText(text_id)" @click="clickEntity(text_id)"></div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </el-main>

      <el-aside width="400px" style="height: 1200px;background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:5px; margin: 5px 5px 5px 0;">
        <el-row>
          <el-button type="text">Project: {{ name }}</el-button>
          <el-button type="text">Users: {{ onlineUsers }}</el-button>
          <el-button type="primary" icon="el-icon-document" v-show="this.pdf_page_count > 0 && this.markMode" @click="showPDF = ! showPDF" size="mini" plain></el-button>
        </el-row>

        <div v-show="this.showPDF && this.pdf_page_count > 0 && this.markMode" class="pdf_div" style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding:2px; margin: 1px;">
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

        <div v-show="!markMode" style="position: static;z-index: 999999;" class="relation_table">
          <el-row style="background-color: #FFFFFF;border: 1px solid #dddddd; border-bottom: 0">
            <el-button type="text">TRIPLES</el-button>
            <el-button icon="el-icon-rank" @click="change_pos('relation_table')" style="padding: 10px; margin: 10px;" v-show="!this.markMode"></el-button>
            <el-row>
              <el-switch
                v-model="auto_rel"
                active-color="#13ce66"
                inactive-text="AUTO Relation"
              >
              </el-switch>
              <el-button type="primary" round @click="justAdd">Add</el-button>
            </el-row>


            <div class="relation_board" v-show="!markMode" style="background-color:#FFFFFF;padding: 8px;margin: 0px 5px;position: static;">
              <el-row>
                <el-button type="info" size="medium" plain style="width: 100%">Head: {{ this.single_triple['head']['word']}}</el-button>
              </el-row>
              <el-row v-show="!auto_rel">
                <el-button  type="info" size="medium" plain style="width: 100%">Relation: {{ this.single_triple['relation']['word']}}</el-button>
              </el-row>
              <el-row v-show="auto_rel">
                <el-button v-show="auto_rel" type="info" size="medium" plain style="width: 100%">Relation: AUTO</el-button>
              </el-row>
              <el-row>
                <el-button type="info" size="medium" plain style="width: 100%">Tail: {{ this.single_triple['tail']['word']}}</el-button>
              </el-row>
            </div>
          </el-row>

          <el-table
            class="tableClass"
            :data="relTable"
            stripe
            max-height="500px"
            style="width: 100%; text-align: center; font-size: 5px; border: 1px solid #dddddd; margin-bottom: 5px; "
            :row-style="{height:'8px'}" :cell-style="{padding:'5px 0'}">
            <el-table-column type="index" label="ID" width="40"></el-table-column>
            <el-table-column prop="head.word" label="HEAD" width="100"></el-table-column>
            <el-table-column prop="relation.word" label="RELATION" width="100"></el-table-column>
            <el-table-column prop="tail.word" label="TAIL" width="100"></el-table-column>
            <el-table-column label="Edit" width="45">
              <template slot-scope="scope">
                <el-button @click.native.prevent="deleteRel(scope.$index, relTable)" type="text" size="small" icon="el-icon-delete"></el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <el-table
          :data="tableData.slice((currentPage - 1) * pageSize, currentPage*pageSize)"
          border
          :highlight-current-row="true"
          :row-class-name="tableRowClassName"
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
              <el-button icon="el-icon-edit" type="primary" @click="editFile(scope.$index, scope.row)" size="mini" :loading="loadingNow"></el-button>
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
  //import jsPlumb from "jsplumb";
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
        single_triple: {'head': '', 'relation': '', 'tail': ''},
        relTable: [],
        auto_rel: true,

        autoMarkSelection: true,
        autoHint: true,
        hintList: {},

        logVis: false,
        logDirection: 'btt',
        logTable: [],

        onlineUsers: null,

        pdfUrl: '',
        pdf_cur_page: 1,
        pdf_page_count: 0,
        showPDF: false,

        activeNames: ['text_detail_0'],
        text_detail_ls :[],

        loadingNow:false,

        entityChanged: false,
        relationChanged: false,
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
          template: '<el-checkbox-group class="labelGroup" v-model="checkList" @change="click_check" :max="check_max" ' +
            'style="background-color: #FFFFFF; box-shadow: 0 0 5px #dddddd; padding: 8px;margin: 0 5px; position: static;">' + template_str +
            '<el-button icon="el-icon-rank" @click="change_pos" style="padding: 10px; margin: 10px;"></el-button></el-switch></el-checkbox-group>',
          data: function () {
            return {
              pos_fixed: true,
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
        this.labelIns.$mount(elementID);

      },

      gen_text_frame(text_ls_dict){
        this.text_detail_ls = [];
        for(let item in text_ls_dict){
          this.text_detail_ls.push(item);
        }
      },

      editFile(index, info){
        if(info['is_edit'] === 1){
          this.$notify({title: 'Warning', message: 'This file is being edited.', duration: 4000, type: 'warning'});
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
        this.gen_text_frame(JSON.parse(info['entity_list']));
        this.activeNames = ['text_detail_0'];
        this.see_PDF(info);
        this.showPDF = false;
        this.edit_fid = info['f_id'];
        this.edit_text = JSON.parse(info['text']);
        this.edit_entity_list = JSON.parse(info['entity_list']);
        this.raw_text = [];
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
        let hint_raw_ls = JSON.parse(info['hint']);
        for(let elementID in this.edit_entity_list){
          if(this.edit_entity_list.hasOwnProperty(elementID)){
            let tmp_entity_str_ls = this.edit_entity_list[elementID];
            let url_data = new FormData();
            url_data.append('string', 'aaa');
            this.$axios.post('/api/heart_beat', url_data).then(response => {
              this.hintList[elementID] = hint_raw_ls[elementID]
              this.removeRedundantHint(elementID);
              if(this.autoHint){
                tmp_entity_str_ls = tmp_entity_str_ls.concat(this.hintList[elementID]);
              }
              let decorated_text = this.genContent(tmp_entity_str_ls, this.edit_text[elementID]);
              this.display_content(decorated_text, elementID);
            }).catch(err => {
              this.hintList[elementID] = hint_raw_ls[elementID]
              this.removeRedundantHint(elementID);
              let decorated_text = this.genContent(tmp_entity_str_ls, this.edit_text[elementID]);
              this.display_content(decorated_text, elementID);
            });
          }
        }
        console.log('DETAIL:', info);
        this.relTable = JSON.parse(info['Mark_relation']);
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
          if(type.indexOf('auto-hint') > -1){
            let hint_color = '#9e9e9e';
            if(this.classNameList.indexOf(type.slice(type.lastIndexOf('-') + 1)) > -1){
              let color_pos = this.classNameList.indexOf(type.slice(type.lastIndexOf('-') + 1));
              hint_color = this.classColorList[color_pos];
            }else{
              if(type.indexOf('ithology') > -1){
                hint_color = '#8fff8e';
              }else if(type.indexOf('eriod') > -1) {
                hint_color = '#ff9474';
              }else if(type.indexOf('ocation') > -1) {
                hint_color = '#be74ff';
              }else if(type.indexOf('word') > -1) {
                hint_color = '#5fe2ff';
              }else{
                hint_color = '#9e9e9e';
              }
            }

            cur_content = cur_content.substring(0, startNum) + '<span class="auto-hint" style="cursor:' + 'pointer'+
              '; border-bottom:2px solid ' + hint_color + '; " data-startNum="' + startNum + '" data-endNum="' + endNum + '" data-word="' + word + '">'
              + cur_content.substring(startNum, endNum) + '</span>' + cur_content.substring(endNum);
          }
        }
        return cur_content;
      },

      autoHintMSG(){
        this.$notify.info({title: 'Message', message: 'Changes will take effect after re entering the edit page.'});
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
          this.$notify({title: 'Warning', message: 'There are other users editing.', type: 'warning'});
        }else{
          this.$confirm('Are you sure to leave?', 'Warning', {
            confirmButtonText: 'Yes',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }).then(() => {
            this.$router.push({path: '/home/class_manage',
              query: {p_id: this.$route.query.p_id, name: this.$route.query.name, path: this.$route.query.path, total: this.$route.query.total}});
          }).catch(() => {
          });
        }
      },

      showHelp(){
        let class_shortcuts = '';
        for(let i = 0; i < this.classNameList.length; i++){
          class_shortcuts += 'shift + ' + String(i + 1) +
            ': switch to class <strong><span style="color: ' + this.classColorList[i] + '">' + this.classNameList[i] + '</span></strong></br>';
        }
        this.$notify.info({
          title: 'Help(Shortcuts)',
          dangerouslyUseHTMLString: true,
          duration: 0,
          message:
            'shift + p: preview all marked entities</br>' +
            'shift + s: save changes</br>' +
            'shift + q: leave</br>' +
            'shift + h: change auto hint status</br>' +
            'shift + m: change auto mark status</br></br>' + class_shortcuts
        });
      },

      save(){
        if(this.edit_fid === null){
          this.$notify({title: 'Message', message: 'Nothing to Save', type: 'info'});
          return;
        }
        this.$confirm('Submit current changes?', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          if(this.entityChanged){
            let url_data = new FormData();
            url_data.append('f_id', this.edit_fid);
            url_data.append('entity_list', JSON.stringify(this.edit_entity_list));
            this.$axios.put('/api/update_entity_list', url_data).then(response => {
              this.tableData[this.edit_table_pos]['version']++;
              this.tableData[this.edit_table_pos]['entity_list'] = JSON.stringify(this.edit_entity_list);
              this.$notify({title: 'Success', message: 'Entity submitted successfully', type: 'success'});
              this.logTable.unshift({'Event': "Save", 'f_id': this.edit_fid, 'info': 'Save to database successfully',
                'entity_list_len': this.edit_entity_list.length});

              let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'entity_list': JSON.stringify(this.edit_entity_list),
                  'version': this.tableData[this.edit_table_pos]['version'], 'pos': this.edit_table_pos}, 'subject': 'save'}
              this.sendMessage(JSON.stringify(wsInfo));
              this.entityChanged = false;
            }).catch(err => {
              this.$notify.error({title: 'Error', message: err});
              this.logTable.unshift({'Event': "Save", 'f_id': this.edit_fid, 'info': 'Cannot Save to database',
                'entity_list_len': this.edit_entity_list.length});
            });
          }else{
            this.$notify.info({title: 'Message', message: 'No changes in entity list'});
          }

          if(this.relationChanged){
            let url_data = new FormData();
            url_data.append('f_id', this.edit_fid);
            url_data.append('relation_list', JSON.stringify(this.relTable));
            this.$axios.put('/api/update_relation_list', url_data).then(response => {
              this.$notify({title: 'Success', message: 'Relation submitted successfully', type: 'success'});
              let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'relation_list': JSON.stringify(this.relTable),
                  'pos': this.edit_table_pos}, 'subject': 'save_relation'}
              this.sendMessage(JSON.stringify(wsInfo));
              this.relationChanged = false;
            }).catch(err => {
              this.$notify.error({title: 'Error', message: err});
            });
          }else{
            this.$notify.info({title: 'Message', message: 'No changes in relation list'});
          }

        }).catch(() => {
        });
      },

      back2project(){
        this.$confirm('Are you sure to leave?', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.$router.push("/home/project_manage");
        }).catch(() => {
        });
      },

      count_str_len(text, str){
        let regex = new RegExp(str, 'g');
        let result = text.match(regex);
        return !result ? 0 : result.length
      },

      selectText(elementID){
        try{
          if(this.markMode === true){
            this.entityChanged = true;
            let element_id_int = parseInt(elementID.charAt(elementID.length-1));
            let selected=window.getSelection().toString();
            let selected_end_char = selected[selected.length - 1];
            selected = selected.trim();
            if(selected.length > 0){
              let range = window.getSelection().getRangeAt(0);
              let base = 0;
              let preElement = range.startContainer;
              while(preElement.previousSibling){
                base += preElement.previousSibling.textContent.length;
                preElement = preElement.previousSibling;
              }
              let start_num = Math.min(window.getSelection().anchorOffset, window.getSelection().focusOffset);
              let end_num = Math.max(window.getSelection().anchorOffset, window.getSelection().focusOffset);
              if(end_num - start_num === selected.length + 1 && selected_end_char === ' '){
                end_num = end_num - 1;
              }
              //console.log(base, this.raw_text, start_num, end_num, selected, selected.length)
              if((this.raw_text[element_id_int] || base > 0 || (!this.raw_text[element_id_int] && base === 0))
                && start_num < end_num && end_num - start_num === selected.length && this.checkList.length === 1){

                if(this.autoMarkSelection){
                  let marginChar = [',', '.', ':', ';', '?', '!', ' ', '(', ')', '>', '<', '"', '*', '%', '-', '_', '\n']
                  let selectedPosList = [];
                  let tmpPos = 0;
                  if(this.edit_text[elementID].indexOf(selected) < selected.length){
                    selectedPosList.push(this.edit_text[elementID].indexOf(selected));
                  }
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
                      if(marginChar.indexOf(this.edit_text[elementID][selectedPosList[i] - 1]) > -1 && marginChar.indexOf(this.edit_text[elementID][selectedPosList[i] + selected.length]) > -1 ||
                      selectedPosList[i] === 0 && marginChar.indexOf(this.edit_text[elementID][selectedPosList[i] + selected.length]) > -1){
                        this.edit_entity_list[elementID].push({'start': selectedPosList[i],
                          'end': selectedPosList[i] + selected.length, 'word': selected, 'type': this.checkList[0]});
                      }
                    }
                  }
                }else{
                  this.edit_entity_list[elementID].push({'start': base + start_num,
                    'end': base + end_num, 'word': selected, 'type': this.checkList[0]});
                }
                let tmp_entity_str_ls = this.edit_entity_list[elementID];
                if(this.autoHint){
                  this.removeRedundantHint(elementID);
                  tmp_entity_str_ls = tmp_entity_str_ls.concat(this.hintList[elementID]);
                }
                let decorated_text = this.genContent(tmp_entity_str_ls, this.edit_text[elementID]);
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

          }

        }catch(err){
          this.$message.error(err);
        }
      },

      clickEntity(elementID){
        if(this.markMode === true){
          this.entityChanged = true;
          let element_id_int = parseInt(elementID.charAt(elementID.length-1));
          let spanObj=document.elementFromPoint(event.clientX, event.clientY);
          let spanClass = spanObj.getAttribute("class");
          if(this.checkList.length === 1 && spanClass === this.checkList[0]) {
            let startNum = parseInt(spanObj.getAttribute("data-startNum"));
            let endNum = parseInt(spanObj.getAttribute("data-endNum"));
            let spanWord = spanObj.getAttribute("data-word");
            let cur_content = this.edit_text[elementID];
            for(let i = this.edit_entity_list[elementID].length-1; i >= 0; i--){
              if(this.autoMarkSelection){
                if(this.edit_entity_list[elementID][i]['end'] - this.edit_entity_list[elementID][i]['start'] === endNum - startNum
                  && this.edit_entity_list[elementID][i]['word'] === spanWord){
                  this.edit_entity_list[elementID].splice(i,1);
                }
              }else{
                if(this.edit_entity_list[elementID][i]['start'] === startNum && this.edit_entity_list[elementID][i]['end'] === endNum){
                  this.edit_entity_list[elementID].splice(i,1);
                }
              }

            }


            if(this.edit_entity_list[elementID].length === 0){this.raw_text[element_id_int] = true;}
            let tmp_entity_str_ls = this.edit_entity_list[elementID];
            if(this.autoHint){
              this.removeRedundantHint(elementID);
              tmp_entity_str_ls = tmp_entity_str_ls.concat(this.hintList[elementID]);
            }
            let decorated_text = this.genContent(tmp_entity_str_ls, cur_content);
            this.display_content(decorated_text, elementID);
            this.logTable.unshift({'Event': "Unmark", 'f_id': this.edit_fid,
              'info': 'Class: ' + spanClass + ', Start: ' + startNum + ', End: ' + endNum,
              'entity_list_len': this.count_entity_num()});
          }else if(this.checkList.length === 1 && spanClass === 'auto-hint'){//auto-hint
            let startNum = parseInt(spanObj.getAttribute("data-startNum"));
            let endNum = parseInt(spanObj.getAttribute("data-endNum"));
            let word = spanObj.getAttribute("data-word");
            let cur_content = this.edit_text[elementID];
            this.edit_entity_list[elementID].push({'start': startNum,
              'end': endNum, 'word': word, 'type': this.checkList[0]});
            this.removeRedundantHint(elementID);
            let tmp_entity_str_ls = this.edit_entity_list[elementID];
            tmp_entity_str_ls = tmp_entity_str_ls.concat(this.hintList[elementID]);
            let decorated_text = this.genContent(tmp_entity_str_ls, cur_content);
            this.display_content(decorated_text, elementID);
            this.raw_text[element_id_int] = false;
            this.logTable.unshift({'Event': "Mark", 'f_id': this.edit_fid,
              'info': 'Selected: ' + word + ', Start: ' + startNum + ', End: ' + endNum,
              'entity_list_len': this.count_entity_num()});
          }
        }else{
          let spanObj=document.elementFromPoint(event.clientX, event.clientY);
          let spanClass = spanObj.getAttribute("class");
          let startNum = parseInt(spanObj.getAttribute("data-startNum"));
          let endNum = parseInt(spanObj.getAttribute("data-endNum"));
          if(!isNaN(startNum) && spanClass !== 'auto-hint'){
            if(!this.auto_rel){
              console.log('Click Span: ' + spanObj.innerHTML + ' ' + startNum + ' ' + endNum + ' ' + spanClass);
              if(this.single_triple.head === ''){
                this.single_triple['head'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass, 'section': elementID};
              }else if(this.single_triple.head !== '' && this.single_triple.relation === ''){
                this.single_triple['relation'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass, 'section': elementID};
              }else{
                this.single_triple['tail'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass, 'section': elementID};
                this.relationChanged = true;
                this.relTable.push(this.single_triple);
                this.single_triple = {'head': '', 'relation': '', 'tail': ''};
              }
            }else{
              //auto rel
              console.log('Click Span: ' + spanObj.innerHTML + ' ' + startNum + ' ' + endNum + ' ' + spanClass);
              if(this.single_triple.head === ''){
                this.single_triple['head'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass, 'section': elementID};
              }else if(this.single_triple.head !== '' && this.single_triple.relation === ''){
                this.single_triple['relation'] = {'word': spanClass, 'start': -1, 'end': -1, 'type': spanClass, 'section': elementID};
                this.single_triple['tail'] = {'word': spanObj.innerHTML, 'start': startNum, 'end': endNum, 'type': spanClass, 'section': elementID};
                this.relationChanged = true;
                this.relTable.push(this.single_triple);
                this.single_triple = {'head': '', 'relation': '', 'tail': ''};
              }
            }

          }
        }
      },

      justAdd(){
        this.relTable.push(this.single_triple);
        this.single_triple = {'head': '', 'relation': '', 'tail': ''};
        this.relationChanged = true;
      },

      deleteRel(index, rows){
        rows.splice(index, 1);
        this.relationChanged = true;
      },

      change_pos(elementClass){
        let obj = document.getElementsByClassName(elementClass);
        if(obj.item(0).style.position === 'fixed'){
          obj.item(0).style.position='static';
        }else if(obj.item(0).style.position === 'static'){
          obj.item(0).style.position='fixed';
        }
      },

      change_status(pos, status, send_msg){
        if(this.edit_fid){
          let url_data = new FormData();
          url_data.append('f_id', this.edit_fid);
          url_data.append('status', status);
          this.loadingNow = true;
          this.$axios.put('/api/change_status', url_data).then(response => {
            this.tableData[pos]['is_edit'] = status;
            let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'status': status, 'pos': pos}, 'subject': 'lock'}
            if(send_msg){
              this.sendMessage(JSON.stringify(wsInfo));
            }
            this.loadingNow = false;
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
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

        if(info_data['subject'] === 'save_relation' && msg['p_id'] === this.p_id && msg['pos'] <= this.tableData.length){
          this.tableData[msg['pos']]['Mark_relation'] = msg['relation_list'];
          this.wsTable.unshift({'subject': 'Remote Info Sync', 'info': this.tableData[msg['pos']]['file_name'] + ' Relation Updated'});
        }

        if(info_data['subject'] === 'checked' && msg['p_id'] === this.p_id && msg['pos'] <= this.tableData.length){
          this.tableData[msg['pos']]['checked'] = msg['checked'];
          this.wsTable.unshift({'subject': 'Remote Info Sync', 'info': this.tableData[msg['pos']]['file_name'] + ' Checked Status Updated'});
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
        if(typeof(info['file_path']) === undefined){
          return;
        }
        let pdf_path = info['file_path'];
        pdf_path = btoa(encodeURIComponent(pdf_path));
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

      tableRowClassName({row, rowIndex}) {
        //console.log(row)
        if (row['checked'] === "0") {
          return 'warning-row';
        } else if (row['checked'] === "1") {
          return 'success-row';
        }
        return 'null-row';
      },

      update_check(f_id, flag){
        let url_data = new FormData();
        url_data.append('f_id', f_id);
        url_data.append('checked', flag);
        this.$axios.put('/api/update_file_check', url_data).then(response => {
          this.tableData[this.edit_table_pos]['checked'] = flag;
          let wsInfo = {'message': {'p_id': this.p_id, 'f_id': this.edit_fid, 'pos': this.edit_table_pos, 'checked': flag}, 'subject': 'checked'}
          this.sendMessage(JSON.stringify(wsInfo));
        }).catch(err => {
          this.$notify.error({title: 'Error', message: err});
        });
      },

    },

    created() {
      this.init_page();
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
        if(this.keydown === 'shift+s') {
          this.keydown = '';
          that.save();
        }else if(this.keydown === 'shift+p') {
          this.keydown = '';
          that.see_all();
        }else if(this.keydown === 'shift+q') {
          this.keydown = '';
          that.back2project();
        }else if(this.keydown === 'shift+m') {
          this.keydown = '';
          that.autoMarkSelection = !that.autoMarkSelection;
        }else if(this.keydown === 'shift+h'){
          this.keydown = '';
          that.autoHint = !that.autoHint;
        }else if(digitalShift.indexOf(this.keydown[this.keydown.length - 1]) > -1){
          let keyPos = digitalShift.indexOf(this.keydown[this.keydown.length - 1]);
          this.keydown = '';
          if(keyPos <= that.classNameList.length){
            if(that.classNameList[keyPos] !== undefined){
              this.checkList = [that.classNameList[keyPos]];
              that.labelIns.checkList = this.checkList;
              that.labelIns.click_check();
              this.keydown = '';
              that.$notify({title: that.classNameList[keyPos], message: 'You have switched to class ' + that.classNameList[keyPos] + '.', type: 'success'
              });
            }
          }
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
