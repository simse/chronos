<template>
  <div class="script">
    <div class="icon-wrapper success" v-if="false">
      <b-icon
          icon="check"
          size="is-medium">
      </b-icon>
    </div>

    <div class="icon-wrapper warning" v-if="false">
      <b-icon
          icon="alert"
          size="is-medium">
      </b-icon>
    </div>

    <div class="icon-wrapper info" v-if="false">
      <b-icon
          icon="information-variant"
          size="is-medium">
      </b-icon>
    </div>

    <div class="meta">
      <h2>{{ script.name }}</h2>
      <p>{{ $t('last_run') | capitalize }}: {{ lastRun }}</p>
    </div>
  </div>
</template>

<script>
import TimeAgo from 'javascript-time-ago'
import en from 'javascript-time-ago/locale/en'
import da from 'javascript-time-ago/locale/da'


TimeAgo.addLocale(en)
TimeAgo.addLocale(da)

export default {
  name: 'Script',
  props: {
    script: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      now: null,
      lastRun: ''
    }
  },
  mounted() {
      this.now = Date.now()

    this.$nextTick(function () {
        window.setInterval(() => {
            this.now = Date.now()
        }, 2000);
    })
  },
  watch: {
    now() {
      if(this.script.logs.length == 0) {
        this.lastRun = 'Never run'
      } else if(this.script.logs.length > 0) {
        let log_date = Date.parse(this.script.logs[0].date)

        const timeAgo = new TimeAgo('en')
        this.lastRun = timeAgo.format(log_date)
      } else {
        this.lastRun = 'not sure'
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.script {
  display: flex;
  align-items: center;
  padding: 12px 8px;
  background: #fff;
  border-bottom: 1px solid lightgrey;
  //border-right: 1px solid lightgrey;

  &.selected {
    background: hsl(217, 71%, 53%);
    color: #fff;

    .icon-wrapper {
      background: transparent;
      //color: #111;
    }
  }

  &:hover {
    background: lightgray;
    cursor: pointer;
  }

  .meta {
    margin-left: 20px;
  }

  .icon-wrapper {
    color: #fff;
    border-radius: 100%;
    padding: 10px 10px 7px 10px;
  }

  .info {
    background: hsl(204, 86%, 53%);
  }

  .success {
    background: hsl(141, 71%, 48%);
  }

  .warning {
    background: hsl(48, 100%, 67%);
  }

  .error {
    background: hsl(348, 100%, 61%);
  }

  h2 {
    font-size: 1.4rem;
  }
}
</style>
