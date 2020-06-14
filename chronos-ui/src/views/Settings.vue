<template>
  <div class="settings">
    <h1 class="page-title">Settings</h1>

    <!--div class="container">
      <div class="sidebar">
        <h3>General</h3>

        <ul>
          <li>
            <a><i class="material-icons">brush</i> Appearance</a>
          </li>
        </ul>
      </div>

      <div class="content">
        <div class="section">
          <h2 class="section-title">Appearance</h2>
        </div>
      </div>
    </div>
  </div-->
</template>

<script>
export default {
  name: "Settings"
};
</script>

<style lang="scss" scoped>
.container {
  display: grid;
  grid-template-columns: 340px auto;
  column-gap: 2%;
  padding: 20px 20px 20px 40px;
}

.sidebar,
.content {
  border-radius: 12px;
  background: #101010;
}

.sidebar {
  h3 {
    font-weight: 400;
    margin-left: 22px;
  }

  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;

    a {
      padding: 22px;
      display: block;

      i {
        vertical-align: middle;
        margin-right: 12px;
        margin-bottom: 3px;
      }
    }
  }
}

.content {
  padding: 20px;

  h2.section-title {
    font-size: 2rem;
    font-weight: 400;
    margin-left: 20px;
  }
}
</style>
