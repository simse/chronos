<template>
  <div>
    <div
      class="save"
      :class="{ loading: scriptEditorBar.saveButton.loading }"
      @click="saveScriptButton"
    >
      <i
        class="material-icons"
        v-if="
          !scriptEditorBar.saveButton.loading &&
            !scriptEditorBar.saveButton.finished
        "
      >
        save
      </i>

      <svg
        v-if="scriptEditorBar.saveButton.finished"
        class="checkmark"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 52 52"
      >
        <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" />
        <path
          class="checkmark__check"
          fill="none"
          d="M14.1 27.2l7.1 7.2 16.7-16.8"
        />
      </svg>

      <span>{{ scriptEditorBar.saveButton.text }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "BottomBar"
};
</script>

<style lang="scss" scoped>
.bottom-bar {
  
}
</style>