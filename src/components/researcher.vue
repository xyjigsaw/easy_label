<template>
  <div>
    <el-button type="primary" @click="navREntity">Entity</el-button>
    <el-button type="success" @click="navRRelation">Relation</el-button>
    <el-button type="warning" @click="navRBeta">BETA</el-button>
  </div>
</template>

<script>
export default {
  name: "researcher",
  data(){
    return{

    }
  },
  methods:{
    navREntity(){
      this.$router.push("/home/researcher_entity");
    },

    navRRelation(){
      this.$router.push("/home/researcher_relation");
    },

    navRBeta(){
      this.$router.push("/home/researcher_beta");
    },
  },
}
</script>

<style scoped>

</style>
