<template>
  <div class="script-editor">
    <h1>{{ local_script.name }}</h1>
    <p v-if="local_script.loading">Loading...</p>

    <div class="s">
      <!--h3>
        <strong>{{ this.$t('quick_actions') }}</strong>
      </h3-->

      <b-button
        @click="install_requirements"
        size="is-standard"
        type="is-info"
        :class="{'is-loading':isInstallingPip}"
        rounded
      >{{ this.$t('install_pip_requirements') }}</b-button>

      <b-button
        @click="execute"
        size="is-standard"
        type="is-info"
        :class="{'is-loading':isExecuting}"
        rounded
      >{{ this.$t('execute') }}</b-button>

      <b-button
        @click="deletePrompt"
        size="is-standard"
        type="is-danger"
        rounded
      >{{ this.$t('delete') }}</b-button>
    </div>

    <b-collapse class="card" animation="slide" aria-id="contentIdForA11y3">
      <div slot="trigger" class="card-header" role="button" aria-controls="contentIdForA11y3">
        <p class="card-header-title">
          <b-icon :icon="'information'"></b-icon>&nbsp;&nbsp;
          Script info
        </p>
        <a class="card-header-icon">
          <b-icon :icon="'menu-down'"></b-icon>
        </a>
      </div>
      <div class="card-content">
        <div class="content">
          <div class="s">
            <b-field label="Name">
              <b-input v-model="local_script.name" size="is-large"></b-input>
            </b-field>

            <b-field label="Script enabled">
              <b-switch v-model="local_script.enabled" type="is-success"></b-switch>
            </b-field>
          </div>

          <div class="s">
            <h3>
              <strong>{{ this.$t('pip_requirements') }}</strong>
            </h3>

            <b-field label="requirements.txt">
              <b-input type="textarea" v-model="local_script.requirements"></b-input>
            </b-field>
          </div>

          <div class="s">
            <h3>
              <strong>{{ this.$t('python_script') }}</strong>
            </h3>

            <codemirror :value="local_script.contents" :options="cmOptions" @input="onCodeChange"></codemirror>
          </div>
        </div>
      </div>
    </b-collapse>

    <b-collapse class="card" animation="slide" aria-id="contentIdForA11y3">
        <div slot="trigger" class="card-header" role="button" aria-controls="contentIdForA11y3">
            <p class="card-header-title">
                <b-icon :icon="'information'"></b-icon>&nbsp;&nbsp;
                Triggers
            </p>
            <a class="card-header-icon">
            <b-icon :icon="'menu-down'"></b-icon>
            </a>
        </div>
        <div class="card-content">
            <div class="content">
                <div class="columns">
                    <div class="column">
                        <div class="add-trigger">
                            <b-icon size="is-medium" :icon="'plus-circle'"></b-icon>
                            <p>Add trigger</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </b-collapse>

    <b-collapse class="card" animation="slide" aria-id="contentIdForA11y3">
      <div slot="trigger" class="card-header" role="button" aria-controls="contentIdForA11y3">
        <p class="card-header-title">
          <b-icon :icon="'information'"></b-icon>&nbsp;&nbsp;
          Logs
        </p>
        <a class="card-header-icon">
          <b-icon :icon="'menu-down'"></b-icon>
        </a>
      </div>
      <div class="card-content">
        <div class="content">
          <div class="s">
            <p>
              <em>{{ this.$t('showing_logs', { logs: local_script.logs.length }) }}</em>

              <br />
              <br />
            </p>

            <div v-for="l in local_script.logs" :key="l.date">
              <b-collapse class="card" aria-id="contentIdForA11y3" :open="false">
                <div
                  slot="trigger"
                  slot-scope="props"
                  class="card-header"
                  role="button"
                  aria-controls="contentIdForA11y3"
                >
                  <p class="card-header-title">
                    <b-tag v-if="l.exitcode == 0" type="is-success">OK</b-tag>
                    <b-tag v-if="l.exitcode == 1" type="is-danger">ERROR</b-tag>
                    &nbsp;&nbsp;{{ l.date }}
                  </p>
                  <a class="card-header-icon">
                    <b-icon :icon="props.open ? 'menu-down' : 'menu-up'"></b-icon>
                  </a>
                </div>
                <div class="card-content">
                  <div class="content">
                    <code>stdout</code>
                    <pre>{{ l.stdout }}</pre>

                    <code>stderr</code>
                    <pre>{{ l.stderr }}</pre>
                  </div>
                </div>
              </b-collapse>
            </div>
          </div>
        </div>
      </div>
    </b-collapse>
  </div>
</template>

<script>
import {EventBus} from '@/bus.js'
import { codemirror } from "vue-codemirror";
import "codemirror/mode/python/python.js";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/base16-dark.css";

