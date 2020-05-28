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
import VuePrismEditor from "vue-prism-editor";
import "vue-prism-editor/dist/VuePrismEditor.css";
import "prismjs";
import "prismjs/components/prism-python";
import { Snackbar } from "buefy";
import VueCollapse from "vue2-collapse";

Vue.use(VueAxios, axios);
Vue.use(VModal);
Vue.component("prism-editor", VuePrismEditor);
Vue.use(Snackbar);
Vue.use(VueCollapse);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
  mounted() {
    api.listenToChronos();

    api.events.onmessage = event => {
      let eventData = JSON.parse(event.data);
      events.$emit("_" + eventData.event, eventData.payload);
    };
  }
}).$mount("#app");
