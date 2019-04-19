<template>
  <div class="home">

    <b-loading :is-full-page="true" :active.sync="isLoading" :can-cancel="false"></b-loading>

    <h2 class="bold">Scripts
      <b-button @click="newScriptModal" size="is-small" type="is-info">
        Add new
      </b-button>
    </h2>

    <div class="columns">
      <div class="column is-one-third">


        <div v-for="s in scripts">
          <div @click="selectScript(s.uid)">
            <Script :script="s" />
          </div>
        </div>
      </div>
      <div class="column">
        <ScriptEditor v-if="selectedScript != null" :script="getScript(this.selectedScript)" />

        <div class="no-script">
          <p v-if="selectedScript == null">No script selected.</p>
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

      this.selectedScript = uid
      console.log(uid)

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
          message: `Please choose a name for your script`,
          inputAttrs: {
              placeholder: 'e.g. Bitcoin Price Check',
              maxlength: 50
          },
          onConfirm: (value) => this.newScript(value)
      })
    },

    newScript(name) {
      this.isLoading = true

      this.$http.post(this.api + '/script/null', {name:name}).then(response => {
        console.log(response)

        this.$toast.open({
            message: '\''+ name +'\' created successfully.',
            type: 'is-success'
        })

        this.isLoading = false
      }).catch(error => {
        this.$toast.open({
            message: '\''+ name +'\' failed to create.',
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
</style>
