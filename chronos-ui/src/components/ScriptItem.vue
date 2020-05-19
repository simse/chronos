<template>
  <div
    :class="{
      script: true,
      active: isActive,
      dark: this.index % 2 !== 0,
      light: this.index % 2 === 0
    }"
    @click="selectScript"
  >
    <div class="text">
      <h2>{{ script.name }}</h2>

      <span class="last-execution">
        <span v-if="!this.script.loading">Last run: {{ lastRun }}</span>

        <span v-else>Creating...</span>
      </span>
    </div>

    <div class="status">
      <!--div class="icon ok">
        <i class="material-icons">check</i>
      </div-->

      <!--div class="icon warning">
        <i class="material-icons">warning</i>
      </div-->

      <!--div class="icon error">
        <i class="material-icons">close</i>
      </div-->

      <div class="spinner" v-if="this.script.loading">
        <Spinner line-bg-color="transparent" line-fg-color="var(--blue)" />
      </div>

      <div class="icon ok" v-else>
        <i class="material-icons">check</i>
      </div>
    </div>
  </div>
</template>

<script>
import Spinner from "vue-simple-spinner";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";

TimeAgo.addLocale(en);

export default {
  name: "ScriptItem",
  components: {
    Spinner
  },
  props: {
    script: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  },
  computed: {
    isActive() {
      const routeParts = this.$route.path.split("/");

      // decodeURIComponent is neccessary to support non-latin characters
      return (
        decodeURIComponent(routeParts[routeParts.length - 1]) == this.script.uid
      );
    },
    lastRun() {
      if (this.script.logs.length === 0) {
        return "Never";
      } else {
        const timeAgo = new TimeAgo("en-US");
        let datetime = Date.parse(this.script.logs[0].date);

        return timeAgo.format(datetime);
      }
    }
  },
  methods: {
    toUnicode(str) {
      return str
        .split("")
        .map(function(value) {
          var temp = value
            .charCodeAt(0)
            .toString(16)
            .toUpperCase();
          if (temp.length > 2) {
            return "\\u" + temp;
          }
          return value;
        })
        .join("");
    },
    selectScript() {
      this.$router
        .push({
          name: "Script",
          params: {
            script_uid: this.script.uid
          }
        })
        .catch(() => {
          void 0;
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.script {
  display: flex;
  padding: 28px;
  transition: cubic-bezier(0.075, 0.82, 0.165, 1) 0.2s background;

  &:hover {
    background: #090909 !important;
    cursor: pointer;
  }

  &.dark {
    background: #0e0e0e;
  }

  &.light {
    background: #111;
  }

  &.active {
    background: var(--blue);

    h2 {
      font-weight: 600;
    }

    &:hover {
      background: darken(#006ee6, 3%) !important;
    }

    &:active {
      background: darken(#006ee6, 5%) !important;
    }

    .icon {
      background: #fff !important;
      opacity: 0.8;

      i {
        color: #000;
      }
    }
  }
}

.status {
  margin-left: auto;
}

h2 {
  font-size: 1.4rem;
  font-weight: 400;
  margin: 0 0 10px 0;
}

span.last-execution {
  font-size: 0.95rem;
  opacity: 60%;
}

.icon {
  margin-top: 2px;
  border-radius: 100px;

  i {
    font-size: 2.2rem;
  }

  &.ok {
    background: var(--green);
    padding: 10px 9px 5px 9px;
  }

  &.warning {
    background: var(--yellow);
    padding: 6px 9px 8px 9px;
  }

  &.error {
    background: var(--red);
    padding: 10px 9px 5px 9px;
  }
}

.spinner {
  margin-top: 9px;
}
</style>
