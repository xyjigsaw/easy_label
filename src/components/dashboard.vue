<template>
  <div>
    <el-card class="box-card" style="width: 40%;">
      <div slot="header" class="clearfix">
        <h2>Notification</h2>
      </div>
      <div class="text item">
        <strong>Last  Updated: 20201118</strong><br>
        <h2>New Features</h2>
        <li>DDEKG-oriented marking</li>
        <li>DDE_Figure-oriented marking</li>
        <li>Paper entity and relation marking</li>
        <li>Researcher entity and relation marking</li>
        <li>Sections can be collapsed.</li>
        <li>Auto Hint</li>
        <li>Auto Mark</li>
        <li>Shortcuts for switching labels</li>

      </div>
    </el-card>

    <el-card class="box-card" style="width: 40%;">
      <div slot="header" class="clearfix">
        <h2>Start</h2>
      </div>
      <div class="text item">
        <el-button type="primary" @click="navProject">Main Project</el-button>
        <el-button type="primary" @click="navFigure">Figures</el-button>
        <el-button type="primary" @click="navqa_NER">QA_NER</el-button>
        <br><br>
        <el-button type="success" @click="navREntity">Researcher Entity</el-button>
        <el-button type="success" @click="navRRelation">Researcher Relation</el-button>
        <br><br>
        <el-button type="info" @click="navHelp">Help</el-button>
        <el-button type="warning" disabled>Feedback</el-button>

      </div>
    </el-card>

  </div>
</template>

<script>
export default {
name: "dashborad",
  data(){
    return{

    };
  },
  methods:{
    navProject(){
      this.$router.push("/home/project_manage");
    },
    navHelp(){
      this.$router.push("/home/help");
    },
    navREntity(){
      this.$router.push("/home/researcher_entity");
    },
    navRRelation(){
      this.$router.push("/home/researcher_relation");
    },

    navFigure(){
      this.$router.push("/home/figures");
    },

    navqa_NER(){
      this.$router.push("/home/qa_ner");
    },
  },
}
</script>

<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
  text-align: left;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}

.box-card {
  float: left;
  padding: 10px;
  margin:20px;
}
</style>
