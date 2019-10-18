import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import axios from 'axios'
import i18n from './i18n'
import { capitalize } from './filters/capitalize'

Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(Buefy)
Vue.filter('capitalize', capitalize);

if(Vue.config.devtools) {
    Vue.prototype.api = 'http://localhost:5000/api'
} else {
    Vue.prototype.api = '/api'
}


new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount('#app')
