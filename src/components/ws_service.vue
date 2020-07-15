<template>
  <div>
    <h1>WebSocket Chat</h1>
    <el-button type="primary" plain @click="sendMessage">Submit</el-button>
    <el-input v-model="input_text" placeholder="请输入内容"></el-input>
    <div id='messages'>
    </div>

  </div>
</template>

<script>
  export default {
    data() {
      return {
        ws: null,
        name: 0,
        input_text: '',
      };
    },
    methods: {
      init() {

        this.ws = new WebSocket(this.$route.meta.ws_port);
        this.ws.onmessage = this.getMessage;

      },

      getMessage(msg) {
        document.getElementById('messages').innerHTML = msg.data;
        console.log(msg);
      },

      sendMessage() {
        this.ws.send(this.input_text)
        this.input_text = ''
      }

    },
    created() {
      this.init();
    }
  };
</script>

<style scoped>
</style>
