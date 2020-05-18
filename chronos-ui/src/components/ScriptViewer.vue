<template>
  <div class="script-viewer">
    <div class="no-script" v-if="script_uid === undefined">
      <h1>No script selected</h1>
    </div>

    <div class="script" v-else>
      <h1>{{ script.name }}</h1>

      <div class="section">
        <h2>Quick actions</h2>

        <div class="quick-actions">
          <QuickAction
            icon="play_arrow"
            text="Execute"
            action="execute"
            script_uid="test"
          />

          <QuickAction
            icon="get_app"
            text="Install Pip requirements"
            action="execute"
            script_uid="test"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QuickAction from "@/components/QuickAction";

export default {
  name: "ScriptViewer",
  components: {
    QuickAction
  },
  props: {
    script_uid: {
      type: String,
      required: false
    }
  },
  computed: {
    scripts() {
      return this.$store.state.scripts;
    },
    script() {
      return this.scripts.find(value => {
        return value.uid === this.script_uid ? true : false;
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.no-script,
.script-viewer {
  width: 100%;
  height: 100%;
}

.no-script {
  display: flex;
  align-items: center;
  justify-content: center;

  h1 {
    opacity: 0.5;
    font-size: 1.6rem;
    font-weight: 400;
  }
}

.script {
  padding: 60px 0 20px 45px;
  box-sizing: border-box;
}

h1 {
  font-size: 3.2rem;
  font-weight: 400;
}

.section {
  margin-bottom: 30px;

  h2 {
    font-size: 1.3rem;
    font-weight: 600;
  }
}

.quick-actions {
  display: flex;

  .quick-action {
    margin-right: 15px;
  }
}
</style>
