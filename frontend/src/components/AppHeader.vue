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
    background: #4e4e4e;
  }
  
  .logout-button {
    font-size: 16px;
    color: #d9d9d9;
    background: transparent;
    border: none;
    cursor: pointer;
  }
  </style>
  