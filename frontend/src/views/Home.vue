<template>
  <div class="home">
    <app-header />
    <history-table />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import HistoryTable from "@/components/HistoryTable.vue";

export default defineComponent({
  name: "Home",
  components: {
    AppHeader,
    HistoryTable
  },
});
</script>

<style scoped>
.home {
  /* text-align: center; */
}
</style>
