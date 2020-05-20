<template>
  <div class="script-viewer">
    <div class="no-script" v-if="script_uid === undefined">
      <h1>No script selected</h1>
    </div>

    <div class="script" v-else>
      <h1>{{ script.name }}</h1>

      <div v-if="!script.synced">
        You have unsaved changes.
      </div>

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

      <div class="section">
        <div class="header">
          <h2>Script triggers</h2>

          <div>
            <a class="button blue">
              <i class="material-icons">add</i> Add trigger
            </a>
          </div>
        </div>

        <div class="triggers">
          <div class="empty">
            <h2>No triggers</h2>

            <p>
              Use triggers to execute your scripts on an interval or using Cron
              expressions
            </p>
          </div>
        </div>
      </div>

      <div class="section">
        <div class="header">
          <h2>Pip requirements</h2>

          <div>
            <a class="button blue">
              <i class="material-icons">add</i> Add requirement
            </a>
          </div>
        </div>

        <div class="requirements">
          <div class="empty">
            <h2>No dependencies</h2>

            <p>
              That’s okay, but if your script requires external Python packages,
              now is the time to declare it
            </p>
          </div>
        </div>

        <a class="raw">Switch to raw mode</a>
      </div>

      <div class="section">
        <h2>Python script</h2>

        <prism-editor
          :code="python_script"
          :lineNumbers="true"
          language="py"
          @change="updateCode"
        ></prism-editor>
      </div>

      <div class="section">
        <h2>Execution reports</h2>
      </div>
    </div>
  </div>
</template>

<script>
import QuickAction from "@/components/QuickAction";
import ActionOutput from "@/components/ActionOutput";
import events from "@/events";

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
  mounted() {
    events.$on("_script_deleted", event => {
      if (event.uid === this.script_uid) {
        this.$router.push("/scripts");
      }
    });
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
    },
    python_script: {
      get() {
        return this.script.contents;
      }
    }
  },
  methods: {
    updateCode(code) {
      this.$store.commit("updateScript", {
        uid: this.script.uid,
        synced: false,
        contents: code
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
  margin-bottom: 70px;
  max-width: 800px;
  border-radius: 12px;

  h2 {
    font-size: 1.3rem;
    font-weight: 600;
  }

  .header {
    display: flex;

    .button {
      margin-top: 15px;
      margin-left: 18px;
      display: block;
      padding: 5px 15px 5px 12px;
    }
  }

  a.raw {
    color: #1b9fff;
    margin-top: 10px;
    display: block;
    font-size: 1.05rem;
    transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms color;

    &:hover {
      cursor: pointer;
      color: darken(#1b9fff, 3%);
    }
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

.prism-editor-wrapper {
  border-radius: 12px;
}

.triggers,
.requirements {
  width: 100%;
  background: #101010;
  border-radius: 12px;
  min-height: 400px;

  .empty {
    width: 100%;
    height: 400px;
    display: flex;
    justify-content: center;
    text-align: center;
    align-items: center;
    flex-direction: column;

    h2,
    p {
      opacity: 0.6;
      font-weight: 300;
    }

    h2 {
      font-size: 1.95rem;
      margin-bottom: 10px;
    }

    p {
      max-width: 60%;
      font-size: 1.1rem;
      line-height: 1.6em;
    }
  }
}
</style>
