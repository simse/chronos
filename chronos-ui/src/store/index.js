import Vue from "vue";
import Vuex from "vuex";
import events from "@/events";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    scripts: [],
    settings: [],
    isConnected: false,
    hasPromptedSave: false
  },
  mutations: {
    setConnectionStatus(state, payload) {
      state.isConnected = payload;
    },
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

        script.synced = true;
      });

      state.scripts = scripts;
    },
    addScriptLoading(state, payload) {
      if (!this.getters.scriptUidExists(payload.uid)) {
        state.scripts.push({
          uid: payload.uid,
          name: payload.name,
          loading: true,
          created: new Date(),
          logs: [],
          actions: {
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
          },
          synced: true
        });
      }
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
    },
    updateScript(state, payload) {
      // TODO: Clean this garbage up
      let script =
        state.scripts[
          state.scripts.findIndex(value => {
            return value.uid === payload.uid ? true : false;
          })
        ];

      if ("synced" in payload) {
        if (!payload.synced && payload.internal) {
          Object.keys(payload).forEach(key => {
            script[key] = payload[key];
          });
        }

        if (payload.synced && payload.internal) {
          Object.keys(payload).forEach(key => {
            script[key] = payload[key];
          });
        }
      } else {
        if (script.synced) {
          Object.keys(payload).forEach(key => {
            script[key] = payload[key];
          });
        } else if ("logs" in payload) {
          script.logs = payload.logs;
        }
      }
    },
    deleteTrigger(state, payload) {
      let script =
        state.scripts[
          state.scripts.findIndex(value => {
            return value.uid === payload.uid ? true : false;
          })
        ];

      script.triggers.splice(payload.trigger_index, 1);
      script.synced = false;

      if (!this.hasPromptedSave) {
        events.$emit("prompt-save");
        this.hasPromptedSave = true;
      }
    },
    resetSavePrompt(state) {
      state.hasPromptedSave = false;
    },
    deleteScript(state, uid) {
      let index = state.scripts.findIndex(value => {
        return value.uid === uid ? true : false;
      });

      state.scripts.splice(index, 1);
    },
    setActionLoadingState(state, payload) {
      let script = state.scripts.findIndex(value => {
        return value.uid === payload.scriptUid ? true : false;
      });

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
    },
    scriptUidExists: state => uid => {
      let script = state.scripts.find(value => {
        return value.uid === uid ? true : false;
      });

      return !(typeof script === "undefined");
    }
  }
});
