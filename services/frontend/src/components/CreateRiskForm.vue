<template>
  <form class="form" v-bind="form" v-on:submit.prevent="submitForm">
    <label for="risk-name">Risk name
      <input type="text" name="risk-name" v-model="name">
    </label>
    <div v-for="(field, i) in fields" :key="i" class="field-input-group">
      <select name="data_type" v-model="fields[i].data_type">
        <option value="0">Text</option>
        <option value="1">Number</option>
        <option value="2">Date</option>
        <option value="3">Enum</option>
      </select>
      <label>Field name
        <input type="text" v-model="fields[i].name">
      </label>
    </div>
    <br>
    <button type="button" class="button" @click="addField">Add field</button>
    <button type="submit" class="button" >Submit</button>
  </form>
</template>

<script>
const axios = require('axios')
export default {
  name: 'CreateRiskForm',
  props: {
    msg: String
  },
  data () {
    return {
      fields: [],
      name: ''
    }
  },
  methods: {
    addField: function() {
      this.fields.push({
        data_type: 0,
        name: '',
      })
    },
    submitForm: function() {
      const formData = new FormData()
      formData.append('name', this.name)
      axios
        .post('http://0.0.0.0:8000/api/v1.0/risks/', formData)
        .then(response => this.$emit('api-data', response.data))
        .catch(err => this.$emit('api-data', err))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.form {
  text-align: left;
  padding-left: 0.5em;
}
.api-console,
.sql-console {
  background: #313131;
  color: #e2e2e2;
  height: 100%;
  width: 100%;
}
</style>
