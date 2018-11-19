import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import App from './App.vue'
import store from './store'

Vue.config.productionTip = false
Vue.config.productionGzip = true
Vue.use(BootstrapVue)

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
