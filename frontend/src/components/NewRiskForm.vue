<template>
  <div class="risk-form">
    <b-form @submit.prevent="onSubmit" @reset="onReset" id="risk-form">
      <b-container fluid>
        <h5 class="text-left">Create a new risk type</h5>
        <b-row class="my-1">
          <b-col sm="3"><label for="input-small"><small>Name</small></label></b-col>
          <b-col sm="9">
            <b-form-input
              id="input-small" 
              size="sm" 
              type="text" 
              v-bind="{ placeholder: `e.g. ${randomExample.name}`}" 
              v-model="newRisk.name"></b-form-input>
          </b-col>
        </b-row>
        <b-row class="my-1">
          <b-col sm="3"><label for="input-small"><small>Description</small></label></b-col>
          <b-col sm="9">
            <b-form-input
              id="input-small" 
              size="sm" 
              type="text"
               v-bind="{ placeholder: `e.g. ${randomExample.description}`}"
               v-model="newRisk.description"></b-form-input>
          </b-col>
        </b-row>
      </b-container>
      <b-button @click="addField()">Add field</b-button>
        <b-card border-variant="default"
          header-bg-variant="default"
          header-text-variant="default"
          align="center"
          v-for="(field, i) in newRisk.fields" :key="i">
          
          <b-row class="my-1" slot="header">
            <b-col sm="2"><label for="input-small"><small>Name</small></label></b-col>
            <b-col sm="8">
              <b-form-input
                id="input-small" 
                size="sm" 
                type="text"
                v-model="newRisk.fields[i].name"></b-form-input>
            </b-col>
            <b-col sm="1">
              <b-button-close @click="removeField(i)"></b-button-close>
            </b-col>
          </b-row>
        <b-row class="my-1">
            <b-col sm="2"><label for="input-small"><small>Type</small></label></b-col>
            <b-col sm="4">
              <b-form-select :options="typeOptions" class="mb-3" size="sm" 
                v-model="newRisk.fields[i].data_type"/>
            </b-col>
            <b-col sm="2"><label for="input-small"><small>Order</small></label></b-col>
            <b-col sm="4">
              <b-form-input
                id="input-small" 
                size="sm" 
                type="number"
                v-model="newRisk.fields[i].display_order"></b-form-input>
            </b-col>
          </b-row>
           <b-row class="my-1" >
            <b-col sm="2"><label for="input-small"><small>Help text</small></label></b-col>
            <b-col sm="10">
              <b-form-textarea
                id="input-small" 
                size="sm" 
                type="text"
                :rows="3"
                 :max-rows="6"
                v-model="newRisk.fields[i].help_text"></b-form-textarea>
            </b-col>
          </b-row>
          <b-row v-if="newRisk.fields[i].data_type == 3" class="my-1" >
            <b-col sm="2"><label for="input-small"><small>Options</small></label></b-col>
            <b-col sm="10">
              <b-form-input
                id="input-small" 
                size="sm" 
                type="text"
                description="Comma separated list of options to display" 
                v-model="newRisk.fields[i].enum_options"></b-form-input>
              <b-form-text sm="10">Comma separated list of options to display.</b-form-text>
            </b-col>
          </b-row>
        </b-card>
      <b-btn variant="outline-primary" type="submit">Create</b-btn>
      <b-btn variant="outline-warning" type="button" @click="onReset">Clear</b-btn>
    </b-form>

    
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'NewRiskForm',
  data () {
    return {
      randomExample: {name: '', description: ''},
      examples: [
        {
          name: 'Automobile Policies',
          description: 'Insurance in case of a collision'
        },
        {
          name: 'Cyber Liability Coverage',
          description: 'Protection against hacking or any other cyber crime'
        },
        {
          name: 'Prize Insurance',
          description: "If someone gets a $1 million hole-in-one prize at a golf tournament, the golf course doesn't pay it, they have an insurance policy to cover them"
        },
        {
          name: 'Work hazard insurance',
          description: 'Coverage in case of an employee accident'
        }
      ],
      typeOptions: [
        { value: null, text: 'Please select an option.'},
        { value: "0", text: 'Text' },
        { value: "1", text: 'Number' },
        { value: "2", text: 'Date' },
        { value: "3", text: 'Enum'}
      ],
      newRisk: {
        name: '',
        description: '',
        fields: [],
      },
      errors: [],
    }
  },
  mounted() {
    this.randomExample = this.examples[Math.floor(Math.random() * this.examples.length)];
  },
  computed: {
    ...mapGetters('newRisk', {
      formValues: 'formValues'
    }),
    ...mapGetters('risks', {
      risks: 'availableRisks'
    }),
    ...mapGetters('alert', {
      alerts: 'alerts'
    }),
    formName: {
      get () {
        return this.$store.state.newRisk.form.name
      },
      set (value) {
        this.$store.commit('newRisk/setFormName', { value })
      }
    },
  },
  update() {
    this.onReset()
  },
  methods: {
    onSubmit: function() {
      this.validateForm()
      if(this.alerts.length > 0) {
        this.showAlert()
      } else {
        this.$store.dispatch('newRisk/createRisk', this.newRisk)
      }
    },
    validateForm: function() {
      if(this.newRisk.name === '') {
       this.$store.commit('alert/addAlert', '"Name" field cannot be blank')
      }
      if(this.newRisk.fields.filter(f => f.name === '').length > 0) {
       this.$store.commit('alert/addAlert', '"Name" field on Field Types is required.')
      }
      if(this.risks.filter(f => f.name === this.newRisk.name).length > 0) {
        this.$store.commit('alert/addAlert', `Risk "${this.newRisk.name}" already exists`)
      }
    },
    onReset: function() {
        this.newRisk =  {
        name: '',
        description: '',
        fields: []
      }
    },
    addField: function() {
      this.newRisk.fields.push({
        name: '',
        data_type: 0,
        help_text: '',
        display_order: 0
      })
    },
    removeField: function(index) {
      this.newRisk.fields = this.newRisk.fields.slice(0, index).concat(this.newRisk.fields.slice(index+1));
    },
    countDownChanged(dismissCountDown) {
      this.$store.commit('alert/setDismissCountDown', dismissCountDown)
    },
    showAlert() {
      this.$store.commit('alert/show')
    },
    clearAlerts() {
      this.$store.commit('alert/clear')
    }
  }
}
</script>

<style scoped>
.risk-form {
  order: 3;
}
@media (min-width: 760px) {
  .risk-form {
    grid-row: 2 / 3;
    grid-column: 2 / 3;
  }
}
</style>
