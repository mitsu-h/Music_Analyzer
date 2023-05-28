<template>
  <div class="analysis">
    <app-header />
    <v-main>
      <v-overlay v-model="overlay" class="align-center justify-center">
        <v-progress-circular color="primary" indeterminate size="64"></v-progress-circular>
      </v-overlay>
      <h1>Analysis</h1>
      <v-container fluid>
        <!-- 選択範囲の表示・編集 -->
        <div>
          <h2>Loop Range {{ currentLoopRangeIndex }}</h2>
          <v-range-slider
            v-model="loopRanges[currentLoopRangeIndex]"
            step="0.1"
            min="0"
            :max="duration"
            class="loop-range"
          >
            <template v-slot:prepend>
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-chip v-bind="attrs" v-on="on">{{
                    formatTime(loopRanges[currentLoopRangeIndex][0])
                  }}</v-chip>
                </template>
                <span>Start</span>
              </v-tooltip>
            </template>
            <template v-slot:append>
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-chip v-bind="attrs" v-on="on">{{
                    formatTime(loopRanges[currentLoopRangeIndex][1])
                  }}</v-chip>
                </template>
                <span>End</span>
              </v-tooltip>
            </template>
          </v-range-slider>
        </div>

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
          thumb-size="24"
        ></v-slider>
        <!-- 操作系のボタン -->
        <div style="display: flex; align-items: center">
          <span>{{ currentTime }} / {{ durationTime }}</span>
          <v-btn @click="togglePlayback">
            {{ isPlaying ? 'Stop' : 'Play' }}
          </v-btn>
          <v-btn :color="isLooping ? 'primary' : ''" @click="isLooping = !isLooping">
            {{ isLooping ? 'Loop On' : 'Loop Off' }}
          </v-btn>
          <!-- 
            * TODO: 横幅いっぱいになってるので、ボタンと同じぐらいの幅にする
            * 表示項目をもっとわかりやすくする
          -->
          <v-select
            v-model="currentLoopRangeIndex"
            :items="[0, 1, 2]"
            label="Select Loop Range"
            :width="10"
          ></v-select>
        </div>
        <v-slider
          v-model="selectedSpeed"
          label="Playback Speed"
          step="0.05"
          min="0.5"
          max="2"
          thumb-label="always"
          thumb-size="24"
        ></v-slider>
        <h2>Volume Controls</h2>
        <v-row no-gutters class="mb-6">
          <v-col v-for="(track, index) in trackLabels" :key="index" cols="12" sm="4" md="3">
            <v-slider
              v-model="gains[index]"
              :label="`${track}: ${gains[index]} dB`"
              step="0.1"
              min="-40"
              max="12"
              thumb-label="always"
              direction="vertical"
              thumb-size="24"
            ></v-slider>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, computed, onBeforeUnmount } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import { useRouter } from 'vue-router'
import { useMusicStore } from '@/stores/musicInfo'
import axios from 'axios'
import {
  fetchSeparatedAudioFiles,
  playAudioBuffers,
  audioBufferToBlob,
  createGainNodes
} from '@/utils/audioHelper.ts'
import {useInterval} from '@/utils/useInterval.ts'

