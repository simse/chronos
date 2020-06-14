<template>
  <div>
    <div class="triggers">
      <div class="empty" v-if="triggers.length === 0">
        <h2>No triggers</h2>

        <p>
          Use triggers to execute your scripts on an interval or using Cron
          expressions
        </p>
      </div>

      <div v-else>
        <div v-for="(trigger, index) in triggers" :key="trigger.id">
          <Trigger :trigger="trigger" :index="index" :script_uid="script_uid" />
        </div>
      </div>
    </div>

    <modal name="new-trigger" height="500px">
      <div class="new-trigger">
        <h2 class="modal-title">Add script trigger</h2>

        <form @submit.prevent="addTrigger">
          <select v-model="newTriggerContent.type">
            <option
              v-for="triggerType in triggersTemplate"
              :key="triggerType.type"
              :value="triggerType.type"
              :disabled="triggerType.type === 'none'"
            >
              {{ triggerType.name }}
            </option>
          </select>

          <h3>Trigger options</h3>
          <label
            v-for="field in getFieldsById(newTriggerContent.type)"
            :key="field.key"
          >
            {{ field.name }}

            <input
              :type="field.type"
              v-model="newTriggerContent.options[field.key]"
            />
          </label>

          <button type="submit" class="button just-icon">
            <i class="material-icons">check</i>
          </button>
        </form>
      </div>
    </modal>
  </div>
</template>

<script>
import Trigger from "@/components/Trigger";
import api from "@/api";

export default {
  name: "Triggers",
  props: {
    script_uid: {
      type: String,
      required: true
    }
  },
  components: {
    Trigger
  },
  data() {
    return {
      triggersTemplate: [
        {
          type: "none",
          name: "Please select a trigger...",
          field: []
        },
        {
          type: "interval",
          name: "Interval trigger",
          fields: [
            {
              name: "Interval (in seconds)",
              key: "interval",
              type: "number"
            }
          ]
        },
        {
          type: "cron",
          name: "CRON trigger",
          fields: [
            {
              name: "CRON expression",
              key: "expression",
              type: "text"
            }
          ]
        },
        {
          type: "on_startup",
          name: "On startup trigger",
          fields: []
        }
      ],
      newTriggerContent: {
        type: "none",
        name: "",
        options: {}
      }
    };
  },
  computed: {
    script() {
      return this.$store.getters.getScriptByUid(this.script_uid);
    },
    triggers() {
      if (typeof this.script === "undefined") {
        return [];
      } else {
        return this.script.triggers;
      }
    }
  },
  methods: {
    newTrigger() {
      this.$modal.show("new-trigger");
    },
    getTriggerById(id) {
      return this.triggersTemplate.find(element => {
        return element.type === id;
      });
    },
    getFieldsById(id) {
      return this.getTriggerById(id).fields;
    },
    addTrigger() {
      this.newTriggerContent.name = this.getTriggerById(
        this.newTriggerContent.type
      ).name;

      let currentTriggers = this.script.triggers;
      currentTriggers.push(this.newTriggerContent);
      this.$store.commit("updateScript", {
        uid: this.script.uid,
        triggers: currentTriggers,
        synced: false,
        internal: true
      });
      api.saveScriptByUid(this.script_uid);
      this.$modal.hide("new-trigger");
      this.newTriggerContent = {
        type: "none",
        name: "",
        options: {}
      };
    }
  }
};
</script>

<style lang="scss" scoped>
.triggers {
  padding: 18px;
}

.new-trigger {
  padding: 30px 50px;

  h3 {
    font-weight: 500;
    margin-top: 50px;
  }
}

form {
  display: flex;
  height: 320px;
  flex-direction: column;
  box-sizing: border-box;

  select,
  input {
    display: block;
    margin-top: 15px;
    width: 100%;
    font-size: 1.3rem;
    padding: 12px 14px;
    border-radius: 8px;
    border: 0;
    outline: 0;
    box-sizing: border-box;
    background: #181818;
    color: #fff;
    font-family: "Inter";
  }

  button {
    margin: auto auto 0 auto;
    display: block;
  }
}
</style>
