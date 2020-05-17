import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    scripts: [],
    settings: [],
    isConnected: false
  },
  mutations: {
    setScripts(state, payload) {
      state.scripts = payload;
    },
    addScriptLoading(state, payload) {
      state.scripts.push({
        uid: payload.uid,
        name: payload.name,
        loading: true,
        created: new Date()
      });
    },
    finishLoadingScript(state, payload) {
      state.scripts.some(value => {
        if (value.uid === payload.uid) {
          value.loading = false;

          Object.keys(payload.script).forEach(key => {
            value[key] = payload.script[key];
          });

          return true;
        }
      });
    }
  },
  actions: {},
  modules: {}
});
