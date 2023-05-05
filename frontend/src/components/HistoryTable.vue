<!-- src/components/HistoryTable.vue -->
<template>
  <v-main @click="deselectRow">
    <h1>History</h1>
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
     <v-data-table 
      :headers="headers"
      :items="filteredItems"
      item-key="name"
      class="history-table"
      @click:row="selectRow"
      @dblclick:row="analyze"
      hover="true"
      >
      <template v-slot:item="{item}">
          <tr
          :class="{ 'selected-row':  selectedRow !==null && item.columns.title === selectedRow.columns.title }" @click="selectRow(item); $event.stopPropagation()">
          <td >
              {{ item.columns.title }}</td>
              <td>{{ item.columns.artist }}</td>
            <td>{{ item.columns.updatedAt }}</td>
          </tr>
        </template>
    </v-data-table>

    <!-- Add item modal -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">Add Item</v-card-title>
        <v-card-text>
          <v-text-field 
                  label="YouTube URL" v-model="youtubeUrl"
                  :error-messages="errorMessage"
                  :loading="loading"
                  append-inner-icon="$magnify"
                  @click:append-inner="searchVideoInfo">
          </v-text-field>
          <v-text-field label="Title" v-model="title"></v-text-field>
          <v-text-field label="Artist" v-model="artist"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="saveItem">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-btn :disabled="analyzeDisabled" @click="analyze">Analyze</v-btn>
    </div>
    </v-main>
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
    artist: "",
    errorMessage: "",
    loading:false,
    selectedRow: null,
    analyzeDisabled: true,
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
      selectRow(row:any) {
        console.log(row)
        this.selectedRow = row;
        this.analyzeDisabled = false;
      },
      deselectRow() {
      this.selectedRow = null
    },
      analyze() {
    if (this.selectedRow) {
      this.$router.push({ name: "Analysis", params: { analysisId: this.selectedRow.analysis_id } });
        }
      },
      searchVideoInfo() {
        this.errorMessage = "";
        if (!this.youtubeUrl) {
          this.errorMessage = "Please input YouTube URL.";
          return;
        }

        // Set loading state to true
        this.loading = true;

        // Call API to get video information
        axios.get("http://localhost:8081/api/music/video_info/", {
          params: {
            url: this.youtubeUrl
          }
        }).then((response)=>{

        if (response.data) {
          this.title = response.data.title;
          this.artist = response.data.channel;
        } 
      }).catch((error) =>{
          // Handle error: Failed to get video information
          this.errorMessage = error.response?.data?.error || "An error occurred.";
        }).finally(()=>{
          this.loading = false;
        });
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

  .v-row{
    flex-wrap: nowrap;
  }

  tr{
    cursor: pointer;
  }
  tr.selected-row>td {
  background-color: rgba(0, 0, 0, 0.1) !important; /* 選択時の背景色 */
}

  </style>

  