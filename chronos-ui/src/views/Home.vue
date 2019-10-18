<template>
  <div class="home">

    <b-loading :is-full-page="true" :active.sync="isLoading" :can-cancel="false"></b-loading>

    <h2 class="bold">{{ $t('scripts') | capitalize }}
      <b-button @click="newScriptModal" size="is-small" type="is-info">
        {{ $t('new_script') | capitalize }}
      </b-button>
    </h2>

    <div class="columns">
      <div class="column is-one-third">


        <div v-for="s in scripts">
          <div @click="selectScript(s.uid)" :class="{selected: selectedScript == s.uid}">
            <Script :script="s" />
          </div>
        </div>
      </div>
      <div class="column">
        <ScriptEditor v-if="selectedScript != null" :script="getScript(this.selectedScript)" />

        <div class="no-script">
          <p v-if="selectedScript == null">{{ $t('no_script_selected') | capitalize }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
// @ is an alias to /src
import Script from '@/components/Script.vue'
import ScriptEditor from '@/components/ScriptEditor.vue'

export default {
  name: 'home',
  components: {
    Script,
    ScriptEditor
  },
  mounted() {

    document.title = 'Chronos'

    this.loadAllScripts();

    this.$nextTick(function () {
        window.setInterval(() => {
            this.loadAllScripts();
        }, 2000);
    })

  },
  data() {

    return {
      url: this.api,
      isLoading: false,
      selectedScript: null,
      scripts: []
    }

  },
  methods: {

    loadAllScripts() {

      this.$http.get(this.url + '/scripts').then(response => {
        this.scripts = response.data
      })

    },

    selectScript(uid) {
        if(this.selectedScript == uid) {
            this.selectedScript = null;
        } else {
            this.selectedScript = uid;
        }
    },

    getScript(uid) {

      for (const s of this.scripts) {
        if(s.uid === uid) {
          return s
        }
      }

    },

    newScriptModal() {
      this.$dialog.prompt({
          message: this.$t('new_script_name'),
          inputAttrs: {
              placeholder: this.$t('eg_name'),
              maxlength: 50,
          },
          confirmText: this.$t('done'),
          cancelText: this.$t('cancel'),
          onConfirm: (value) => this.newScript(value)
      })
    },

    newScript(name) {
      this.isLoading = true

      this.$http.post(this.api + '/script/null', {name:name}).then(response => {
        this.$toast.open({
            message: this.$t('new_script_succcesful', { name: name }),
            type: 'is-success'
        })

        this.isLoading = false
      }).catch(error => {
        this.$toast.open({
            message: this.$t('new_script_failed', { name: name }),
            type: 'is-danger'
        })

        this.isLoading = false
      })
    }
  }
}
</script>

<style lang="scss">
  h2.bold {
    font-weight: bold;
    font-size: 1.4rem;
  }

  .no-script {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 150px 0;

    font-size: 2rem;
    opacity: .5;
  }

  .selected .script {
      background: hsl(217, 71%, 53%);
      color: #fff;
      transition: .2s all;

      .icon-wrapper {
          background: white !important;

          .icon {
              color: hsl(217, 71%, 53%);
          }
      }
  }
</style>