export default defineComponent({
  name: 'Analysis',
  components: {
    AppHeader
  },
  setup() {
    const router = useRouter()
    const musicStore = useMusicStore()
    const overlay = ref(true)
    const analysisData = ref(musicStore.analysisData.raw)
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

    const intervalId = ref(null)
    const timerId = ref(null)

    // トラックラベルとゲインのリアクティブ変数を定義
    const trackLabels = ['vocals', 'drums', 'bass', 'other']
    const gains = ref([0, 0, 0, 0])

    function startTimer() {
      //  console.log(audioContext.currentTime);
      playbackPosition.value = audioElements.value[0].currentTime
      currentTime.value = formatTime(audioElements.value[0].currentTime % duration.value)
      timerId.value = setTimeout(() => {
        startTimer()
      }, 100)
    }

    function updateGains(newGains) {
      gainNodes.value.forEach((gainNode, index) => {
        console.log(newGains[index])
        gainNode.gainNode.gain.value = Math.pow(10, newGains[index] / 20)
      })
      console.log(gainNodes)
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

    // 選択範囲のループ再生
    const loopRanges = ref([
      [0, duration.value / 3],
      [duration.value / 3, (duration.value / 3) * 2],
      [(duration.value / 3) * 2, duration.value]
    ])
    const currentLoopRangeIndex = ref(0)
    const isLooping = ref(false)

    const progress = ref(0)
    const currentTime = ref(0)

    const playbackPosition = ref(0)

    watch(
      playbackPosition,
      (newPlaybackPosition) => {
        if (!isLooping.value) return
        const currentLoopRange = loopRanges.value[currentLoopRangeIndex.value]
        if (
          newPlaybackPosition < currentLoopRange[0] ||
          newPlaybackPosition > currentLoopRange[1]
        ) {
          audioElements.value.forEach((audioElement) => {
            audioElement.currentTime = currentLoopRange[0]
          })
        }
      },
      { deep: true }
    )

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

    const isPlaying = ref(false)
    async function play() {
      if (audioContext.state === 'suspended') {
        await audioContext.resume()
      }
      audioElements.value.forEach((audioElement) => {
        audioElement.play()
      })
    }

    function stop() {
      audioElements.value.forEach((audioElement) => {
        audioElement.pause()
      })
    }

    const togglePlayback = () => {
      if (isPlaying.value) {
        stop()
      } else {
        play()
      }
      isPlaying.value = !isPlaying.value
    }

    const selectedSpeed = ref(1)
    // selectedSpeed が変更されたときに playbackRate を更新
    watch(selectedSpeed, (newSpeed) => {
      audioElements.value.forEach((audioElement) => (audioElement.playbackRate = newSpeed))
    })

    onMounted(async () => {
      // analysisData.value = JSON.parse(router.currentRoute.value.query.analysisData).raw

      // try {
        console.log(analysisData.value.separated_audio_files)
        const separatedAudioDataList = await fetchSeparatedAudioFiles(
          analysisData.value.separated_audio_files
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
        decodedAudioDataList.value.forEach(
          (audioBuffer, index) =>
            (audioURLs.value[index] = URL.createObjectURL(audioBufferToBlob(audioBuffer)))
        )
        playAudioBuffers(audioElements.value, audioContext, gainNodes.value)

        // DBの値をセット
        audioElements.value.forEach((audioElement) => {
          audioElement.currentTime = Number(analysisData.value.last_played_position)
      })
        duration.value = decodedAudioDataList.value[0].duration
        loopRanges.value = JSON.parse(analysisData.value.loop_intervals)
        currentLoopRangeIndex.value = Number(analysisData.value.loop_range_index)
        isLooping.value = analysisData.value.is_looping
        selectedSpeed.value = Number(analysisData.value.playback_speed)
        audioElements.value.forEach((audioElement) => (audioElement.playbackRate = selectedSpeed.value))
        gains.value = Object.values(JSON.parse(analysisData.value.instruments_volume))

        startTimer()
        overlay.value = false

        // 30秒ごとに実行する関数
        const saveIntervalInfo = async () => {
          try {
            const instruments_volume = trackLabels.reduce((acc, label, index) => {
            acc[label] = gains.value[index];
            return acc;
          }, {});
            await axios.post('http://localhost:8081/api/save_to_dynamodb/', {
              user_id: analysisData.value.user_id,
              analysis_id: analysisData.value.analysis_id,
              last_played_position: playbackPosition.value,
              loop_intervals: loopRanges.value,
              loop_range_index: currentLoopRangeIndex.value,
              is_looping: isLooping.value,
              playback_speed: selectedSpeed.value,
              instruments_volume: instruments_volume,
            })
          } catch (error) {
            console.error('Failed to save interval info:', error)
          }
        }

        // 30秒ごとにsaveIntervalInfoを実行
        intervalId.value = useInterval(saveIntervalInfo, 30000)
      // }
    })

    onBeforeUnmount(() => {
      clearTimeout(timerId.value)
      clearInterval(intervalId.value)
    })

    return {
      overlay,
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
      loopRanges,
      currentLoopRangeIndex,
      isLooping,
      togglePlayback,
      formatTime,
      controllPlayback,
      audioURLs,
      selectedSpeed,
      isPlaying
    }
  }
})
</script>

<style scoped>
/* TODO: rangeのsliderの玉のサイズ調整 */
.loop-range >>> .v-slider__thumb__surface {
  height: 24px;
  width: 10px;
}
</style>
