<template>
  <div id="app">
    <img class="company-logo" alt="Britecore logo" src="./assets/logo.png">
    <RiskManagement/>
  </div>
</template>

<script>
import RiskManagement from './components/RiskManagement.vue'

export default {
  name: 'app',
  components: {
    RiskManagement,
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
  margin-top: 60px;
}
.company-logo {
  height: 40px;
};
</style>
