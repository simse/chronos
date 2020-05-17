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
        loading: true
      });
    },
    finishLoadingScript(state, payload) {
      state.scripts.some(value => {
        if (value.uid === payload.uid) {
          value.loading = false;
          value.triggers = payload.script.triggers;
          value.enabled = payload.script.enabled;
          value.name = payload.script.name;
          value.logs = payload.script.logs;

          return true;
        }
      });
    }
  },
  actions: {},
  modules: {}
});
