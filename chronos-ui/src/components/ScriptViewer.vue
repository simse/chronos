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
            :showOutput="true"
            :script_uid="script_uid"
          />

          <ActionOutput
            :uid="this.script_uid"
            action="execute"
            :modalId="this.script_uid + '_execute'"
            title="Execute script output"
          />

          <QuickAction
            icon="get_app"
            text="Install Pip requirements"
            action="install_requirements"
            :showOutput="true"
            :script_uid="script_uid"
          />

          <ActionOutput
            :uid="this.script_uid"
            action="install_requirements"
            :modalId="this.script_uid + '_install_requirements'"
            title="Install pip requirements output"
          />

          <QuickAction
            :icon="disableOrEnable.icon"
            :text="disableOrEnable.text"
            :action="disableOrEnable.action"
            :script_uid="script_uid"
          />

          <QuickAction
            icon="delete"
            text="Delete"
            action="delete"
            :confirm="true"
            :script_uid="script_uid"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QuickAction from "@/components/QuickAction";
import ActionOutput from "@/components/ActionOutput";

export default {
  name: "ScriptViewer",
  components: {
    QuickAction,
    ActionOutput
  },
  props: {
    script_uid: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      loading: false
    };
  },
  computed: {
    scripts() {
      return this.$store.state.scripts;
    },
    script() {
      if (this.$store.state.scripts.length == 0) {
        return {};
      }

      return this.scripts.find(value => {
        return value.uid === this.script_uid ? true : false;
      });
    },
    disableOrEnable() {
      if (this.script !== {}) {
        if (!this.script.enabled) {
          return {
            text: "Enable",
            icon: "check",
            action: "enable"
          };
        }
      }

      return {
        text: "Disable",
        icon: "clear",
        action: "disable"
      };
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
  flex-wrap: wrap;

  .quick-action {
    margin-right: 15px;
    margin-bottom: 15px;
  }
}
</style>
