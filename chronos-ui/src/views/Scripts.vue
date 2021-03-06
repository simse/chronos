<template>
  <div class="scripts">
    <div class="sidebar">
      <div class="header">
        <div class="left">
          <h2>Scripts</h2>
        </div>

        <div class="right">
          <NewScript ref="newScript" />
          <a class="button primary" @click="openNewScript">
            <i class="material-icons">add</i> New script
          </a>
        </div>
      </div>

      <div class="list">
        <div v-for="(script, index) in scripts" :key="script.uid">
          <ScriptItem :script="script" :index="index" />
        </div>

        <p v-if="scripts.length == 0" class="no-scripts">
          You don't have any scripts yet.
        </p>
      </div>
    </div>

    <div class="content">
      <ScriptViewer :script_uid="script_uid" />
    </div>
  </div>
</template>

<script>
import ScriptItem from "@/components/ScriptItem";
import NewScript from "@/components/NewScript";
import ScriptViewer from "@/components/ScriptViewer";
import events from "@/events";
import api from "@/api";

export default {
  name: "Scripts",
  components: {
    ScriptItem,
    NewScript,
    ScriptViewer
  },
  props: {
    script_uid: {
      required: false,
      type: String
    }
  },
  computed: {
    scripts() {
      const unsortedScripts = this.$store.state.scripts;

      // Sort scripts by creation date
      let sortedScripts = unsortedScripts.sort((a, b) => {
        const dateA = new Date(a.created);
        const dateB = new Date(b.created);

        return dateA < dateB ? 1 : -1;
      });

      return sortedScripts;
    }
  },
  mounted() {
    events.$on("prompt-save", () => {
      this.$buefy.snackbar.open({
        indefinite: true,
        message: "You have unsaved changes",
        position: "is-top",
        onAction: api.saveAllScripts
      });
    });
  },
  methods: {
    openNewScript() {
      this.$refs.newScript.open();
    }
  }
};
</script>

<style lang="scss" scoped>
.scripts {
  display: grid;
  grid-template-columns: 400px auto;
  overflow-y: hidden;
  height: 100vh;
}

.content {
  overflow-y: scroll;
  max-height: 100vh;
  padding-bottom: 100px;
}

.sidebar {
  border-right: 1px rgba(0, 0, 0, 0.3) solid;
  height: 100vh;
  max-height: 100vh;
  overflow-y: scroll;
  padding-bottom: 20px;
  box-sizing: border-box;

  // Chromium (Edge, Chrome) scrollbar styling
  &::-webkit-scrollbar {
    width: 5px;
    height: 8px;
    background-color: #666; /* or add it to the track */
  }

  &::-webkit-scrollbar-thumb {
    background: #111;
  }

  // Firefox scrollbar styling
  scrollbar-width: thin;
}

.header {
  display: flex;
  padding: 25px;

  .right {
    margin-left: auto;
  }

  h2 {
    font-weight: 400;
    opacity: 0.9;
  }

  a {
    margin-top: 12px;
    display: block;
  }
}

.no-scripts {
  opacity: 0.7;
  padding: 50px;
  text-align: center;
}
</style>
