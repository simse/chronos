<template>
  <div class="script-editor">
    <h1>{{ local_script.name }}</h1>

    <div class="s">
      <h3><strong>{{ this.$t('quick_actions') }}</strong></h3>

      <b-button @click="install_requirements" size="is-standard" type="is-info" :class="{'is-loading':isInstallingPip}">
        {{ this.$t('install_pip_requirements') }}
      </b-button>

      <b-button @click="execute" size="is-standard" type="is-info" :class="{'is-loading':isExecuting}">
        {{ this.$t('execute') }}
      </b-button>

      <b-button @click="deletePrompt" size="is-standard" type="is-danger">
        {{ this.$t('delete') }}
      </b-button>
    </div>

    <div class="s">
      <h3><strong>{{ this.$t('script_info') }}</strong></h3>

      <b-field label="Name">
          <b-input v-model="local_script.name" size="is-large"></b-input>
      </b-field>



      <b-field label="Script enabled">
          <b-switch v-model="local_script.enabled"
          type="is-success">

          </b-switch>
      </b-field>
    </div>


    <div class="s">
        <h3><strong>{{ this.$t('triggers') }}</strong></h3>

        <b-field :label="this.$t('enable_interval_trigger')">
            <b-switch v-model="local_script.interval_enabled" type="is-success"></b-switch>
        </b-field>

        <b-field :label="this.$t('interval')" v-show="local_script.interval_enabled">
            <b-input v-model.number="local_script.interval" type="number" size="is-large"></b-input>
        </b-field>

        <br />

        <b-field :label="this.$t('enable_cron_trigger')">
            <b-switch v-model="local_script.cron_enabled" type="is-success"></b-switch>
        </b-field>

        <b-field :label="this.$t('cron_expression')" v-show="local_script.cron_enabled">
            <b-input v-model="local_script.cron" type="number" size="is-large"></b-input>
        </b-field>
    </div>


    <div class="s">
      <h3><strong>{{ this.$t('pip_requirements') }}</strong></h3>

      <b-field label="requirements.txt">
          <b-input type="textarea" v-model="local_script.requirements"></b-input>
      </b-field>
    </div>


    <div class="s">
      <h3><strong>{{ this.$t('python_script') }}</strong></h3>

      <prism-editor v-model="local_script.contents" language="python"></prism-editor>
    </div>


    <div class="s">
      <h3><strong>{{ this.$t('logs') }}</strong></h3>

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
                aria-controls="contentIdForA11y3">
                <p class="card-header-title">
                    <b-tag v-if="l.exitcode == 0" type="is-success">OK</b-tag><b-tag v-if="l.exitcode == 1" type="is-danger">ERROR</b-tag>&nbsp;&nbsp;{{ l.date }}
                </p>
                <a class="card-header-icon">
                    <b-icon
                        :icon="props.open ? 'menu-down' : 'menu-up'">
                    </b-icon>
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
</template>

<script>
import '@/prism.js';
import "prismjs/themes/prism.css";

import PrismEditor from 'vue-prism-editor'

export default {
  name: 'ScriptEditor',
  components: {
    PrismEditor
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
      local_script: this.script
    }

  },
  watch: {
    script: function() {

      if(this.script == undefined) {
        this.local_script = null
      }

      if(this.local_script.uid !== this.script.uid) {
        this.local_script = this.script
      } else {

        this.local_script.logs = this.script.logs

        this.detect_changes()
      }
    },

    local_script: {
        handler: function (val, oldVal) {
            this.detect_changes()
        },
        deep: true
    }
  },
  mounted() {

  },
  methods: {
    detect_changes() {

        if(
          !this.snackbarOpen &&
          JSON.stringify(this.local_script) != JSON.stringify(this.script)
        ) {
          this.snackbarOpen = true

          this.$snackbar.open({
                message: this.$t('unsaved_changes'),
                type: 'is-info',
                position: 'is-top',
                actionText: this.$t('save'),
                indefinite: true,
                onAction: () => {
                    this.snackbarOpen = false
                    this.save()
                }
            })
        }

        //if(this.snackbarOpen &&
        //    JSON.stringify(this.local_script) != JSON.stringify(this.script)
        //) {
        //    //this.$snackbar.close()
        //    this.snackbarOpen = false
        //}
    },

    save() {

      this.$http.put(this.api + '/script/' + this.local_script.uid, {
        name: this.local_script.name,
        interval: this.local_script.interval,
        cron: this.local_script.cron,
        enabled: this.local_script.enabled,
        interval_enabled: this.local_script.interval_enabled,
        cron_enabled: this.local_script.cron_enabled,
        contents: this.local_script.contents,
        requirements: this.local_script.requirements
      }).then(response => {

      })

    },

    install_requirements() {

      this.isInstallingPip = true;

      this.$http.get(this.api + '/script/' + this.local_script.uid + '/install_requirements').then(response => {
        this.isInstallingPip = false;

        this.$toast.open({
            message: this.$t('pip_requirements_installed'),
            type: 'is-success'
        })

        this.$modal.open('<pre>' + response.data.response + '</pre>')
      }).catch(error => {
        this.isInstallingPip = false;
        this.$toast.open({
            message: this.$t('pip_requirements_failed'),
            type: 'is-danger'
        })
      })

    },

    execute() {

      this.isExecuting = true;

      this.$http.get(this.api + '/script/' + this.local_script.uid + '/execute').then(response => {
        this.isExecuting = false;

        let stdout = 'no output.';
        if(response.data.response.stdout != '') {
          stdout = response.data.response.stdout
        }

        let stderr = 'no output.';
        if(response.data.response.stderr != '') {
          stdout = response.data.response.stderr
        }

        let modalContent = '<code>stdout</code><br><pre>' + stdout
        modalContent += '</pre><br><code>stderr</code><br><pre>' + stderr
        modalContent += '</pre>'

        this.$modal.open(modalContent)
      }).catch(error => {
        this.isExecuting = false;
        this.$toast.open({
            message: this.$t('execute_failed'),
            type: 'is-danger'
        })
      })

    },

    deletePrompt() {

      this.$dialog.confirm({
          title: this.$t('delete_script', { name: this.name }),
          message: this.$t('delete_confirm'),
          confirmText: this.$t('delete_confirm_button'),
          type: 'is-danger',
          hasIcon: true,
          onConfirm: () => this.delete()
      })


    },

    delete() {

      this.$http.delete(this.api + '/script/' + this.local_script.uid).then(response => {

        this.$toast.open({
            message: this.$t('script_deleted'),
            type: 'is-success'
        })

      }).catch(error => {
        this.$toast.open({
            message: this.$t('script_delete_failed'),
            type: 'is-danger'
        })
      })

    },

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.script-editor {
  background: #fff;
  padding: 25px 32px;
  box-shadow: 0 4px 6px rgba(50,50,93,.11), 0 1px 3px rgba(0,0,0,.08);
  border-radius: 8px;
  margin-top: 17px;


  h1 {
    margin-bottom: 20px;
    margin-top: 0px;
    font-size: 2rem;
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

button {
  margin-right: 10px;
}
</style>
