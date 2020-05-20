import store from "./store";
import events from "./events";
import axios from "axios";

const api = {
  events: null,
  getApiUrl() {
    return "http://localhost:5000/api/";
  },
  loadScripts() {
    axios.get(this.getApiUrl() + "scripts").then(response => {
      if (response.status === 200) {
        store.commit("setScripts", response.data);
      }
    });
  },
  createScript(name, callback = () => {}) {
    axios
      .post(this.getApiUrl() + "script/null", {
        name: name
      })
      .then(response => {
        if (response.status === 200) {
          store.commit("addScriptLoading", {
            name: name,
            uid: response.data.uid
          });

          events.$on("_script_created", event => {
            let payload = event;

            if (payload.uid === response.data.uid) {
              store.commit("finishLoadingScript", {
                uid: response.data.uid,
                script: payload
              });

              callback();
            }
          });
        }
      });
  },
  scriptAction(uid, action, callback = () => {}) {
    store.commit("resetActionOutput", {
      scriptUid: uid,
      action: action
    });

    store.commit("setActionLoadingState", {
      scriptUid: uid,
      action: action,
      loading: true
    });

    let taskOutputCallback = event => {
      if (event.script_uid === uid && event.task === action) {
        store.commit("appendActionOutput", {
          scriptUid: uid,
          action: action,
          output: event.output + "\n"
        });

        store.commit("setActionTaskId", {
          scriptUid: uid,
          action: action,
          taskId: event.task_id
        });
      }
    };

    let taskCompleteCallback = event => {
      let script = store.getters.getScriptByUid(uid);

      if (typeof script === "undefined") return;

      if (event.task_id === script.actions[action].currentTaskId) {
        store.commit("setActionDoneState", {
          scriptUid: uid,
          action: action,
          done: true
        });

        events.$off("_task_output", taskOutputCallback);
        events.$off("_task_finished", taskCompleteCallback);
      }
    };

    axios
      .get(this.getApiUrl() + "script/" + uid + "/action/" + action)
      .then(response => {
        if (response.status === 200) {
          events.$on("_action_complete", callback);
          events.$on("_task_output", taskOutputCallback);
          events.$on("_task_finished", taskCompleteCallback);
        }
      });
  },
  saveScript(script, callback = () => {}) {
    axios.put(this.getApiUrl() + "script/" + script.uid, script).then(() => {
      console.log("okay");
      store.commit("updateScript", {
        uid: script.uid,
        synced: true,
        internal: true
      });
      callback();
    });
  },
  saveAllScripts() {
    store.state.scripts.forEach(script => {
      if (!script.synced) {
        api.saveScript(script);
      }
    });

    store.commit("resetSavePrompt");
  },
  listenToChronos() {
    this.events = new EventSource(this.getApiUrl() + "events/any");

    events.$on("_script_updated", event => {
      store.commit("updateScript", event);
    });

    events.$on("_script_deleted", event => {
      store.commit("deleteScript", event.uid);
    });

    events.$on("_action_started", event => {
      store.commit("setActionLoadingState", {
        scriptUid: event.uid,
        action: event.action,
        loading: true
      });
    });

    events.$on("_action_complete", event => {
      store.commit("setActionLoadingState", {
        scriptUid: event.uid,
        action: event.action,
        loading: false
      });
    });
  }
};

export default api;
