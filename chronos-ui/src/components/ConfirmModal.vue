<template>
  <modal name="confirm" height="auto">
    <h2 class="modal-title">Are you sure?</h2>
    <p>
      When I'm done here, everything about your script will be gone.
    </p>

    <div class="buttons">
      <a class="button grey just-text" @click="cancel">Cancel</a>
      <a class="button red just-text" @click="confirm">Confirm</a>
    </div>
  </modal>
</template>

<script>
import events from "@/events";

export default {
  name: "ConfirmModal",
  mounted() {
    events.$on("confirm", () => {
      this.$modal.show("confirm");
    });
  },
  methods: {
    confirm() {
      events.$emit("confirmed");
      this.$modal.hide("confirm");
    },
    cancel() {
      events.$emit("cancelled");
      this.$modal.hide("confirm");
    }
  }
};
</script>

<style lang="scss" scoped>
h2 {
  padding-top: 50px;
  margin-bottom: 20px !important;
}

p {
  padding: 0 20px 20px 20px;
  text-align: center;
  margin-top: 0;
}

.buttons {
  margin: 40px auto 0 auto;
  display: flex;
  justify-content: space-around;
  max-width: 200px;
  padding-bottom: 50px;
}
</style>
