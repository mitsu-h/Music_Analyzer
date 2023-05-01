<!-- src/components/HistoryTable.vue -->
<template>
    <div class="history-table">
      <v-toolbar flat color="white">
        <v-text-field
          v-model="search"
          append-icon="$magnify"
          label="検索"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-btn icon @click="addItem">
          <v-icon :icon="mdiPlus"></v-icon>
        </v-btn>
      </v-toolbar>
     <v-data-table :headers="headers" :items="filteredItems" item-value="name" class="history-table" @click:row="">
    </v-data-table>

    <!-- Add item modal -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title class="headline">Add Item</v-card-title>
        <v-card-text>
          <v-text-field label="YouTube URL" v-model="youtubeUrl"></v-text-field>
          <v-text-field label="Title" v-model="title"></v-text-field>
          <v-text-field label="Artist" v-model="artist"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="searchVideoInfo">Search</v-btn>
          <v-btn color="blue darken-1" text @click="saveItem">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import axios from "axios";
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
        dialog: false,
    youtubeUrl: "",
    title: "",
    artist: ""
      }
    },
    computed: {
    filteredItems() {
      return this.items.filter((item) => {
        return (
          item.title.toLowerCase().includes(this.search.toLowerCase()) ||
          item.artist.toLowerCase().includes(this.search.toLowerCase())
        );
      });
    },
  },
    methods: {
      addItem() {
        this.dialog = true;
      },
      async searchVideoInfo() {
        if (!this.youtubeUrl) {
          // Handle error: YouTube URL is empty
          return;
        }

        // Call API to get video information
        const response = await axios.get("http://localhost:8081/api/music/video_info/", {
          params: {
            url: this.youtubeUrl
          }
        });

        if (response.data) {
          this.title = response.data.title;
          this.artist = response.data.channel;
        } else {
          // Handle error: Failed to get video information
          console.error("not found !")
        }
      },
  saveItem() {
    // Save item to the list
    this.dialog = false;
  }
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