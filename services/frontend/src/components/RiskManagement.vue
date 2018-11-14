<template>
  <div class="risk-app">
    <h1>Welcome to my BriteCore application project!</h1>
    <p>Thank you for taking the time to review my project.</p>
    <div class="grid">
      <div class="left">
        <h3>Create a risk policy</h3>
        <CreateRiskForm v-on:api-data="this.api_data = $event"/>
      </div>
      <div class="center">
        <h3>API Form</h3>
        <APIForm />
      </div>
      <div class="right-top">
        <h3>API Console</h3>
        <APIConsole log="api_data"/>
      </div>
      <div class="right-bottom">
        <h3>SQL Console</h3>
        <SQLConsole />
      </div>
    </div>
  </div>
</template>

<script>
import CreateRiskForm from './CreateRiskForm.vue'
import SQLConsole from './SQLConsole.vue'
import APIConsole from './APIConsole.vue'
import APIForm from './APIForm.vue'
export default {
  name: 'RiskManagement',
  props: {
    msg: String
  },
  components: {
    CreateRiskForm,
    SQLConsole,
    APIConsole,
    APIForm
  },
  data () {
    return {
      api_data: ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  column-gap: 5px;
  row-gap: 5px;
}
.left {
  grid-row: 1 / -1;
  grid-column: 1 / 2;
}
.center {
  grid-row: 1 / -1;
  grid-column: 2 / 3;
}
.right-top,
.right-bottom {
  grid-row: 1 / 2;
  grid-column: -2 / -1;
}
.right-bottom {
  grid-row: 2 / 3;
}
.left,
.center,
.right-bottom,
.right-top {
  border: 1px solid black;
  min-height: 35vh;
}
h3 {
  margin: 0.6em 0 ;
}
.api-console,
.sql-console {
  background: #313131;
  color: #e2e2e2;
  height: 100%;
  width: 100%;
}
</style>
