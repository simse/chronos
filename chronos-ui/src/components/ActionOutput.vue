<template>
  <modal
    :name="modalId"
    height="auto"
    width="50%"
    :scrollable="true"
    @closed="reset"
  >
    <h2 class="modal-title">{{ title }}</h2>

    <pre>{{ output }}<span v-if="this.done && this.output === '\n'" class="no-output">No output from this command</span></pre>

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
  font-size: 1.1rem;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  word-wrap: break-word;
  padding: 0 30px 30px 30px;
  margin: 0;
  font-family: "Fira Code";
}

.button {
  margin: 0 auto 20px auto;
  display: block;
  width: 80px;
  text-align: center;
}

.no-output {
  font-style: italic;
  opacity: 0.6;
}
</style>
