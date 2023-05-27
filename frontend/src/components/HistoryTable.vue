<!-- src/components/HistoryTable.vue -->
<template>
  <v-main @click="deselectRow">
    <h1>History</h1>
    <div class="history-table">
      <v-toolbar flat color="#4e4e4e">
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
      hover=true
      >
      <template v-slot:item="{item}">
          <tr
          :class="{ 'selected-row':  selectedRow !==null && item.columns.title === selectedRow.columns.title }" @click="selectRow(item); $event.stopPropagation()">
          <td >
              {{ item.columns.title }}</td>
              <td>{{ item.columns.artist }}</td>
            <td>{{ item.columns.updated_at }}</td>
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
                  append-inner-icon="$magnify"
                  @click:append-inner="searchVideoInfo">
          </v-text-field>
          <v-text-field label="Title" v-model="title"></v-text-field>
          <v-text-field label="Artist" v-model="artist"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text :loading="loading" @click="saveItem">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-btn class="right-btn" :disabled="analyzeDisabled" @click="analyze">Analyze</v-btn>
    </div>
    </v-main>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, onMounted, toRaw } from "vue";
  import axios from "axios";
  import {mdiPlus} from "@mdi/js";
import { useRouter } from "vue-router";

  

  export default defineComponent({
  name: "HistoryTable",
  setup() {
    const headers = ref([
      { title: "Title", key: "title" },
      { title: "Artist", key: "artist" },
      { title: "Last Edit", key: "updated_at" },
    ]);

    const search = ref("");
    async function fetchAnalysisResults() {
      const response = await fetch("http://localhost:8081/api/analysis_results/a043bae1-6038-03a8-39c0-cb52f511d9cb");
      const data = await response.json();
      return data;
    }
    const items = ref([]);
    onMounted(async () => {
    items.value = await fetchAnalysisResults();
    console.log(items.value)
    });

    const filteredItems = computed(() => {
      if(!items.value) return [];
      return items.value.filter((item) => {
        return (
          item.title.toLowerCase().includes(search.value.toLowerCase()) ||
          item.artist.toLowerCase().includes(search.value.toLowerCase())
        );
      });
    });

    const loading = ref(false);
    const selectedRow = ref(null);
    const analyzeDisabled = ref(true);

    const selectRow = (item: any) => {
      selectedRow.value = item;
      analyzeDisabled.value = false;
    };
    const deselectRow = () => {
      selectedRow.value = null;
      analyzeDisabled.value = true;
    };

    //新規追加の処理
    const dialog = ref(false);
    const addItem = () => {
        dialog.value = true;
      };
    const youtubeUrl = ref("");
    const title = ref("");
    const artist = ref("");
    const errorMessage = ref("");
    
    const router = useRouter();
    const analyze = () => {
      if (selectedRow.value) {
        router.push({ name: "Analysis", query: { analysisData: JSON.stringify(selectedRow.value) } });
      }
    };

    const searchVideoInfo = async () => {
      errorMessage.value = "";
      if (!youtubeUrl.value) {
        errorMessage.value = "Please input YouTube URL.";
        return;
      }

      loading.value = true;

      try {
        const response = await axios.get("http://localhost:8081/api/music/video_info/", {
          params: {
            url: youtubeUrl.value
          }
        });

        if (response.data) {
          title.value = response.data.title;
          artist.value = response.data.channel;
        }
      } catch (error) {
        errorMessage.value = error.response?.data?.error || "An error occurred.";
      } finally {
        loading.value = false;
      }
    };

    const saveItem = () => {
      if (!youtubeUrl.value) {
        errorMessage.value = "Please input YouTube URL.";
        return;
      }
      if (!title.value || !artist.value){
        errorMessage.value = "Please click search icon or input title and artist.";
      }
      loading.value = true;
      axios.get("http://localhost:8081/api/download_and_separate_audio/", {
        params: {
          // TODO: userIdを変数化、実際のユーザに置き換える
          user_id: "a043bae1-6038-03a8-39c0-cb52f511d9cb",
          url: youtubeUrl.value,
          title: title.value,
          artist: artist.value

        }
      }).then((response) =>{
        console.log("sccess put data");
        loading.value = false;
        // DynamoDBに書き込んだ楽曲でAnalysisページへと遷移
        // また、テーブルから選択したときとobjectが一致するようにrawを追加
        router.push({ name: "Analysis", query: { analysisData: JSON.stringify({raw: response.data}) } });
      }
      ).catch((error)=>errorMessage.value = error.response?.data?.error || "An error occurred.")
    }

    return {
      mdiPlus,
      headers,
      search,
      filteredItems,
      selectRow,
      youtubeUrl,
      title,
      artist,
      errorMessage,
      loading,
      selectedRow,
      deselectRow,
      analyzeDisabled,
      analyze,
      searchVideoInfo,
      dialog,
      addItem,
      saveItem
    };
  },
});
  </script>
  
  <style scoped>
  /* ...existing styles... */
  .v-toolbar{
    padding: 1em;
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

.right-btn{
  display: flex;
  margin: 0.5em 0 0.5em auto;
}

  </style>

  