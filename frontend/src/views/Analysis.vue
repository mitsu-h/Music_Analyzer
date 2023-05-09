<template>
  <div class="analysis">
    <app-header />
    <v-main>
      <h1>Analysis</h1>
      <v-container fluid>
        <audio
          v-for="(track, index) in trackLabels"
          :key="index"
          :ref="audioElementsRef"
          :src="audioURLs[index]"
          preload="auto"
        ></audio>
        <v-slider
          v-bind:model-value="playbackPosition"
          @click="controllPlayback"
          @input="controllPlayback"
          label="Playback Position"
          step="0.1"
          min="0"
          :max="duration"
          thumb-label="always"
          thumb-size="24"
        ></v-slider>
        <span>{{ currentTime }} / {{ durationTime }}</span>
        <v-btn @click="play">Play</v-btn>
        <v-btn @click="stop">Stop</v-btn>
        <v-slider
          v-model="selectedSpeed"
          label="Playback Speed"
          step="0.05"
          min="0.5"
          max="2"
          thumb-label="always"
          thumb-size="24"
        ></v-slider>
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
import { defineComponent, onMounted, ref, watch, computed } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  fetchSeparatedAudioFiles,
  playAudioBuffers,
  audioBufferToBlob,
  createGainNodes
} from '@/utils/audioHelper.ts'

export default defineComponent({
  name: 'Analysis',
  components: {
    AppHeader
  },
  setup() {
    const router = useRouter()
    const analysisData = ref(null)
    const audioURLs = ref([])
    const audioElements = ref([])
    const audioElementsRef = (el) => {
      if (el) {
        audioElements.value.push(el)
      }
    }
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    const decodedAudioDataList = ref(null)
    const mixedAudioBuffer = ref(null)
    const duration = ref(null)
    const durationTime = computed(() => formatTime(duration.value || 0))
    const gainNodes = ref([])

    // トラックラベルとゲインのリアクティブ変数を定義
    const trackLabels = ['vocals', 'drums', 'bass', 'other']
    const gains = ref([0, 0, 0, 0])

    function startTimer() {
      //  console.log(audioContext.currentTime);
      playbackPosition.value = (audioElements.value[0].currentTime / duration.value) * 100
      currentTime.value = formatTime(audioElements.value[0].currentTime % duration.value)
      setTimeout(() => {
        startTimer()
      }, 100)
    }

    function updateGains(newGains) {
      gainNodes.value.forEach((gainNode, index) => {
        console.log(newGains[index])
        gainNode.gainNode.gain.value = Math.pow(10, newGains[index] / 20)
      })
    }

    // ゲインが変更されたときに音源を再ミックスして再生する関数
    watch(
      gains,
      () => {
        // ゲインを適用して音源を再ミックス
        console.log('change gain!', gains.value)
        // ゲインノードの値を更新
        updateGains(gains.value)
      },
      { deep: true }
    )

    onMounted(async () => {
      analysisData.value = JSON.parse(router.currentRoute.value.query.analysisData)

      try {
        console.log(analysisData.value.raw.separated_audio_files)
        const separatedAudioDataList = await fetchSeparatedAudioFiles(
          analysisData.value.raw.separated_audio_files
        )
        console.log(separatedAudioDataList)
        // ArrayBufferをAudioBufferにデコード
        decodedAudioDataList.value = await Promise.all(
          Object.values(separatedAudioDataList).map((arrayBuffer) =>
            audioContext.decodeAudioData(arrayBuffer)
          )
        )
        gainNodes.value = createGainNodes(decodedAudioDataList.value, audioContext, gains.value)
        console.log(gainNodes.value)
        duration.value = decodedAudioDataList.value[0].duration
        decodedAudioDataList.value.forEach(
          (audioBuffer, index) =>
            (audioURLs.value[index] = URL.createObjectURL(audioBufferToBlob(audioBuffer)))
        )
        await playAudioBuffers(audioElements.value, audioContext, gainNodes.value)
        startTimer()
      } catch (error) {
        console.error('Error fetching audio:', error)
      }
    })

    const progress = ref(0)
    const currentTime = ref(0)

    const playbackPosition = ref(0)

    function controllPlayback(event) {
      // クリック位置を0～1の範囲に正規化
      const clickPosition = event.offsetX / event.target.clientWidth

      // 再生位置を計算
      const newPlaybackPosition = clickPosition * duration.value

      audioElements.value.forEach((audioElement) => {
        audioElement.currentTime = newPlaybackPosition
      })
    }

    function formatTime(time) {
      const minutes = Math.floor(time / 60)
      const seconds = Math.floor(time % 60)
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    }

    function play() {
      audioElements.value.forEach((audioElement) => {
        audioElement.play()
      })
    }

    function stop() {
      audioElements.value.forEach((audioElement) => {
        audioElement.pause()
      })
    }

    const speedOptions = [
      0.5, 0.75, 1.0, 1.25, 1.5, 2.0
      // { text: "0.5x", value: 0.5 },
      // { text: "1x", value: 1 },
      // { text: "1.5x", value: 1.5 },
      // { text: "2x", value: 2 },
    ]
    const selectedSpeed = ref(1)
    // selectedSpeed が変更されたときに playbackRate を更新
    watch(selectedSpeed, (newSpeed) => {
      audioElements.value.forEach((audioElement) => (audioElement.playbackRate = newSpeed))
    })

    return {
      analysisData,
      audioElements,
      audioElementsRef,
      mixedAudioBuffer,
      trackLabels,
      gains,
      playbackPosition,
      progress,
      currentTime,
      duration,
      durationTime,
      play,
      stop,
      formatTime,
      controllPlayback,
      audioURLs,
      speedOptions,
      selectedSpeed
    }
  }
})
</script>

<style scoped>
</style>
