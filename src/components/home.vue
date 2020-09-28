<template>
  <el-container class="container">
    <!-- 头部 -->
    <el-header>
      <h1 style="color: #409EFF">Easy Mark</h1>
    </el-header>
    <el-container>
      <!-- aside menu-->
      <el-menu class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
        <el-menu-item index="5" @click="navDashboard">
          <i class="el-icon-star-off"></i>
          <span slot="title">Home</span>
        </el-menu-item>
        <el-menu-item index="1" @click="navProject">
          <i class="el-icon-folder-opened"></i>
          <span slot="title">Project</span>
        </el-menu-item>
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
      this.$router.push("/home/dashboard");
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
      navHelp(){
        this.$router.push("/home/help");
      },
      navResearcher(){
        this.$router.push("/home/researcher");
      },
      navDashboard(){
        this.$router.push("/home/dashboard");
      }
    }
  };
</script>
<style scoped>
  .el-container {
    margin-bottom: 40px;
  }
  .container {
    height: 1000px;
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
