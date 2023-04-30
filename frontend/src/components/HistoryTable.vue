<!-- src/components/HistoryTable.vue -->
<template>
    <div class="history-table">
      <v-toolbar flat color="white">
        <v-text-field
          v-model="search"
          append-icon="$mdimagnify"
          label="検索"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-btn icon @click="addItem">
          <v-icon :icon="mdiPlus"></v-icon>
        </v-btn>
      </v-toolbar>
     <v-data-table :headers="headers" :items="items" item-value="name" class="history-table" @click:row="">
    </v-data-table>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import {mdiPlus} from "@mdi/js";

  
  export default defineComponent({
    name: "HistoryTable",
    data() {
      return {
        mdiPlus,
        search: "",
        headers: [
        { title: "Title", key: "title" },
      { title: "Artist", key: "artist" },
      { title: "Last Edit", key: "updatedAt" },
        ],
        items: [
          { title: "Song 1", artist: "Artist 1", updatedAt: '2023-04-28' },
          { title: "Song 2", artist: "Artist 2", updatedAt: '2023-04-27' },
          { title: "Song 3", artist: "Artist 3", updatedAt: '2023-04-22' },
        ],
      }
    },
    methods: {
      addItem() {
        // 追加ボタンが押されたときの処理をここに書く
      },
    },
  })
  </script>
  
  <style scoped>
  /* ...existing styles... */
  .history-table{
    width: 80%;
    margin: 0 auto;
  }
  .v-toolbar{
    width: 80%;
    margin: 0 auto;
    padding: 1em;
  }
  tr.selected {
    background-color: rgba(0, 0, 255, 0.1);
  }
  </style>