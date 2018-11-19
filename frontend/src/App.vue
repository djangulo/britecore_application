<template>
  <div id="app">
    <GridContainer />
  </div>
</template>

<script>
import GridContainer from './components/GridContainer.vue'

export default {
  name: 'app',
  components: {
    GridContainer
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0.2em;
}
</style>
