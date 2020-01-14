import Vue from 'vue'
import Vuex from 'vuex'

import App from './App.vue'
import router from './router'

import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

import axios from 'axios'
import i18n from './i18n'
import {
  capitalize
} from './filters/capitalize'

Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(Buefy)
Vue.use(Vuex)
Vue.filter('capitalize', capitalize);

if (Vue.config.devtools) {
  Vue.prototype.api = 'http://localhost:5000/api'
} else {
  Vue.prototype.api = '/api'
}


const store = new Vuex.Store({
  state: {
    $chronos: {
      connected: false
    },
    scripts: []
  },
  mutations: {
    connected(state, payload) {
      state.$chronos.connected = payload
    },
    scripts(state, payload) {
      state.scripts = payload
    }
  }
})


new Vue({
  router,
  i18n,
  store,
  render: h => h(App),
  mounted() {
    this.loadAllScripts();

    this.$nextTick(function () {
      window.setInterval(() => {
        this.loadAllScripts();
      }, 2000);
    })

  },
  methods: {
    loadAllScripts() {
      this.$http.get(this.api + '/scripts').then(response => {
        store.commit('scripts', response.data)
        store.commit('connected', true)
      }).catch(() => {
        store.commit('connected', true)
      })
    },
  }
}).$mount('#app')