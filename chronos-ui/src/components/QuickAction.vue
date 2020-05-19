<template>
  <div class="quick-action" @click="activate">
    <div class="loading" :class="{ 'is-hidden': !loading }">
      <div class="spinner">
        <Spinner line-bg-color="transparent" line-fg-color="var(--blue)" />
      </div>
    </div>

    <div class="icon">
      <i class="material-icons">{{ icon }}</i>
    </div>

    <div class="text">
      <span>{{ text }}</span>
    </div>
  </div>
</template>

<script>
import Spinner from "vue-simple-spinner";
import api from "@/api";

export default {
  name: "QuickAction",
  components: {
    Spinner
  },
  props: {
    icon: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    },
    action: {
      type: String,
      required: true
    },
    script_uid: {
      type: String,
      required: true
    },
    showOutput: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  computed: {
    loading() {
      let script = this.$store.getters.getScriptByUid(this.script_uid);
      if (script === undefined) {
        return false;
      }

      return script.actions[this.action].loading;
    }
  },
  watch: {
    script_uid() {
      this.$forceUpdate();
    }
  },
  methods: {
    activate() {
      if (this.loading) {
        this.showActionOutput();
        return;
      }

      api.scriptAction(this.script_uid, this.action);

      //console.log(this.showOutput);

      if (this.showOutput) {
        this.showActionOutput();
      }
    },
    finish() {},
    showActionOutput() {
      this.$modal.show(this.script_uid + "_" + this.action);
    }
  }
};
</script>

<style lang="scss" scoped>
.quick-action {
  height: 170px;
  width: 170px;
  background: #101010;
  border-radius: 22px;
  text-align: center;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms background,
    cubic-bezier(0.075, 0.82, 0.165, 1) 400ms transform;

  &:hover {
    cursor: pointer;
    background: darken(#101010, 3%);
  }

  &:active {
    transform: scale(0.98);
  }

  .icon,
  .text {
    display: flex;
    justify-content: center;
  }

  .icon {
    height: 50%;
    align-items: flex-end;
  }

  .text {
    height: 40%;
    padding-top: 10%;
  }

  span {
    font-size: 1rem;
    font-weight: 500;
  }

  i {
    color: #fff;
    font-size: 3.5rem;
  }
}

.loading {
  position: absolute;
  background: rgba(0, 0, 0, 0.6);
  width: 170px;
  height: 170px;
  border-radius: 22px;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(6px);
  transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms all;

  .spinner {
    transition: cubic-bezier(0.075, 0.82, 0.165, 1) 200ms opacity;
  }

  &.is-hidden {
    background: transparent;
    backdrop-filter: blur(0);

    .spinner {
      opacity: 0 !important;
    }
  }
}
</style>
