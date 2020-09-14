<template>
  <div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span><strong>Help</strong></span>
      </div>
      <div class="list" style="font-size: large;">
        <ul>
          <h2>Start</h2>
          <li>a: upload <strong>ZIP</strong> compressed papers</li>
          <li>b: add entity class(label)</li>
          <li>c: click <i class="el-icon-edit"></i> in the table on the right to start marking</li>
          <li>d: use the mouse to select and mark</li>
          <li>e: click the marked block to remove</li>
          <h2>Shortcuts</h2>
          <li>shift + p: preview all marked entities</li>
          <li>shift + s: save changes</li>
          <li>shift + q: leave</li>
          <li>shift + h: change auto hint status</li>
          <li>shift + m: change auto mark status</li>
          <li>shift + [1, 2, 3, 4, ...]: switch to the ith label</li>
          <h2>Features</h2>
          <li>auto hint: recognize potential entities which will be <span style="border-bottom:2px solid #ff5858;">underlined</span> in red</li>
          <li>auto mark: recognize and mark all identical entities after selection</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
name: "help"
}
</script>

<style>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
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
  width: auto;
}
.list {
  text-align: left;
}
</style>
