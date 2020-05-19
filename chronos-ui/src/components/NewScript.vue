<template>
  <modal name="new-script" height="auto">
    <div class="new-script">
      <h2 class="modal-title">Create new script</h2>

      <form @submit.prevent="newScript">
        <label>
          Script name
          <input
            type="text"
            name="script_name"
            placeholder="Please enter a name for your script"
            v-model="scriptName"
            :class="{ 'has-error': error !== '' && canError }"
            @input="checkScript"
          />

          <div class="error" v-if="error !== '' && canError">
            <i class="material-icons">error</i> <span>{{ this.error }}</span>
          </div>
        </label>

        <button
          type="submit"
          class="button just-icon"
          :class="{ disabled: this.disabled }"
        >
          <i class="material-icons">check</i>
        </button>
      </form>
    </div>
  </modal>
</template>

<script>
import api from "@/api";

export default {
  name: "NewScript",
  data() {
    return {
      scriptName: "",
      disabled: true,
      error: "",
      canError: false
    };
  },
  methods: {
    open() {
      this.$modal.show("new-script");
    },
    close() {
      this.$modal.hide("new-script");
    },
    checkScript() {
      this.checkError();
      this.canError = false;

      if (this.scriptName != "") {
        this.disabled = false;
      } else {
        this.disabled = true;
      }
    },
    checkError() {
      if (this.scriptName == "") {
        this.error = "You must enter a script name";
        return true;
      } else {
        this.error = "";
        return false;
      }
    },
    newScript() {
      this.canError = true;

      if (!this.checkError()) {
        api.createScript(this.scriptName);
        this.scriptName = "";
        this.canError = false;
        this.close();
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.new-script {
  padding: 30px 50px;
}

h2.modal-title {
  font-weight: 400;
  text-align: center;
  margin-bottom: 45px;
}

form {
  label {
    font-weight: 500;
    font-size: 1.2rem;
    opacity: 0.8;
  }

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

    &.has-error {
      border: 1px solid var(--red);
    }
  }

  .error {
    font-weight: 500;
    margin-top: 10px;
    font-size: 1rem;
    color: var(--red);

    i {
      vertical-align: middle;
      font-size: 1.5rem;
    }

    span {
      vertical-align: middle;
    }
  }

  button {
    margin: 40px auto 0 auto;
    display: block;
  }
}
</style>
