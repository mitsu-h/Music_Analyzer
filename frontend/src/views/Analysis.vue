<template>
  <div class="analysis">
    <app-header />
    <v-main>
      <h1>Analysis</h1>
      <v-container fluid>
        <audio ref="audioElement" controls preload="auto" style="width: 100%;">
        Your browser does not support the audio element.
      </audio>
      </v-container>
    </v-main>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import {fetchSeparatedAudioFiles, mixAudioBuffers, playAudioBuffer, audioBufferToBlob} from "@/utils/audioHelper.ts"

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
    const mixedAudioBuffer = ref(null);
    async function playMixedAudioWithMediaStream(audioBuffer, audioElement) {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioContext.createBufferSource();
      source.buffer = audioBuffer;

      const destination = audioContext.createMediaStreamDestination();
      source.connect(destination);

      const mediaStream = destination.stream;
      audioElement.srcObject = mediaStream;

      source.start(0);
    }

    onMounted(async() => {
      analysisData.value = JSON.parse(router.currentRoute.value.query.analysisData);

      try {
        console.log(analysisData.value.raw.separated_audio_files)
        const separatedAudioDataList = await fetchSeparatedAudioFiles(analysisData.value.raw.separated_audio_files);
        console.log(separatedAudioDataList)
        // ArrayBufferをAudioBufferにデコード
        const decodedAudioDataList = await Promise.all(
          Object.values(separatedAudioDataList).map((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer)
          )
        )
        console.log(decodedAudioDataList)

      // 音源をミックス
      mixedAudioBuffer.value = await mixAudioBuffers(decodedAudioDataList, audioContext);

      // 音源を再生
      // playAudioBuffer(mixedAudioBuffer.value, audioContext);

      // mixedAudioBufferをBlobに変換し、オーディオ要素にセット
      const mixedBlob = audioBufferToBlob(mixedAudioBuffer.value)
      audioElement.value.src = URL.createObjectURL(mixedBlob);
      console.log(audioElement.value)
      audioElement.value.load();
      // audioElement.value.play();
      } catch (error) {
        console.error("Error fetching audio:", error);
      }
    });

    return {
      analysisData,
      audioElement,
      mixedAudioBuffer
    };
  },
});
</script>

<style scoped>
</style>
