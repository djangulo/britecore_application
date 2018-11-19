/* eslint-disable */
import axios from 'axios'
import { apiRoot } from './apiData'
// initial state
// shape: [{ id, quantity }]
const state = {
  tables: [],
  tabIndex: -1
}

const getters = {
  tables: (state) => {
    return state.tables
  },
  tabIndex: (state) => {
    return state.tabIndex
  },
  risks: (state, getters, rootState) => {
    return rootState.risks.risks
  },
  selectedRisk: (state, getters, rootState) => {
    return rootState.risks.selectedRisk
  }
}

const actions = {
  insertRow({commit}, {risk, data}) {
    let msg = `Inserting row into table "${risk.name}"`
    commit('log/write', msg, {root: true})
    commit('insertRow', {risk: risk, data: data})
    msg = `Successfully inserted row into table "${risk.name}"`
    commit('log/write', msg, {root: true})
  },
  refreshTables({state}) {
    state.tables = state.tables
  },
  createTable({commit, state}, risk) {
    let msg = `Creating "database" table "${risk.name}"`
    commit('log/write', msg, {root: true})
    if(state.tables.filter(t => t.slug === risk.slug).length > 0) {
      msg = `It seems table "${risk.name}" already exists, selecting it instead`
      commit('log/write', msg, {root: true})
      commit('setTabIndex', state.tables.find(t => t.slug === risk.slug).tabIndex)
    } else {
      let msg = `Creating "database" table "${risk.name}"`
      commit('log/write', msg, {root: true})
      commit('createTable', {risk})
      msg = `Successfully created table "${risk.name}"`
      commit('log/write', msg, {root: true})
    }
  },
  saveTables({commit}) {
    let msg = 'Saving "database" tables to localStorage '
    commit('log/write', msg, {root: true})
    commit('saveToLocal')
    msg = 'Successfully saved tables to localStorage'
    commit('log/write', msg, {root: true})
  },
  deleteTables({commit}) {
    let msg = 'Deleting "database" tables from localStorage '
    commit('log/write', msg, {root: true})
    commit('deleteFromLocal')
    msg = 'Successfully deleted tables from localStorage'
    commit('log/write', msg, {root: true})
  },
  restoreTables({commit}) {
    let msg = 'Pulling "database" tables from localStorage '
    commit('log/write', msg, {root: true})
    commit('restoreFromLocal')
    msg = 'Successfully pulled tables from localStorage'
    commit('log/write', msg, {root: true})
  }
}

// mutations
const mutations = {
  createTable(state, { risk }) {
    state.tables.push({
      name: risk.name,
      slug: risk.slug,
      tabIndex: state.tabIndex + 1,
      headers: risk.fields.map(f => f.name),
      values: []
    })
  },
  setTabIndex(state, index) {
    state.tabIndex = index
  },
  insertRow(state, { risk, data}) {
    state.tables.find(table => table.slug === risk.slug).values.push(data)
  },
  deleteRow(state, { risk, rowIndex}) {
    state.tables.splice(rowIndex, 1)
  },
  saveToLocal(state) {
    localStorage.setItem('tables', JSON.stringify(state.tables))
  },
  deleteFromLocal(state) {
    localStorage.tables = JSON.stringify([])
  },
  restoreFromLocal(state) {
    state.tables = JSON.parse(localStorage.getItem('tables'))
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}