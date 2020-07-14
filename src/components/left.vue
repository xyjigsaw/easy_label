<template>
  <div>
    <!-- 菜单组件 -->
    <el-menu default-active="0" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">

      <!-- 子菜单：用户管理 -->
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>Project</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="11" @click="navProject">Add Project</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group>
          <el-menu-item index="12" @click="navClass">Class</el-menu-item>
        </el-menu-item-group>
      </el-submenu>

    </el-menu>

  </div>
</template>

<script>
  export default {
    data() {
      return {

      };
    },
    methods: {
      handleOpen(key, keyPath) {
        //console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        //console.log(key, keyPath);
      },
      navClass(){
        this.$router.push("/home/class_manage");
      },
      navProject(){
        this.$router.push("/home/project_manage");
      }
    }
  };
</script>

<style scoped>
</style>
