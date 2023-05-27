import { defineStore } from 'pinia'

export const useMusicStore = defineStore({
  id: 'music',
  state: () => ({
    analysisData: null
  }),
  persist: true,
  actions: {
    setAnalysisData(data) {
      this.analysisData = data
    }
  }
})
