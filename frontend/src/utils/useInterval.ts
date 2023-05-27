// /src/utils/useInterval.ts

import { ref, watch } from 'vue'

export function useInterval(callback: Function, delay: number) {
  const savedCallback = ref<Function>()

  // コールバックを保存
  savedCallback.value = callback

  // 間隔を設定
  let intervalId = setInterval(() => {
    savedCallback.value()
  }, delay)

  // コールバックが変更された場合、間隔を再設定
  watch(savedCallback, () => {
    clearInterval(intervalId)
    intervalId = setInterval(() => {
      savedCallback.value()
    }, delay)
  })
}
