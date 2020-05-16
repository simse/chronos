<template>
  <div id="app">
    <div id="nav">
      <Navigation />
    </div>
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation.vue";

export default {
  name: "App",
  components: {
    Navigation
  }
};
</script>

<style lang="scss">
@import "styles/fonts.scss";

:root {
  --grey: #1f1f1f;
  --blue: #007aff;
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

h1 {
  padding-top: 70px;
  padding-left: 40px;
  padding-bottom: 40px;
  font-weight: 400;
  font-size: 3rem;
  margin: 0;
}
</style>
