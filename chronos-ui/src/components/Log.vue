<template>
  <div class="log">
    <v-collapse-wrapper>
      <div class="log-header">
        <div class="log-status">
          <div class="icon ok" v-if="log.exitcode === 0">
            <i class="material-icons">check</i>
          </div>

          <div class="icon error" v-else>
            <i class="material-icons">close</i>
          </div>
        </div>

        <p class="log-date">{{ log.date }}</p>

        <div class="log-expand" v-collapse-toggle>
          <i class="material-icons">keyboard_arrow_down</i>
        </div>
      </div>

      <div v-collapse-content>
        <h3>stdout</h3>
        <pre>{{ log.stdout }}</pre>

        <h3>stderr</h3>
        <pre>{{ log.stderr }}</pre>
      </div>
    </v-collapse-wrapper>
  </div>
</template>

<script>
export default {
  name: "Log",
  props: {
    log: {
      required: true,
      type: Object
    }
  }
};
</script>

<style lang="scss" scoped>
.vc-collapse {
  width: 100%;
  background: #181818;
  margin-bottom: 16px;
  padding: 14px 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;

  p {
    margin: 0;
    margin-top: 9px;
    font-weight: 600;
  }

  .v-collapse-content {
    max-height: 0px;
    overflow: hidden;
    transition: cubic-bezier(0, 1, 0, 1) 300ms max-height;
  }

  .v-collapse-content-end {
    max-height: 500px;
    //transition: cubic-bezier(0.075, 0.82, 0.165, 1) 300ms max-height;
  }
}

.log-header {
  display: flex;
}

.log-status {
  width: 36px;
  margin-right: 20px;

  .icon {
    //margin-top: 2px;
    border-radius: 100px;

    i {
      font-size: 1.6rem;
    }

    &.ok {
      background: var(--green);
      padding: 7px 5px 1px 5px;
    }

    &.error {
      background: var(--red);
      padding: 7px 5px 2px 5px;
    }
  }
}

.log-expand {
  margin-left: auto;

  &:hover {
    cursor: pointer;
  }

  i {
    font-size: 2rem;
    user-select: none;
  }
}
</style>
