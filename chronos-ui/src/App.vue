<template>
  <div id="app" class="container">
    <link rel="stylesheet" href="https://cdn.materialdesignicons.com/2.5.94/css/materialdesignicons.min.css">

    <h1 class="is-size-1 title">Chronos</h1>
    <p class="is-size-5 subtitle">{{ $t('version') | capitalize }}: {{ version }}</p>

    <router-view/>

    <div class="bottom-bar">
      <div class="status">
        <span>
          <span :class="{'icon':true,'red':!connectedBool}"></span>
          {{ $t(connected) }}
        </span>
      </div>

      <div class="tasks">

      </div>
    </div>
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
    },
    computed: {
      connectedBool() {
        return this.$store.state.$chronos.connected
      },
      connected() {
        if(this.connectedBool) {
          return 'connected'
        } else {
          return 'disconnected'
        }
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
  padding: 70px 15px 0 15px;
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

.bottom-bar {
  display: flex;
  justify-content: space-between;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100vw;
  padding: 12px 20px;
  background: #000;
  color: #fff;

  .icon {
    width: 7px;
    height: 7px;
    background: #4cd137;
    border-radius: 100%;
    margin-bottom: 2px;
    margin-right: 5px;

    &.red {
      background: #e84118;
    }
  }
}
</style>
