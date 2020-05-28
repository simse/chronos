<template>
  <div class="navigation">
    <div class="logo">
      <img src="@/assets/logo.svg" />
    </div>

    <div class="items">
      <router-link
        v-for="route in routes"
        :key="route.name"
        :to="route.path"
        v-slot="{ href, route, navigate }"
      >
        <a :href="href" @click="navigate">
          <div :class="{ item: true, active: isActive(route.path) }">
            <i class="material-icons">{{ icon(route.path) }}</i>
          </div>
        </a>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Navigation",
  computed: {
    routes() {
      const routes = this.$router.options.routes;

      return routes.filter(value => {
        if (value.path !== "/scripts/:script_uid" && value.path !== "/") {
          return value;
        }
      });
    }
  },
  methods: {
    icon(routePath) {
      const icons = {
        "/": "home",
        "/scripts": "code",
        "/settings": "settings",
        "/logs": "subject"
      };

      return icons[routePath];
    },
    isActive(path) {
      const currentPath = this.$router.currentRoute.path;

      if (path === currentPath) {
        return true;
      }

      if (currentPath.includes(path) && path !== "/") {
        return true;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.navigation {
  min-height: 100vh;
  width: 90px;
  background: #000;
  text-align: center;
  position: fixed;
  top: 0;
  left: 0;
}

.logo {
  img {
    padding: 32px 0 22px 0;
    max-width: 50px;
  }
}

.items {
  padding-top: 20px;

  a {
    color: #fff;
  }
}

.item {
  padding: 31.5px 0;
  width: 100%;
  transition: 0.2s cubic-bezier(0.075, 0.82, 0.165, 1) background;

  i.material-icons {
    font-size: 2.3rem;
  }

  &:hover {
    cursor: pointer;
    background: lighten(#000, 5%);
  }

  &.active {
    &::after {
      content: "\A";
      width: 6px;
      height: 6px;
      border-radius: 100%;
      background: var(--blue);
      display: inline-block;
      position: relative;
      bottom: 14px;
      left: 8px;
    }

    i.material-icons {
      padding-left: 6px;
    }
  }
}
</style>
