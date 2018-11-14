<template>
  <div class="sql-console"></div>
</template>

<script>
export default {
  name: 'SQLConsole',
  props: {
    log: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.sql-console {
  background: #313131;
  color: #e2e2e2;
  height: 200px;
  width: 200px;
}
</style>
