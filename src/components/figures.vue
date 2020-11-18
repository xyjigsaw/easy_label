<template>
  <div>
    <div class="buttons" style="width: 50%; text-align: center; margin: auto">
    <el-row style="margin: 10px;">
      <el-col :span="3">
        <el-button type="danger" icon="el-icon-back" circle @click="back2home"></el-button>
        <p style="font-size: 8px; color: #F56C6C; text-align: center; margin: 0;">Exit</p>
      </el-col>
      <el-col :span="3">
        <el-button type="info" icon="el-icon-question" circle @click="showHelp"></el-button>
        <p style="font-size: 8px; color: #909399; text-align: center; margin: 0;">Help</p>
      </el-col>

      <el-col :span="5">
        <el-button type="primary" @click="query_img(pre_figure_id)">Back</el-button>
      </el-col>

      <el-col :span="5">
        <el-button type="success" icon="el-icon-check" @click="save">Save</el-button>
      </el-col>

      <el-col :span="5">
        <el-button type="warning" @click="get_img">Random</el-button>
      </el-col>

      <el-col :span="3">
        <el-switch
          style="display: block; margin-top: 10px;"
          v-model="auto_next"
          active-color="#13ce66">
        </el-switch>
        <p style="font-size: 8px; text-align: center; margin: 0; color: #606266">Fast Mark</p>
      </el-col>
    </el-row>
    </div>
    <div id="class_ls">

    </div>
    <div class="demo-image__lazy" style="width: 60%;text-align: center; margin: auto; padding:20px; background-color: #FFFFFF;
    box-shadow: 0 0 2px #FFFFFF; border-radius: 5px;">
      <el-row>
        <el-col :span="8">
          <span id="figure_id" style="background-color: #cecece; margin: 20px; padding: 10px;
          font-weight: bolder; line-height: 20px; font-size: 20px; color: #2c3e50; border-radius: 5px;"></span>
        </el-col>
        <el-col :span="8">
          <span id="version" style="background-color: #cecece; margin: 20px; padding: 10px;
          font-weight: bolder; line-height: 20px; font-size: 20px; color: #2c3e50; border-radius: 5px;"></span>
        </el-col>
        <el-col :span="8">
          <span id="label" style="background-color: #cecece; margin: 20px; padding: 10px;
          font-weight: bolder; line-height: 20px; font-size: 20px; color: #2c3e50; border-radius: 5px;"></span>
        </el-col>
      </el-row>
      <br>
      <el-row>
        <span id="caption" style="padding: 10px; font-weight: bolder; line-height: 30px; font-size: 25px; color: #2c3e50;"></span>
      </el-row>
      <el-row>
        <el-image :src="img_path" lazy style="padding: 5px;margin: 10px;"></el-image>
      </el-row>

    </div>
  </div>
</template>

<script>
import Vue from "vue";

