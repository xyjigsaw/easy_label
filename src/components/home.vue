<template>
  <el-container class="container_all">
    <!-- 头部 -->
    <el-header>
      <h1 style="color: #409EFF">Easy Mark</h1>
    </el-header>
    <el-container class="container_main">
      <!-- aside menu-->
      <el-menu class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
        <el-menu-item index="5" @click="navDashboard">
          <i class="el-icon-star-off"></i>
          <span slot="title">Home</span>
        </el-menu-item>

        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-folder-opened"></i>
            <span>Project</span>
          </template>
          <el-menu-item index="1-1" @click="navProject">
            <i class="el-icon-folder-opened"></i>
            <span slot="title">Mark</span>
          </el-menu-item>

          <el-menu-item index="1-2" @click="navFigure">
            <i class="el-icon-folder-opened"></i>
            <span slot="title">Figure</span>
          </el-menu-item>
          <el-menu-item index="1-3" @click="navQANER">
            <i class="el-icon-folder-opened"></i>
            <span slot="title">QA_NER</span>
          </el-menu-item>
        </el-submenu>

        <el-menu-item index="2" @click="navHelp">
          <i class="el-icon-question"></i>
          <span slot="title">Help</span>
        </el-menu-item>
        <el-menu-item index="3" @click="navResearcher">
          <i class="el-icon-share"></i>
          <span slot="title">Researcher</span>
        </el-menu-item>
        <el-menu-item index="4" @click="isCollapse = !isCollapse">
          <i class="el-icon-caret-right" v-if="isCollapse"></i>
          <span slot="title" v-if="isCollapse">Unfold</span>
          <i class="el-icon-caret-left" v-if="!isCollapse"></i>
          <span slot="title" v-if="!isCollapse">Hide</span>
        </el-menu-item>
      </el-menu>
      <!-- main -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
    <el-footer height="10px"><span style="color: #b3b3b3; font-size: 12px;"> </span></el-footer>
  </el-container>
</template>

<script>
  export default {
    name: "home",
    data() {
      return {
        isCollapse: false,
      };
    },
    created() {
      //this.$router.push("/home/dashboard");
    },
    methods: {
      handleOpen(key, keyPath) {
        //console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        //console.log(key, keyPath);
      },
      navProject(){
        this.$router.push("/home/project_manage");
      },
      navFigure(){
        this.$router.push("/home/figures");
      },
      navHelp(){
        this.$router.push("/home/help");
      },
      navResearcher(){
        this.$router.push("/home/researcher_beta");
      },
      navDashboard(){
        this.$router.push("/home/dashboard");
      },
      navQANER(){
        this.$router.push("/home/qa_ner");
      }
    }
  };
</script>
<style scoped>
  .el-container {
    margin-bottom: 10px;
  }
  .container_main {
    height: calc(90vh);
  }
  .el-header {
    text-align: left;
    background-color: #FFFFFF;
  }
  .el-main {
    background-color: #e9eef3;
    text-align: center;
    padding: 0;
  }
  .el-menu-vertical-demo{
    text-align: left;
    background-color: #FFFFFF;
    font-size: large;
    font-weight: bolder;
  }

  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
    min-width: 200px;

  }
  .el-menu--collapse {
    min-width: 64px;
  }
</style>
