/* eslint-disable */
import axios from 'axios'
const apiRoot = 'http://localhost:8000/api/v1.0'

const state = {
  form: {
    name: '',
    description: '',
    fields: []
  }
}

const getters = {
  formValues: (state) => {
    state.form ? state.form : {name: '', description: '', fields: []}
  },
}

const actions = {
  async createRisk ({ dispatch, commit, state }, risk) {
    const savedValues = {...risk}
    let msg = `Creating risk "${risk.name}".`
    commit('log/write', msg, {root: true})
    // commit('setFormValues', {risk: {
    //   name: '',
    //   description: '',
    //   fields: []
    // }})
    return new Promise((resolve, reject) => {
      axios
      .post(`${apiRoot}/risks/`, {
        'name': risk.name,
        'description': risk.description,
        'fields': risk.fields
      })
      .then(async response => {
        msg = `Risk type "${response.data.name}" created successfully!`
        commit('log/write', msg, {root: true})
        await dispatch('risks/getRisks', null, { root: true})
        resolve(response);
      }, async err => {
        msg = `Creation of risk "${risk.name}" failed: ${err.data}`
        commit('log/write', msg, {root: true})
        // commit('setFormValues', savedValues)
        reject(err)
      })
    })
  },
  addFormField({commit}) {
    let msg = `Adding new blank field.`
    commit('log/write', msg, {root: true})
    commit('addField')
  },
  removeNewRiskFormField({commit}, index) {
    let msg = `Removing field no. ${index}.`
    commit('log/write', msg, {root: true})
    commit('removeField', index)
    msg = `Field no. ${index} succesfully removed.`
    commit('log/write', msg, {root: true})
  },
}

// mutations
const mutations = {
  setFormValues(state, { risk }) {
    state.form.name = risk ? risk.name ? risk.name : '' : null
    state.form.description = risk ? risk.name ? risk.name : '' : null
    state.form.fields = risk.fields ? risk.fields : []
  },
  setFormName(state, { name }) {
    state.form.name = name
  },
  setFormDescription(state, { description }) {
    state.form.description = description
  },
  setFormFields(state, { fields }) {
    state.form.fields = fields
  },
  setFieldName(state, value, index) {
    state.form.fields[index].name = value
  },
  setFieldType(state, value, index) {
    state.form.fields[index].data_type = value
  },
  setFieldHelp(state, value, index) {
    console.dir(value)
    state.form.fields[index].help_text = 'this is a modidid'
  },
  setOrder(state, value, index) {
    state.form.fields[index].display_order = value
  },
  moveField(state, { index }) {

  },
  addField(state) {
    state.form.fields.push({
      name: '',
      data_type: 0,
      help_text: '',
      display_order: 0
    })
  },
  removeField(state, { index }) {
    state.form.fields.splice(index, 1)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}