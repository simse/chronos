import store from "./store";
import axios from "axios";

const api = {
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
  createScript(name) {
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

          const eventStream = new EventSource(
            this.getApiUrl() + "events/script_created"
          );

          eventStream.onmessage = function(event) {
            console.log(event);
            let payload = JSON.parse(event.data).payload;

            console.log(payload.uid);
            console.log(response.data.uid);

            if (payload.uid === response.data.uid) {
              store.commit("finishLoadingScript", {
                uid: response.data.uid,
                script: payload
              });

              eventStream.close();
            }
          };
        }
      });
  }
};

export default api;
