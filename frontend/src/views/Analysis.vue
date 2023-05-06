<template>
    <div class="analysis">
      <app-header />
      <v-main>
      <h1>Analysis</h1>
    </v-main>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import AppHeader from "@/components/AppHeader.vue";
  
  export default defineComponent({
    name: "Analysis",
    components: {
      AppHeader,
    },
  });
  </script>
  
  <style scoped>
  .home {
    text-align: center;
  }
  </style>
  