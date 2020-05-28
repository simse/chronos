<template>
  <div class="logs">
    <div class="log" v-for="log in logs" :key="log.date">
      <Log :log="log" />
    </div>
  </div>
</template>

<script>
import Log from "@/components/Log";

export default {
  name: "Logs",
  components: {
    Log
  },
  props: {
    logs: {
      required: true
    }
  }
};
</script>

<style lang="scss" scoped>
.logs {
  width: 100%;
  background: #101010;
  border-radius: 12px;
  min-height: 400px;
  padding: 16px;
}
</style>
