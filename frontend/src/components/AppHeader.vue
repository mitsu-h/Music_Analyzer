<!-- src/components/AppHeader.vue -->
<template>
  <v-app-bar app color="grey darken-2">
    <v-btn v-if="showBackButton" icon @click="router.go(-1)">
    <v-icon :icon="mdiArrowLeft"></v-icon>
  </v-btn>
    <v-spacer></v-spacer>
    <v-btn text color="white" @click="logout">Log out</v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {mdiArrowLeft} from "@mdi/js";

export default defineComponent({
  name: "AppHeader",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const logout = () => {
      authStore.logout();
      router.push({ name: "AuthSwitcher" });
    };

    const showBackButton = computed(() => {
      return router.currentRoute.value.name === "Analysis";
  });

    return {
      router,
      logout,
      showBackButton,
      mdiArrowLeft
    };
  },
});
</script>

<style scoped>
</style>
