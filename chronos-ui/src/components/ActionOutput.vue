<template>
  <modal :name="modalId" height="auto" width="75%" :scrollable="true">
    <h2 class="modal-title">{{ title }}</h2>

    <pre>
      {{ output }}
    </pre>

    <a class="button" @click="close" v-if="done">Close</a>
  </modal>
</template>

<script>
import events from "@/events";

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
  data() {
    return {
      lines: [],
      done: false,
      taskId: null
    };
  },
  computed: {
    output() {
      return this.lines.join("");
    }
  },
  mounted() {
    events.$on("_task_output", event => {
      if (event.script_uid === this.uid && event.task === this.action) {
        this.lines.push(event.output + "\n");
        this.taskId = event.task_id;
      }
    });

    events.$on("_task_finished", event => {
      if (event.task_id === this.taskId) {
        this.done = true;
      }
    });
  },
  methods: {
    open() {
      this.$modal.show(this.modalId);
    },
    close() {
      this.$modal.hide(this.modalId);
    },
    reset() {
      this.lines = [];
    }
  }
};
</script>

<style lang="scss" scoped>
pre {
  font-size: 1.2rem;
  white-space: pre-wrap;       /* css-3 */
  white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
  white-space: -pre-wrap;      /* Opera 4-6 */
  white-space: -o-pre-wrap;    /* Opera 7 */
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
