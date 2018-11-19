/* eslint-disable */
import axios from 'axios'
import { apiRoot } from './apiData'
// initial state
// shape: [{ id, quantity }]
const state = {
  risks: [],
  selectedRisk: null,
}

const getters = {
  availableRisks: (state) => {
    return state.risks
  },
  selectedRisk: (state) => state.selectedRisk,
}

const actions = {
  async getRisks({commit}) {
    return new Promise((resolve, reject) => {
      let msg = 'Fetching risks...'
      commit('log/write', msg, {root: true})
      axios
      .get(`${apiRoot}/risks/`)
      .then(response => {
        let msg = `Successfully fetched ${response.data.length} risk types.`
        commit('log/write', msg, {root: true})
        commit('setRisks', { risks: response.data})
          resolve(response);
        }, err => {
          let msg = `Failed to fetch risks: ${err.data}`
          commit('log/write', msg, {root: true})
          reject(err);
      })
    })
  },
  selectRisk ({commit}, risk) {
    let msg = `Selected risk "${risk.name}".`
    commit('log/write', msg, {root: true})
    commit('setSelectedRisk', {risk: risk})
  },
  deSelectRisk ({commit, state}) {
    let msg = `Deselected risk "${state.selectedRisk.name}".`
    commit('log/write', msg, {root: true})
    commit('setSelectedRisk', {risk: null})
  },
  // async modifyRisk ({dispatch, commit, state}, risk) {
  //   const savedSelectedRisk = state.selectedRisk
  //   let msg = `Modifyng risk "${risk.name}".`
  //   commit('log/write', msg, {root: true})
  //   return new Promise((resolve, reject) => {
  //     axios
  //     .patch(`${apiRoot}/risks/${risk.id}`, {
  //       'name': risk.name,
  //       'description': risk.description,
  //       'fields': risk.fields
  //     })
  //     .then(async response => {
  //       msg = `Risk "${risk.name}" modified successfully!`
  //       commit('log/write', msg, {root: true})
  //       commit('setRisks', await dispatch('getRisks'))
  //       commit('setSelectedRisk', { risk: null, riskId: response.data.id })
  //       resolve(response);
  //     }, async err => {
  //       msg = `Modification of ${risk.name} failed: ${err.data}`
  //       commit('log/write', msg, {root: true})
  //       commit('setSelectedRisk', savedSelectedRisk)
  //       reject(err)
  //     })
  //   })
  // },
  async deleteRisk ({dispatch, commit, state}, risk) {
    const savedRisks = [...state.risks]
    let msg = `Deleting risk "${risk.name}".`
    commit('log/write', msg, {root: true})
    return new Promise((resolve, reject) => {
      axios
      .delete(`${apiRoot}/risks/${risk.id}`)
      .then(async () => {
        msg = `Risk "${risk.name}" deleted successfully!`
        commit('log/write', msg, {root: true})
        await dispatch('getRisks').then(
          commit('setSelectedRisk', {risk: null})
        )
        resolve();
      }, async err => {
        msg = `Deletion of "${risk.name}" failed: ${err.data}`
        commit('log/write', msg, {root: true})
        commit('setRisks', savedRisks)
        reject(err)
      })
    })
  },
  async restoreOriginalRisks({dispatch, commit, state}, risk) {
    const savedRisks = [...state.risks]
    let msg = `Restoring original sample risks.`
    commit('log/write', msg, {root: true})
    return new Promise((resolve, reject) => {
      axios
      .get(`${apiRoot}/risks/create_initial_risks`)
      .then(async response => {
        msg = `Original sample risks restored successfully`
        commit('log/write', msg, {root: true})
        await dispatch('getRisks')
        resolve(response);
      }, async err => {
        msg = `Original sample risks restoration failed: ${err.data}`
        commit('log/write', msg, {root: true})
        commit('setRisks', savedRisks)
        reject(err)
      })
    })
  },
}

// mutations
const mutations = {
  setRisks (state, { risks }) {
    state.risks = risks
  },
  setSelectedRisk(state, { risk, riskId=null }) {
    if(riskId !== null) {
      state.selectedRisk = state.risks.filter(r => r.id === riskId)
    } else {
      state.selectedRisk = risk
    }
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}