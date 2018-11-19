/* eslint-disable */
const state = {
  status: '',
  log: [],
}

const getters = {
  status: (state) => state.status,
  log: (state) => state.log
}

const actions = {
}

// mutations
const mutations = {
  write(state, status) {
    state.status = status
    state.log.push(status)
  },
  clear(state, n) {
    if(n == 0) {
      state.log = []
    } else {
      state.log = state.log.slice([state.log.length - (1+n)])
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}