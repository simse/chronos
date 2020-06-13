import store from "./store";
import events from "./events";
import axios from "axios";
import slugify from "slugify";
import ReconnectingWebSocket from "reconnecting-websocket";

const api = {
  events: null,
  getBaseUrl() {
    if (
      process.env.NODE_ENV !== "production" &&
      process.env.NODE_ENV !== "test" &&
      typeof console !== "undefined"
    ) {
      return "http://localhost:5000/";
    } else {
      return window.location.origin + "/";
    }
  },
  getApiUrl() {
    return this.getBaseUrl() + "api/";
  },
  getWsUrl() {
    return this.getBaseUrl().replace("http", "ws") + "ws/";
  },
  guessScriptUid(name) {
    return slugify(name, {
      lower: true,
      strict: true
    });
  },
  loadScripts() {
    axios.get(this.getApiUrl() + "scripts").then(response => {
      if (response.status === 200) {
        store.commit("setScripts", response.data);
      }
    });
  },
  createScript(name, callback = () => {}) {
    let scriptUid = this.guessScriptUid(name);

    store.commit("addScriptLoading", {
      name: name,
      uid: scriptUid
    });

    let createScriptCallback = event => {
      let payload = event;
      if (payload.uid === scriptUid) {
        store.commit("finishLoadingScript", {
          uid: event.uid,
          script: payload
        });
        events.$off("_script_created", createScriptCallback);
        callback();
      }
    };
    events.$on("_script_created", createScriptCallback);

    axios.post(this.getApiUrl() + "script/null", {
      name: name
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

    events.$on("_action_complete", callback);
    events.$on("_task_output", taskOutputCallback);
    events.$on("_task_finished", taskCompleteCallback);

    axios.get(this.getApiUrl() + "script/" + uid + "/action/" + action);
  },
  saveScript(script, callback = () => {}) {
    axios.put(this.getApiUrl() + "script/" + script.uid, script).then(() => {
      // console.log("okay");
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

    // Start WebSocket connection
    const ws = new ReconnectingWebSocket(this.getWsUrl());
    ws.onmessage = event => {
      let data = JSON.parse(event.data);

      events.$emit("_" + data.event, data.payload);
    };

    ws.onopen = () => {
      store.commit("setConnectionStatus", true);
    };

    ws.onclose = () => {
      this.loadScripts();
      store.commit("setConnectionStatus", false);
    };
  }
};

export default api;