export default {
  name: "ScriptEditor",
  components: {
    codemirror
  },
  props: {
    script: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      snackbarOpen: false,
      isInstallingPip: false,
      isExecuting: false,
      local_script: this.script,
      cmOptions: {
        tabSize: 4,
        theme: "base16-dark",
        lineNumbers: true,
        line: true
      }
    };
  },
  watch: {
    script: function() {
      if (this.script == undefined) {
        this.local_script = null;
      }

      if (this.local_script.uid !== this.script.uid) {
        this.local_script = this.script;
      } else {
        this.local_script.logs = this.script.logs;

        this.detect_changes();
      }
    },

    local_script: {
      handler() {
        this.detect_changes();
      },
      deep: true
    }
  },
  mounted() {},
  methods: {
    onCodeChange(newCode) {
      this.local_script.contents = newCode;
    },
    detect_changes() {
      if (
        !this.snackbarOpen &&
        JSON.stringify(this.local_script) != JSON.stringify(this.script)
      ) {
          if(this.local_script.loading) {
              this.local_script = this.script;
          } else {
              this.snackbarOpen = true;

        this.$snackbar.open({
          message: this.$t("unsaved_changes"),
          type: "is-info",
          position: "is-top",
          actionText: this.$t("save"),
          indefinite: true,
          onAction: () => {
            this.snackbarOpen = false;
            this.save();
          }
        });
          }

        
      }
    },

    save() {
      this.$http
        .put(this.api + "/script/" + this.local_script.uid, {
          name: this.local_script.name,
          interval: this.local_script.interval,
          triggers: this.local_script.triggers,
          contents: this.local_script.contents,
          requirements: this.local_script.requirements
        })
        .then(() => {});
    },

    install_requirements() {
      this.isInstallingPip = true;

      this.$http
        .get(
          this.api +
            "/script/" +
            this.local_script.uid +
            "/install_requirements"
        )
        .then(response => {
          this.isInstallingPip = false;

          this.$toast.open({
            message: this.$t("pip_requirements_installed"),
            type: "is-success"
          });

          this.$modal.open("<pre>" + response.data.response + "</pre>");
        })
        .catch(() => {
          this.isInstallingPip = false;
          this.$toast.open({
            message: this.$t("pip_requirements_failed"),
            type: "is-danger"
          });
        });
    },

    execute() {
      this.isExecuting = true;

      this.$http
        .get(this.api + "/script/" + this.local_script.uid + "/execute")
        .then(response => {
          this.isExecuting = false;

          let stdout = "no output.";
          if (response.data.response.stdout != "") {
            stdout = response.data.response.stdout;
          }

          let stderr = "no output.";
          if (response.data.response.stderr != "") {
            stdout = response.data.response.stderr;
          }

          let modalContent = "<code>stdout</code><br><pre>" + stdout;
          modalContent += "</pre><br><code>stderr</code><br><pre>" + stderr;
          modalContent += "</pre>";

          this.$modal.open(modalContent);
        })
        .catch(() => {
          this.isExecuting = false;
          this.$toast.open({
            message: this.$t("execute_failed"),
            type: "is-danger"
          });
        });
    },

    deletePrompt() {
      this.$dialog.confirm({
        title: this.$t("delete_script", { name: this.name }),
        message: this.$t("delete_confirm"),
        confirmText: this.$t("delete_confirm_button"),
        type: "is-danger",
        hasIcon: true,
        onConfirm: () => this.delete()
      });
    },

    delete() {
      this.$http
        .delete(this.api + "/script/" + this.local_script.uid)
        .then(() => {
          this.$toast.open({
            message: this.$t("script_deleted"),
            type: "is-success"
          });

          this.$emit("script-deleted");
          EventBus.$emit('reloadScripts')
        })
        .catch(() => {
          this.$toast.open({
            message: this.$t("script_delete_failed"),
            type: "is-danger"
          });
        });
    },

    addTriggerModal() {

    },

    addTrigger() {

    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
.script-editor {
  background: #fff;
  padding: 25px 32px;
  min-height: calc(100vh - 66px);

  h1 {
    margin-bottom: 20px;
    margin-top: 0px;
    font-size: 2.4rem;
    font-weight: 700;
  }
}

.s {
  margin-bottom: 50px;

  h3 {
    margin-bottom: 15px;
    font-size: 1.1rem;
  }
}

.card {
  margin-bottom: 20px;
}

.button {
  margin-right: 10px;
}

.tabs li.is-active a {
  color: hsl(217, 71%, 53%) !important;
}

.add-trigger {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height: 200px;
    width: 200px;
    border: 1px solid lightgray;
    border-radius: 4px;
    transition: .1s background;

    p {
        margin-top: 15px;
    }

    &:hover {
        cursor: pointer;
        background: darken(#fff, 5%);
    }
}
</style>
