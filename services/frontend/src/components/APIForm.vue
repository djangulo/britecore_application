<template>
  <div class="risks">
    <p>{{ err }}</p>
    <ul>
    <li v-for="(risk, i) in availableRisks" :key="i">{{ risk.name }}</li>
    </ul>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  name: 'APIForm',
  props: {
    msg: String
  },
  data () {
    return {
      availableRisks: null,
      err: ''
    }
  },
  mounted () {
    axios
      .get('http://localhost:8000/api/v1.0/risks/')
      .then(response => (this.availableRisks = response.data))
      .catch(err => this.err = err)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
