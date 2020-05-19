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
    callback();
  },
  listenToChronos() {
    this.events = new EventSource(this.getApiUrl() + "events/any");
  }
};

export default api;
