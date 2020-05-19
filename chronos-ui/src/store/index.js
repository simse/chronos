import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    scripts: [],
    actions: {},
    settings: [],
    isConnected: false
  },
  mutations: {
    setScripts(state, payload) {
      let scripts = payload;

      // Add data so Vue knows to listen for changes
      scripts.forEach(script => {
        script.actions = {
          execute: {
            loading: false,
            done: false,
            output: "",
            currentTaskId: 0
          },
          install_requirements: {
            loading: false,
            done: false,
            output: "",
            currentTaskId: 0
          },
          disable: {
            loading: false,
            done: false,
            output: "",
            currentTaskId: 0
          },
          enable: {
            loading: false,
            done: false,
            output: "",
            currentTaskId: 0
          },
          delete: {
            loading: false,
            done: false,
            output: "",
            currentTaskId: 0
          }
        };
      });

      state.scripts = scripts;
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
          value.actions = {
            execute: {
              loading: false,
              done: false,
              output: "",
              currentTaskId: 0
            },
            install_requirements: {
              loading: false,
              done: false,
              output: "",
              currentTaskId: 0
            },
            disable: {
              loading: false,
              done: false,
              output: "",
              currentTaskId: 0
            },
            enable: {
              loading: false,
              done: false,
              output: "",
              currentTaskId: 0
            },
            delete: {
              loading: false,
              done: false,
              output: "",
              currentTaskId: 0
            }
          };

          Object.keys(payload.script).forEach(key => {
            value[key] = payload.script[key];
          });

          return true;
        }
      });
    },
    updateScript(state, payload) {
      let script =
        state.scripts[
          state.scripts.findIndex(value => {
            return value.uid === payload.uid ? true : false;
          })
        ];

      Object.keys(payload).forEach(key => {
        script[key] = payload[key];
      });
    },
    setActionLoadingState(state, payload) {
      let script = state.scripts.findIndex(value => {
        return value.uid === payload.scriptUid ? true : false;
      });

      //console.log(state.scripts[script]);

      state.scripts[script].actions[payload.action].loading = payload.loading;
    },
    setActionDoneState(state, payload) {
      let script = state.scripts.findIndex(value => {
        return value.uid === payload.scriptUid ? true : false;
      });

      state.scripts[script].actions[payload.action].done = payload.done;
    },
    setActionTaskId(state, payload) {
      let script = state.scripts.findIndex(value => {
        return value.uid === payload.scriptUid ? true : false;
      });

      state.scripts[script].actions[payload.action].currentTaskId =
        payload.taskId;
    },
    appendActionOutput(state, payload) {
      let script = state.scripts.findIndex(value => {
        return value.uid === payload.scriptUid ? true : false;
      });

      state.scripts[script].actions[payload.action].output += payload.output;
    },
    resetActionOutput(state, payload) {
      let script = state.scripts.findIndex(value => {
        return value.uid === payload.scriptUid ? true : false;
      });

      state.scripts[script].actions[payload.action].output = "";
      state.scripts[script].actions[payload.action].done = false;
    }
  },
  getters: {
    getScriptByUid: state => uid => {
      if (state.scripts.length == 0) {
        return undefined;
      }

      return state.scripts.find(value => {
        return value.uid === uid ? true : false;
      });
    }
  }
});
