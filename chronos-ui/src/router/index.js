import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/scripts",
    name: "Scripts",
    component: () => import("../views/Scripts.vue"),
    props: true
  },
  {
    path: "/scripts/:script_uid",
    name: "Script",
    component: () => import("../views/Scripts.vue"),
    props: true
  },
  {
    path: "/logs",
    name: "Logs",
    component: () => import("../views/Logs.vue")
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("../views/Settings.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
