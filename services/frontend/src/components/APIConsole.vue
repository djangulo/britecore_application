<template>
  <div class="api-data">
    {{ log }}
  </div>
</template>

<script>
export default {
  name: 'APIConsole',
  props: {
    log: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.api-data {
  overflow-y: scroll;
}
</style>
