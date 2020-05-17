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

          <!--ScriptItem :script="script" :index="index + 1" /-->
        </div>
      </div>
    </div>

    <div class="content">
      Hello!
    </div>
  </div>
</template>

<script>
import ScriptItem from "@/components/ScriptItem";
import NewScript from "@/components/NewScript";
import store from "@/store/index.js";

export default {
  name: "Scripts",
  components: {
    ScriptItem,
    NewScript
  },
  computed: {
    scripts() {
      return this.$store.state.scripts;
    }
  },
  methods: {
    openNewScript() {
      this.$refs.newScript.open();
    },
    test() {
      store.commit("addScriptLoading", {
        name: "Hello",
        uid: "hello"
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.scripts {
  display: grid;
  grid-template-columns: 400px auto;
}

.sidebar {
  border-right: 1px rgba(0, 0, 0, 0.3) solid;
  height: 100vh;
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

.content {
  padding-left: 50px;
}
</style>
