<template>
  <div class="script-viewer">
    <h1 v-if="script_uid === undefined">No script selected</h1>

    <h1 v-else>{{ script_uid }}</h1>
  </div>
</template>

<script>
export default {
  name: "ScriptViewer",
  props: {
    script_uid: {
      type: String,
      required: false
    }
  }
};
</script>

<style lang="scss" scoped>
.script-viewer {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
</style>
