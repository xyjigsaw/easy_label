<template>
  <div>
    <el-card class="box-card" style="width: 60%;">
      <div slot="header" class="clearfix">
        <span>Notification</span>
      </div>
      <div class="text item">
        <li>Features</li>
        <li>Functions</li>
      </div>
    </el-card>

    <el-card class="box-card" style="width: 30%;">
      <div slot="header" class="clearfix">
        <span>Start</span>
      </div>
      <div class="text item">
        <el-button type="success" @click="navProject">Project</el-button>
        <el-button type="info" @click="navHelp">Help</el-button>
        <el-button type="primary" disabled>Feedback</el-button>

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
