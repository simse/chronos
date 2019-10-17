<template>
  <div id="app" class="container">
    <link rel="stylesheet" href="https://cdn.materialdesignicons.com/2.5.94/css/materialdesignicons.min.css">

    <h1 class="is-size-1 title">Chronos</h1>
    <p class="is-size-5 subtitle">Version: {{ version }}</p>

    <router-view/>
  </div>
</template>

<script>
import version from '!raw-loader!./VERSION'

export default {
    name: 'App',
    data() {
        return {
            version: version
        }

    }
}

</script>

<style lang="scss">
*,
*::before,
*::after {
    box-sizing: border-box;
}

html {
    font-size: 100%;
    font-family: 'SF Pro Display';
}

body {
  background: #f6f9fc;
  min-height: 100vh;
}

#app {

  padding-top: 70px;
}

.title,
.subtitle {
  text-align: center;
}

.title {
    padding-bottom: 10px;
}

.subtitle {
    padding-bottom: 45px;
}

.version {
    opacity: 0.7;
}
</style>
