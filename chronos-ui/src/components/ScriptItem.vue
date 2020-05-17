<template>
  <div
    :class="{
      script: true,
      dark: this.index % 2 !== 0,
      light: this.index % 2 === 0
    }"
  >
    <div class="text">
      <h2>{{ script.name }}</h2>

      <span class="last-execution">
        <span v-if="!this.script.loading">Last run: 2 hours ago</span>

        <span v-else>Creating...</span>
      </span>
    </div>

    <div class="status">
      <!--div class="icon ok">
        <i class="material-icons">check</i>
      </div-->

      <!--div class="icon warning">
        <i class="material-icons">warning</i>
      </div-->

      <!--div class="icon error">
        <i class="material-icons">close</i>
      </div-->

      <div class="spinner" v-if="this.script.loading">
        <Spinner line-bg-color="transparent" line-fg-color="var(--blue)" />
      </div>

      <div class="icon ok" v-else>
        <i class="material-icons">check</i>
      </div>
    </div>
  </div>
</template>

<script>
import Spinner from "vue-simple-spinner";

export default {
  name: "ScriptItem",
  components: {
    Spinner
  },
  props: {
    script: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  }
};
</script>

<style lang="scss" scoped>
.script {
  display: flex;
  padding: 28px;
  transition: cubic-bezier(0.075, 0.82, 0.165, 1) 0.2s background;

  &:hover {
    background: #090909 !important;
    cursor: pointer;
  }

  &.dark {
    background: #0e0e0e;
  }

  &.light {
    background: #111;
  }
}

.status {
  margin-left: auto;
}

h2 {
  font-size: 1.4rem;
  font-weight: 400;
  margin: 0 0 10px 0;
}

span.last-execution {
  font-size: 0.95rem;
  opacity: 60%;
}

.icon {
  margin-top: 2px;
  border-radius: 100px;

  i {
    font-size: 2.2rem;
  }

  &.ok {
    background: var(--green);
    padding: 10px 9px 5px 9px;
  }

  &.warning {
    background: var(--yellow);
    padding: 6px 9px 8px 9px;
  }

  &.error {
    background: var(--red);
    padding: 10px 9px 5px 9px;
  }
}

.spinner {
  margin-top: 9px;
}
</style>
