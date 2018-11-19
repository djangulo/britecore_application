<template>
  <form @click.prevent="onSubmit" class="db-form text-left">
    <b-card v-bind="{ title: selectedRisk.name, 'sub-title': selectedRisk.description }">
      <b-row v-for="(field, i) in selectedRisk.fields" :key="i" class="my-1">
        <b-col sm="4"><label for="input-small"><small>{{ field.name }}</small></label></b-col>
        <b-col sm="8">
          <b-form-input
            id="input-small" 
            size="sm" 
            type="text" 
            v-bind="{ placeholder: `e.g. ${field.help_text}`}" 
            v-model="formValues[field.name]"></b-form-input>
        </b-col>
      </b-row>
      <b-btn variant="outline-primary" type="submit">Create</b-btn>
      <b-btn variant="outline-warning" type="submit" @click="onReset">Clear</b-btn>
    </b-card>
  </form>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'DbForm',
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
      console.log('you "submitted" your form')
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
    }
  }
}
</script>

<style scoped>
.db-form {
  order: 2;
  max-height: 35h;
  height: 35vh;
  overflow-y: scroll;
}
@media (min-width: 760px) {
  .db-form{
    grid-row: 1 / 2;
    grid-column: 3 / 4;
  }
}
</style>
