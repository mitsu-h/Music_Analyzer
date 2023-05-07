<template>
  <div class="analysis">
    <app-header />
    <v-main>
      <h1>Analysis</h1>
      <v-container fluid>
        <v-tooltip top>
    <template v-slot:activator="{ on }">
      <v-progress-linear
        v-on="on"
        v-model="progress"
        :value="progress"
        @click="seek"
        height="20"
      ></v-progress-linear>
    </template>
    <span>{{ currentTime }} / {{ duration }}</span>
  </v-tooltip>
        <v-btn @click="togglePlay">再生/停止</v-btn>
      <v-row>
          <v-col v-for="(track, index) in trackLabels" :key="index" cols="12" sm="6" md="4">
            <v-slider
              v-model="gains[index]"
              :label="`${track}: ${gains[index]} dB`"
              step="0.1"
              min="-40"
              max="12"
              thumb-label="always"
              thumb-size="24"
            ></v-slider>
          </v-col>
      </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, computed } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import {fetchSeparatedAudioFiles, mixAudioBuffers, playAudioBuffer, audioBufferToBlob, createGainNodes} from "@/utils/audioHelper.ts"

export default defineComponent({
  name: "Analysis",
  components: {
    AppHeader,
  },
  setup() {
    const router = useRouter();
    const analysisData = ref(null);
    const audioElement = ref(null);
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const decodedAudioDataList = ref(null);
    const mixedAudioBuffer = ref(null);
    const playStartTime = ref(null);
    const sourceNode = ref(null);
    const gainNodes = ref([]);
    
    // トラックラベルとゲインのリアクティブ変数を定義
    const trackLabels = ["vocals", "drums", "bass", "other"];
    const gains = ref([0,0,0,0]);

    function startTimer() {
        if (playStartTime.value !== null) {
            const elapsedTime = audioContext.currentTime - playStartTime.value;
            const duration = gainNodes.value[0]?.source?.buffer?.duration;
            currentTime.value = formatTime(elapsedTime % duration);
          }else currentTime.value = formatTime(0);
          setTimeout(() => {
            startTimer();
          }, 1000);
      }
      

    function updateGains(newGains) {
      
    gainNodes.value.forEach((gainNode, index) => {
      console.log(newGains[index])
      gainNode.gainNode.gain.value = Math.pow(10, newGains[index] / 20);
      });
    }

    // ゲインが変更されたときに音源を再ミックスして再生する関数
    watch(gains, () => {
      // ゲインを適用して音源を再ミックス
      console.log("change gain!", gains.value);
        // ゲインノードの値を更新
        updateGains(gains.value);
    }, {deep: true})



    onMounted(async() => {
      analysisData.value = JSON.parse(router.currentRoute.value.query.analysisData);

      try {
        console.log(analysisData.value.raw.separated_audio_files)
        const separatedAudioDataList = await fetchSeparatedAudioFiles(analysisData.value.raw.separated_audio_files);
        console.log(separatedAudioDataList)
        // ArrayBufferをAudioBufferにデコード
        decodedAudioDataList.value = await Promise.all(
          Object.values(separatedAudioDataList).map((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer)
          )
        )
        gainNodes.value = createGainNodes(decodedAudioDataList.value, audioContext, gains.value);
        console.log(gainNodes.value)
        mixedAudioBuffer.value = mixAudioBuffers(decodedAudioDataList.value, audioContext, gainNodes.value);
        playAudioBuffer(audioContext, gainNodes.value);
        playStartTime.value = audioContext.currentTime
        startTimer()

        // audioElement.value.addEventListener("timeupdate", updateCurrentTime);
      } catch (error) {
        console.error("Error fetching audio:", error);
      }
    });

    const progress = ref(0);
    const currentTime = ref(0);

    const duration = computed(() => formatTime(mixedAudioBuffer.value?.duration || 0));

    watch(
      () => audioElement.value?.currentTime,
      (value) => {
        progress.value = (value / audioElement.value.duration) * 100;
      },
      { deep: true }
    );

    function seek(event) {
      const rect = event.target.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const seekTime = (x / rect.width) * audioElement.value.duration;
      audioElement.value.currentTime = seekTime;
      progress.value = (seekTime / audioElement.value.duration) * 100;
    }

    function formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }


    function togglePlay() {
      if (audioContext.state === "running") {
        audioContext.suspend();
      } else if (audioContext.state === "suspended") {
        audioContext.resume();
      }
    }

    return {
      analysisData,
      audioElement,
      mixedAudioBuffer,
      trackLabels,
      gains,
      progress,
      currentTime,
      duration,
      seek,
      togglePlay
    };
  },
});
</script>

<style scoped>
</style>
