
import Vue from 'vue'
import Vuex from 'vuex'
import risks from './modules/risks'
import log from './modules/log'
import newRisk from './modules/newRisk'
import alert from './modules/alert'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    alert,
    log,
    newRisk,
    risks,
  },
  strict: debug,
})