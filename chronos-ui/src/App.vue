<template>
  <div id="app">
    <div id="nav">
      <Navigation />
    </div>
    <div class="content">
      <router-view />
    </div>

    <ConfirmModal />

    <div class="connection-status-overlay" :class="{ hidden: isConnected }">
      <Spinner line-bg-color="transparent" line-fg-color="var(--blue)" />

      <h1>Connecting to Chronos...</h1>
    </div>
  </div>
</template>

<script>
import Spinner from "vue-simple-spinner";
import Navigation from "@/components/Navigation";
import ConfirmModal from "@/components/ConfirmModal";
import api from "@/api";

export default {
  name: "App",
  components: {
    Navigation,
    ConfirmModal,
    Spinner
  },
  mounted() {
    api.loadScripts();
  },
  computed: {
    isConnected() {
      return this.$store.state.isConnected;
    }
  }
};
</script>

<style lang="scss">
@import "styles/fonts.scss";
@import "styles/buttons.scss";
@import "styles/syntax.scss";
@import "styles/snackbar.scss";

:root {
  --grey: #1f1f1f;
  --blue: #007aff;
  --blue-dark: #006ee6;
  --green: #04cd00;
  --yellow: #dcac00;
  --red: #dc0000;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  box-sizing: border-box;
}

#app {
  font-family: "Inter";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #fff;
  background: var(--grey);
  min-height: 100vh;

  display: grid;
  grid-template-columns: 90px auto;
}

h1.page-title {
  padding-top: 70px;
  padding-left: 40px;
  padding-bottom: 40px;
  font-weight: 400;
  font-size: 3rem;
  margin: 0;
  opacity: 0.9;
}

.vm--overlay {
  background: rgba(0, 0, 0, 0.9) !important;
}

.vm--modal {
  background: #101010 !important;
  box-shadow: 0 20px 60px -2px rgba(0, 0, 0, 0.3) !important;
}

h2.modal-title {
  font-weight: 400;
  text-align: center;
  margin-bottom: 45px;
}

.connection-status-overlay {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(14px);
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms background;
  transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms backdrop-filter;

  &.hidden {
    background: rgba(0, 0, 0, 0);
    backdrop-filter: blur(0px);
    pointer-events: none;

    h1 {
      opacity: 0;
    }

    .vue-simple-spinner {
      display: none;
    }
  }

  h1 {
    font-size: 2rem;
    margin: 50px 0 0 0;
    transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms opacity;
  }
}
</style>
