<template>
  <div class="trigger">
    <p class="trigger-name">{{ triggerName }}</p>

    <p class="trigger-detail">{{ triggerDetail }}</p>

    <div class="trigger-actions">
      <i class="material-icons" @click="deleteTrigger">delete</i>
    </div>
  </div>
</template>

<script>
import cronstrue from "cronstrue";
import api from "@/api";

export default {
  name: "Trigger",
  props: {
    trigger: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    },
    script_uid: {
      type: String,
      required: true
    }
  },
  computed: {
    triggerName() {
      return this.trigger.name;
    },
    triggerDetail() {
      if (this.trigger.type === "interval") {
        return "Every " + this.trigger.options.interval + " seconds";
      }

      if (this.trigger.type === "cron") {
        return cronstrue.toString(this.trigger.options.expression);
      }

      if (this.trigger.type === "on_startup") {
        return "";
      }

      return "";
    }
  },
  methods: {
    deleteTrigger() {
      this.$store.commit("deleteTrigger", {
        uid: this.script_uid,
        trigger_index: this.index
      });
      api.saveScriptByUid(this.script_uid);
    }
  }
};
</script>

<style lang="scss" scoped>
.trigger {
  width: 100%;
  background: #181818;
  margin-bottom: 18px;
  padding: 14px 16px;
  border-radius: 12px;
  display: flex;

  p {
    margin: 0;
  }

  .trigger-name {
    font-weight: 700;
    min-width: 150px;
  }

  .trigger-detail {
    margin-left: 20px;
  }

  .trigger-actions {
    margin-left: auto;

    i {
      font-size: 1.2rem;
      vertical-align: middle;
      transition: cubic-bezier(0.075, 0.82, 0.165, 1) 200ms background;

      &:hover {
        cursor: pointer;
      }
    }
  }
}
</style>
