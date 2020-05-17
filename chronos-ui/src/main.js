import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import "./api";

import axios from "axios";
import VueAxios from "vue-axios";
import VModal from "vue-js-modal";

Vue.use(VueAxios, axios);
Vue.use(VModal);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
