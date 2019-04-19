import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import axios from 'axios'

Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(Buefy)

Vue.prototype.api = 'http://localhost:5000/api'

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
