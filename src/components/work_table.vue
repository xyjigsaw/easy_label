<template>
  <div>
    <el-container>
      <el-main style="padding: 0;">

        <el-row :gutter="12" type="flex" justify="center" style="padding: 10px;">
          <el-col :span="6"><div class="grid-content bg-purple">
            <el-button icon="el-icon-search" circle @click="see_all"></el-button>
            <p style="font-size: 8px; color: #606266; text-align: center">Preview</p>
          </div></el-col>
          <el-col :span="6"><div class="grid-content bg-purple">
            <el-button type="success" icon="el-icon-check" circle @click="save"></el-button>
            <p style="font-size: 8px; color: #67C23A; text-align: center">Save</p>
          </div></el-col>
        </el-row>

        <div id="class_ls">
        </div>



        <div id="operation">
          <div id="text_detail" @mouseup='selectText' @click='deleteEntity'></div>
        </div>
      </el-main>

      <el-aside width="320px" style="background-color: #42b983">
        <el-table
          :data="tableData.slice((currentPage - 1) * pageSize, currentPage*pageSize)"
          border
          small
          max-height="600"
          style="width: 100%; font-size: 10px">
          <el-table-column fixed prop="file_name" label="Name"></el-table-column>
          <el-table-column fixed prop="version" label="Ver." width="48"></el-table-column>
          <el-table-column fixed prop="is_edit" label="Lock" width="48"></el-table-column>

          <el-table-column
            fixed="right"
            label="Edit"
            width="50">
            <template slot-scope="scope">
              <el-button @click="editFile(scope.row)" type="text" size="small">Tag</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="partition" style="margin-top:15px;">
          <el-pagination align='center'
                         @next-click="handleNextClick"
                         :current-page.sync="currentPage"
                         :page-size="pageSize"
                         layout="total, prev, next"
                         :total="parseInt(total)">
          </el-pagination>
        </div>

      </el-aside>
    </el-container>
  </div>
</template>

<script>
  import Vue from 'vue'
  export default {
    data() {
      return {
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
        check_max: 10,

        edit_cid: null,
        edit_text: '',
        edit_entity_list: [],
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
          this.$notify.error({
            title: 'Error',
            message: err
          });
        });
      },

      init_page() {
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
                this.$router.push({path: '/home/class_manage', query: {p_id: this.$route.query.p_id, name: this.$route.query.name, path: this.$route.query.path}});
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
            this.checkList = this.classNameList;
            this.check_max = this.classNameList.length;
            this.gen_labels(class_str, '#class_ls');

            this.lazy_fetch_file(0);

          }
        }).catch(err => {
          this.$notify.error({
            title: 'Error',
            message: err
          });
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
          template: '<el-checkbox-group v-model="checkList" @change="click_check" :max="check_max">' + template_str +
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

      editFile(info){
        console.log(info['f_id']);
        //for content

        this.edit_cid = info['f_id'];
        this.edit_text = info['text'];
        this.edit_entity_list = eval(info['entity_list']);

        let decorated_text = this.genContent(this.edit_entity_list, this.edit_text);
        document.getElementById("text_detail").innerHTML="<div style=\"box-shadow: 0 0 2px #b1b1b1; margin: 10px; padding:20px; border-radius: 5px; " +
          "line-height: 30px;\">" + decorated_text + "</div>";
      },

      sort_entity(a, b){
        return a.start - b.start;
      },

      genContent(entity_str_ls, cur_content){
        entity_str_ls.sort(this.sort_entity);
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
      },

      save(){

      },

      selectText(){
        try{
          let selected=window.getSelection().toString();
          if(selected != null){
            let base = 0;
            let raw_flag = false;
            let container = window.getSelection().getRangeAt(0).startContainer;
            while(container.previousSibling){
              base += container.previousSibling.textContent.length;
              container = container.previousSibling;
            }
            if(!container.previousSibling){
              raw_flag = true;
            }
            let anchorOffset = window.getSelection().anchorOffset;
            let focusOffset = window.getSelection().focusOffset;
            let start_num = Math.min(anchorOffset, focusOffset);
            let end_num = Math.max(anchorOffset, focusOffset);
            if(raw_flag || (base > 0 && start_num < end_num && end_num - start_num === selected.length && this.checkList.length === 1)){


              console.log('Selected text: ' + selected);
              console.log(start_num, end_num);


              this.edit_entity_list.push({'start': base + start_num,
                'end': base + end_num, 'word': selected, 'type': this.checkList[0]});

              console.log(this.edit_entity_list);


              let decorated_text = this.genContent(this.edit_entity_list, this.text);

              console.log(decorated_text);
              document.getElementById("text_detail").innerHTML="<div style=\"box-shadow: 0 0 2px #b1b1b1; margin: 10px; padding:20px; border-radius: 5px; " +
                "line-height: 30px;\">" + decorated_text + "</div>";

            }else if(base === 0 && this.checkList.length === 1){
              return;
            }else{
              return;
            }
          }else{
            return;
          }
        }catch(err){
          this.$message.error(err);
        }
      },
      deleteEntity(){

      },



    },

    created() {
      this.init_page();
    }
  };
</script>

<style scoped>

</style>
