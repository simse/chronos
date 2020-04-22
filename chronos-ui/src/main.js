import Vue from 'vue'
import Vuex from 'vuex'

import App from './App.vue'
import router from './router'
import { EventBus } from './bus.js'

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

    EventBus.$on('reloadScripts', () => {
      this.loadAllScripts();
    })

    EventBus.$on('addLoadingScript', (payload) => {
      this.addLoadingScript(payload.name, payload.uid)
    })

    
  },
  methods: {
    loadAllScripts() {
      this.$http.get(this.api + '/scripts').then(response => {
        store.commit('scripts', response.data)
        store.commit('connected', true)

        
      }).catch(() => {
        store.commit('connected', false)
      })

      
    },
    addLoadingScript(name, uid) {
      let scripts = this.$store.state.scripts;
      scripts.push({
        name: name,
        uid: uid,
        loading: true,
        logs: []
      })

      store.commit('scripts', scripts)
    },
  }
}).$mount('#app')