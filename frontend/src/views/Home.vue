<template>
  <div class="home">
    <app-header />
    <h1>Welcome to the Home Page!</h1>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppHeader from "@/components/AppHeader.vue";

export default defineComponent({
  name: "Home",
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
