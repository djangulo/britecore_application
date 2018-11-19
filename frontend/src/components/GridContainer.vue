<template>
  <div class="main">
    <h1 class="text-center">Welcome to my BriteCore application project!</h1>
    <p class="text-center">Thank you for taking the time to review my project.</p>
    <p class="text-center">Here is the <a href="https://github.com/djangulo/britecore_application/" target="_blank" rel="noopener">link to the github repository.</a></p>
    <Alert />
    <div class="grid">
      <RiskList />
      <!-- <RiskForm v-show="selectedRisk !== null"/> -->
      <NewRiskForm />
      <DbForm v-if="selectedRisk !== null"/>
      <div class="third-col">
        <Console />
        <DbTables />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Alert from './Alert.vue'
import Console from './Console.vue'
import NewRiskForm from './NewRiskForm.vue'
import RiskList from './RiskList.vue'
import DbForm from './DbForm.vue'
import DbTables from './DbTables.vue'
export default {
  name: 'GridContainer',
  components: {
    Alert,
    Console,
    DbForm,
    NewRiskForm,
    RiskList,
    DbTables
  },
  computed: {
    ...mapGetters('risks', {
      risks: 'availableRisks',
      selectedRisk: 'selectedRisk',
    }),
  },
}
</script>

<style>
.grid {
  display: flex;
  flex-direction: column;
}
@media screen and (min-width: 760px) {
  .grid {
    display: grid;
    grid-template-columns: 0.4em repeat(2, 1fr)  2fr 0.4em;
    grid-template-rows: repeat(2, max-content);
  }
  .third-col {
    grid-column: 4 / 5;
    grid-row: 1 / -1;
  }
}
h1 {
  margin-top: 0;
}
h3 {
  margin: 0.2em 0 0;
}
h5 {
  margin-left: 0.3em;
}
ul {
  padding: 0;
}
li {
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
