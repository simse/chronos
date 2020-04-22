<template>
  <div class="home">

    <b-loading :is-full-page="true" :active.sync="isLoading" :can-cancel="false"></b-loading>

    <div class="columns is-gapless">
      <div class="column is-one-quarter border-right">

        <div v-for="s in scripts" :key="s.uid">
          <div @click="selectScript(s.uid)" :class="{selected: selectedScript == s.uid}">
            <Script :script="s" />
          </div>
        </div>

        <div class="new-script" @click="newScriptModal">
          <b-icon :icon="'plus-circle'"></b-icon>
          New script
        </div>
      </div>
      <div class="column">
        <ScriptEditor v-if="selectedScript != null" :script="getScript(this.selectedScript)" @script-deleted="selectedScript = null"/>

        <div class="no-script" v-if="selectedScript == null">
          <p>{{ $t('no_script_selected') | capitalize }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import Script from '@/components/Script.vue'
import ScriptEditor from '@/components/ScriptEditor.vue'
import { EventBus } from '@/bus.js';

export default {
  name: 'home',
  components: {
    Script,
    ScriptEditor
  },
  mounted() {
    document.title = 'Chronos'
  },
  data() {
    return {
      isLoading: false,
      selectedScript: null
    }
  },
  computed: {
    scripts() {
      return this.$store.state.scripts
    }
  },
  methods: {
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
      //this.isLoading = true

      this.$http.post(this.api + '/script/null', {name:name}).then((response) => {

        EventBus.$emit('addLoadingScript', {
          name: name,
          uid: response.data.uid
        })

        this.selectedScript = response.data.uid

        const evtSource = new EventSource(this.api + '/events/script_created');

        evtSource.onmessage = function(event) {
          let payload = JSON.parse(event.data).payload

          if(payload.name === name) {
            EventBus.$emit('reloadScripts')
            evtSource.close()
          }
        }
        
      }).catch(() => {
        this.$toast.open({
            message: this.$t('new_script_failed', { name: name }),
            type: 'is-danger'
        })

        //this.isLoading = false
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
    //padding: 150px 0;
    height: calc(100vh - 66px);

    font-size: 2rem;
    opacity: .5;
  }

  .selected .script {
      background: hsl(217, 71%, 53%);
      color: #fff;
      transition: .2s all;

      &:hover {
        background: darken(hsl(217, 71%, 53%), 5%) !important;
      }

      .icon-wrapper {
          background: white !important;

          .icon {
              color: hsl(217, 71%, 53%);
          }
      }
  }

  .border-right {
    border-right: 1px solid lightgray;
    
  }

  .new-script {
    position: fixed;
    bottom: 0;
    padding: 22px;
    text-align: center;
    width: calc(25% - 1px);
    background: #fff;
    font-size: 1.2rem;
    border-top: 1px solid lightgray;

    &:hover {
        cursor: pointer;
      }

    .icon {
      vertical-align: middle;
      padding-bottom: 2px;
    }
  }
</style>