export default {
  name: "figures",
  data() {
    return {
      figure_id: '',
      pre_figure_id: '',
      img_path: '',
      classNameList: [],
      classColorList: [],
      labelIns: null,
      checkList: [],
      check_max: 1,
      auto_next: false,
    }
  },
  created() {
    this.get_class()
    this.get_img();

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
      }else if(this.keydown === 'shift+q') {
        this.keydown = '';
        that.back2project();
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

  methods: {
    get_class(){
      this.$axios.get('/api/fetch_figure_class').then(response => {
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
      }).catch(err => {
        this.$notify.error({title: 'Error', message: err});
      });
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
          'style="padding: 8px;margin: 0 5px; position: static;">' + template_str +
          '</el-switch></el-checkbox-group>',
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
        }
      });

      this.labelIns = new classLabel();
      this.labelIns.$mount(elementID);

    },

    click_check(){

    },

    get_img(){
      this.pre_figure_id = this.figure_id;
      this.$axios.get('/api/fetch_rand_figure').then((response)=> {
        console.log(response.data['data'][0]);
        this.figure_id = response.data['data'][0]['figure_id'];
        let img_path = response.data['data'][0]['image_path'];
        if(img_path.indexOf('dkvl') > -1){
          img_path = img_path.substring(img_path.indexOf('/dkvl/var/www/ner-api/') + '/dkvl/var/www/ner-api/'.length);
        }
        this.img_path = this.$route.meta.img_port + btoa(encodeURIComponent(img_path));
        document.getElementById("caption").innerHTML = response.data['data'][0]['text'];
        document.getElementById("figure_id").innerHTML = 'ID: ' + response.data['data'][0]['figure_id'];
        document.getElementById("version").innerHTML = 'Version: ' + response.data['data'][0]['version'];
        if(response.data['data'][0]['label'] == null) {
          document.getElementById("label").innerHTML = 'Label: NULL';
          document.getElementById("label").style.color = '#2c3e50';
        }else{
          document.getElementById("label").innerHTML = 'Label: ' + response.data['data'][0]['label'];
          document.getElementById("label").style.color = this.classColorList[this.classNameList.indexOf(response.data['data'][0]['label'])];
        }
        this.checkList = [];
        this.labelIns.checkList = [];
      }).catch((err)=> {
        this.$notify.error({title: 'Error', message: err});
      });
    },

    query_img(query_id){
      if(this.pre_figure_id !== ''){
        let url_data={
          figure_id: query_id,
        };
        this.$axios.get('/api/fetch_figure', {params: url_data}).then((response)=> {
          console.log(response.data['data'][0]);
          this.figure_id = response.data['data'][0]['figure_id']
          this.img_path = this.$route.meta.img_port + btoa(encodeURIComponent(response.data['data'][0]['image_path']));
          document.getElementById("caption").innerHTML = response.data['data'][0]['text'];
          document.getElementById("figure_id").innerHTML = 'ID: ' + response.data['data'][0]['figure_id'];
          document.getElementById("version").innerHTML = 'Version: ' + response.data['data'][0]['version'];
          if(response.data['data'][0]['label'] == null) {
            document.getElementById("label").innerHTML = 'Label: NULL';
            document.getElementById("label").style.color = '#2c3e50';
          }else{
            document.getElementById("label").innerHTML = 'Label: ' + response.data['data'][0]['label'];
            document.getElementById("label").style.color = this.classColorList[this.classNameList.indexOf(response.data['data'][0]['label'])];
          }
          this.checkList = [];
          this.labelIns.checkList = [];
        }).catch((err)=> {
          this.$notify.error({title: 'Error', message: err});
        });
      }else{
        this.$notify({title: 'Warning', message: 'Noting', type: 'warning'});
      }
    },

    save(){
      if(!this.auto_next){
        this.$confirm('Submit current changes?', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          if(this.checkList.length === 1){
            let url_data = new FormData();
            url_data.append('figure_id', this.figure_id);
            url_data.append('figure_class', this.checkList[0]);
            this.$axios.put('/api/update_figure_class', url_data).then(response => {
              this.$notify({title: 'Success', message: 'Submitted successfully', type: 'success'});
              document.getElementById("label").style.color = this.classColorList[this.classNameList.indexOf(this.checkList[0])];
            }).catch(err => {
              this.$notify.error({title: 'Error', message: err});
            });
          }else{
            this.$notify({title: 'Warning', message: 'Noting to save', type: 'warning'});
          }
        }).catch(() => {});
      }else{
        if(this.checkList.length === 1){
          let url_data = new FormData();
          url_data.append('figure_id', this.figure_id);
          url_data.append('figure_class', this.checkList[0]);
          this.$axios.put('/api/update_figure_class', url_data).then(response => {
            this.$notify({title: 'Success', message: 'Submitted successfully', type: 'success'});
            document.getElementById("label").style.color = this.classColorList[this.classNameList.indexOf(this.checkList[0])];
            this.get_img();
          }).catch(err => {
            this.$notify.error({title: 'Error', message: err});
          });
        }else{
          this.$notify({title: 'Warning', message: 'Noting to save', type: 'warning'});
        }
      }

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
          'shift + s: save changes</br>' +
          'shift + q: leave</br>' + class_shortcuts
      });
    },

  },


}
</script>

<style scoped>

</style>
