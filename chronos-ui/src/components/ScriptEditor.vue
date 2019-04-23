<template>
  <div class="script-editor">
    <h1>{{ local_script.name }}</h1>

    <div class="s">
      <h3><strong>Quick actions</strong></h3>

      <b-button @click="install_requirements" size="is-standard" type="is-info" :class="{'is-loading':isInstallingPip}">
        Install Pip requirements
      </b-button>

      <b-button @click="execute" size="is-standard" type="is-info" :class="{'is-loading':isExecuting}">
        Execute
      </b-button>

      <b-button @click="deletePrompt" size="is-standard" type="is-danger">
        Delete
      </b-button>
    </div>

    <div class="s">
      <h3><strong>Script info</strong></h3>

      <b-field label="Name">
          <b-input v-model="local_script.name" size="is-large"></b-input>
      </b-field>

      <b-field label="Interval (seconds)">
          <b-input v-model="local_script.interval" type="integer" size="is-large"></b-input>
      </b-field>

      <b-field label="Script enabled">
          <b-switch v-model="local_script.enabled"
          type="is-success">

          </b-switch>
      </b-field>
    </div>


    <div class="s">
      <h3><strong>Pip requirements</strong></h3>

      <b-field label="requirements.txt">
          <b-input type="textarea" v-model="local_script.requirements"></b-input>
      </b-field>
    </div>


    <div class="s">
      <h3><strong>Python script</strong></h3>

      <prism-editor v-model="local_script.contents" language="python"></prism-editor>
    </div>


    <div class="s">
      <h3><strong>Logs</strong></h3>

      <p>
        <em>Showing {{ local_script.logs.length }} logs</em>

        <br />
        <br />
      </p>

      <div v-for="l in local_script.logs">
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
                    <pre>{{ l.text }}</pre>
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

        if(
          !this.snackbarOpen &&
          (this.local_script.name != this.script.name ||
          this.local_script.interval != this.script.interval ||
          this.local_script.enabled != this.script.enabled ||
          this.local_script.contents != this.script.contents ||
          this.local_script.requirements != this.script.requirements)
        ) {
          this.snackbarOpen = true

          this.$snackbar.open({
                message: 'You have unsaved changes.',
                type: 'is-info',
                position: 'is-top',
                actionText: 'Save',
                indefinite: true,
                onAction: () => {
                    this.snackbarOpen = false
                    this.save()
                }
            })

        }


      }
    }
  },
  mounted() {

  },
  methods: {

    save() {

      this.$http.put(this.api + '/script/' + this.local_script.uid, {
        name: this.local_script.name,
        interval: this.local_script.interval,
        enabled: this.local_script.enabled,
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
            message: 'Pip requirements installed.',
            type: 'is-success'
        })
      }).catch(error => {
        this.isInstallingPip = false;
        this.$toast.open({
            message: 'Couldn\'t install Pip requirements',
            type: 'is-danger'
        })
      })

    },

    execute() {

      this.isExecuting = true;

      this.$http.get(this.api + '/script/' + this.local_script.uid + '/execute').then(response => {
        this.isExecuting = false;

        this.$modal.open('<pre>' + response.data.response + '</pre>')
      }).catch(error => {
        this.isExecuting = false;
        this.$toast.open({
            message: 'Couldn\'t execute script.',
            type: 'is-danger'
        })
      })

    },

    deletePrompt() {

      this.$dialog.confirm({
          title: 'Deleting script \'' + this.local_script.name + '\'',
          message: 'Are you sure you want to <b>delete</b> your script? This action cannot be undone.',
          confirmText: 'Delete Script',
          type: 'is-danger',
          hasIcon: true,
          onConfirm: () => this.delete()
      })


    },

    delete() {

      this.$http.delete(this.api + '/script/' + this.local_script.uid).then(response => {

        this.$toast.open({
            message: 'Deleted script successfully.',
            type: 'is-success'
        })

      }).catch(error => {
        this.$toast.open({
            message: 'Couldn\'t delete script.',
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
