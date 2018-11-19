<template>
  <form @submit.prevent="onSubmit" class="db-form text-left">
    <b-card v-bind="{ title: selectedRisk.name, 'sub-title': selectedRisk.description }">
      <b-row v-for="(field, i) in selectedRisk.fields" :key="i" class="my-1">
        <b-col sm="4"><label v-bind="{ for: `input-${i}`, id: `input-${i}-label` }"><small>{{ field.name }}</small></label></b-col>
        <b-col sm="8">
          <b-form-input v-if="field.data_type == 0"
            id="input-small" 
            size="sm" 
            type="text" 
            v-bind="{ description: field.help_text !== '' ? `e.g. ${field.help_text}` : null, id: `input-${i}`, 'aria-describedby': `input-${i}-label` }" 
            v-model="formValues[field.name]"></b-form-input>
          <b-form-input v-if="field.data_type == 1"
            id="input-small" 
            size="sm" 
            type="number" 
            v-bind="{ description: field.help_text !== '' ? `e.g. ${field.help_text}` : null, id: `input-${i}`, 'aria-describedby': `input-${i}-label` }" 
            v-model="formValues[field.name]"></b-form-input>
          <Datepicker 
            v-if="field.data_type == 2" 
            input-class="form-control" 
            v-bind="{ id: `input-${i}`, 'aria-describedby': `input-${i}-label` }" typeable
            v-model="formValues[field.name]"></Datepicker>
          <b-form-select v-if="field.data_type == 3"
            id="input-small" 
            size="sm" 
            type="number" 
            :options="parseOptions(field.enum_options)" 
            v-bind="{ description: field.help_text !== '' ? `e.g. ${field.help_text}` : null, id: `input-${i}`, 'aria-describedby': `input-${i}-label` }" 
            v-model="formValues[field.name]"></b-form-select>
        </b-col>
      </b-row>
      <b-btn variant="outline-primary" type="submit">Create</b-btn>
      <b-btn variant="outline-warning" type="button" @click="onReset">Clear</b-btn>
    </b-card>
  </form>
</template>

<script>
import { mapGetters } from 'vuex'
import Datepicker from 'vuejs-datepicker'
export default {
  name: 'DbForm',
  components: {
    Datepicker,
  },
  data () {
    return {
      formValues: {}
    }
  },
  mounted() {
    this.clearFormValues()
  },
  computed: {
    ...mapGetters('risks', {
      selectedRisk: 'selectedRisk',
    }),
  },
  methods: {
    onSubmit: function() {
      this.$store.dispatch('database/insertRow', {risk: this.selectedRisk, data: this.formValues})
    },
    onReset: function() {
        this.newRisk =  {
        name: '',
        description: '',
        fields: []
      }
    },
    clearFormValues: function() {
      this.selectedRisk.fields.map(f => this.formValues[f.name] = '')
    },
    parseOptions(optString) {
      let arr = optString.split(',')
      let options = [{value: null, text: 'Please select an option'}]
      for(let i = 0; i < arr.length; i++){
        options.push({value: i, text: arr[i]})
      }
      return options
    }
  }
}
</script>

<style scoped>
.db-form {
  order: 2;
  /* max-height: 35h;
  height: 35vh; */
}
@media (min-width: 760px) {
  .db-form{
    grid-row: 1 / 3;
    grid-column: 3 / 4;
  }
}
</style>
