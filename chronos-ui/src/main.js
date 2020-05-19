import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import "./api";

import axios from "axios";
import VueAxios from "vue-axios";
import VModal from "vue-js-modal";
import api from "./api";
import events from "./events";

Vue.use(VueAxios, axios);
Vue.use(VModal, { dialog: true });

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
  mounted() {
    api.listenToChronos();

    api.events.onmessage = event => {
      let eventData = JSON.parse(event.data);

      // console.log(eventData);

      events.$emit("_" + eventData.event, eventData.payload);
    };
  }
}).$mount("#app");
