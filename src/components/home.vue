<template>
  <el-container class="container">
    <!-- 头部 -->
    <el-header>
      <h1>Easy Label</h1>
    </el-header>
    <el-container>
      <!-- aside -->
      <el-aside width="200px">
        <left />
      </el-aside>
      <!-- main -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  import left from "@/components/left.vue";

  export default {
    name: "home",
    components: {
      left
    },
    data() {
      return {
        fits: ["fill", "contain", "cover", "none", "scale-down"]
      };
    }
  };
</script>
<style scoped>
  .el-container {
    margin-bottom: 40px;
  }
  .container {
    height: 600px;
  }
  .el-header {
    text-align: left;
    background-color: #e0e0e0;
  }
  .el-main {
    background-color: #e9eef3;
    text-align: center;
    padding: 0;
  }
  .el-aside{
    background-color: #e0e0e0;
  }
</style>
