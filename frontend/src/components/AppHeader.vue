<!-- src/components/AppHeader.vue -->
<template>
    <header class="app-header">
      <nav>
        <button @click="logout" class="logout-button">Log out</button>
      </nav>
    </header>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "@/stores/auth";
  
  export default defineComponent({
    name: "AppHeader",
    setup() {
      const authStore = useAuthStore();
      const router = useRouter();
  
      const logout = () => {
        authStore.logout();
        router.push({name: "AuthSwitcher"})
      };
  
      return {
        logout,
      };
    },
  });
  </script>
  
  <style scoped>
  .app-header {
    display: flex;
    justify-content: flex-end;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .logout-button {
    font-size: 16px;
    color: #fff;
    background: transparent;
    border: none;
    cursor: pointer;
  }
  </style>
  