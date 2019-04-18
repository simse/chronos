<template>
  <div id="app" class="container">
    <link rel="stylesheet" href="https://cdn.materialdesignicons.com/2.5.94/css/materialdesignicons.min.css">

    <h1 class="is-size-1 title">Chronos</h1>

    <!--div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div-->
    <router-view/>


  </div>
</template>

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

.title {
  padding-bottom: 50px;
  text-align: center;
}

</style>
