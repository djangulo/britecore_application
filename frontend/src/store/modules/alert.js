/* eslint-disable */
const state = {
  dismissSecs: 5,
  dismissCountDown: 0,
  alerts: []
}

const getters = {
  alerts: (state) => state.alerts,
  dismissCountDown: (state) => state.dismissCountDown,
  dismissSecs: (state) => state.dismissSecs
}

const actions = {
}

// mutations
const mutations = {
  show(state) {
    state.dismissCountDown = state.dismissSecs
  },
  addAlert(state, msg) {
    state.alerts.push(msg)
  },
  setDismissCountDown(state, value) {
    state.dismissCountDown = value
    if(value === 0) {
      state.alerts = []
    }
  },
  clear(state) {
    state.alerts = []
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}