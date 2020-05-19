<template>
  <modal
    :name="modalId"
    height="auto"
    width="75%"
    :scrollable="true"
    @closed="reset"
  >
    <h2 class="modal-title">{{ title }}</h2>

    <pre>
      {{ output }}
    </pre>

    <a class="button" @click="close" v-if="done">Close</a>
  </modal>
</template>

<script>
export default {
  name: "ActionOutput",
  props: {
    action: {
      type: String,
      required: true
    },
    uid: {
      type: String,
      required: true
    },
    modalId: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    }
  },
  computed: {
    output() {
      let script = this.$store.getters.getScriptByUid(this.uid);

      if (typeof script === "undefined") {
        return "";
      }

      return script.actions[this.action].output;
    },
    done() {
      let script = this.$store.getters.getScriptByUid(this.uid);

      if (typeof script === "undefined") {
        return false;
      }

      return script.actions[this.action].done;
    }
  },
  methods: {
    open() {
      this.$modal.show(this.modalId);
    },
    close() {
      this.$modal.hide(this.modalId);
    },
    reset() {
      if (this.done) {
        this.$store.commit("resetActionOutput", {
          scriptUid: this.uid,
          action: this.action
        });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
pre {
  font-size: 1.2rem;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  word-wrap: break-word;
  padding: 20px;
  margin-bottom: 0;
}

.button {
  margin: 0 auto 20px auto;
  display: block;
  width: 80px;
  text-align: center;
}
</style>
