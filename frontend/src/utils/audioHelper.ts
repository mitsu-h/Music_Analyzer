import axios from 'axios'

// 音源を取得する非同期関数
async function fetchAudioFile(audio_file_path: string) {
  const response = await axios.get('http://localhost:8081/api/get_audio_file/', {
    params: {
      audio_file_path: audio_file_path
    }
  })
  const base64Data = response.data.audio_file_data
  const binaryData = atob(base64Data)
  const len = binaryData.length
  const bytes = new Uint8Array(len)
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryData.charCodeAt(i)
  }
  return bytes.buffer
}

// Promise.allを使用して音源を並行して取得
export async function fetchSeparatedAudioFiles(separated_audio_files: string) {
  const audioFiles = JSON.parse(separated_audio_files)
  const promises = Object.values(audioFiles).map(fetchAudioFile)
  const arrayBuffers = await Promise.all(promises)
  return Object.keys(audioFiles).reduce((result, key, i) => {
    result[key] = arrayBuffers[i]
    return result
  }, {})
}

// 音源データをミックスする関数
export function mixAudioBuffers(
  audioDataList: AudioBuffer[],
  audioContext: AudioContext,
  gainNodes: GainNode[]
) {
  const numChannels = 2 // ステレオ
  const mixedBuffer = audioContext.createBuffer(
    numChannels,
    audioDataList[0].length,
    audioContext.sampleRate
  )

  for (let channel = 0; channel < numChannels; channel++) {
    const mixedBufferData = mixedBuffer.getChannelData(channel)

    for (let i = 0; i < audioDataList.length; i++) {
      const audioData = audioDataList[i]
      const channelData = audioData.getChannelData(channel)
      const gainNode = gainNodes[i]

      for (let j = 0; j < channelData.length; j++) {
        mixedBufferData[j] += channelData[j] * gainNode.gainNode.gain.value
      }
    }
  }

  return mixedBuffer
}

export function createGainNodes(audioDataList, audioContext, gains) {
  const gainNodes = audioDataList.map((audioData, index) => {
    const gainNode = audioContext.createGain()
    const source = audioContext.createBufferSource()
    source.buffer = audioData
    const gain = Math.pow(10, gains[index] / 20)
    gainNode.gain.value = gain
    source.connect(gainNode)
    gainNode.connect(audioContext.destination)
    return { source, gainNode }
  })
  return gainNodes
}

function writeWavHeader(
  buffer: ArrayBuffer,
  sampleRate: number,
  numChannels: number,
  dataSize: number
) {
  /**
   * wavのヘッダー情報を付与
   */
  const view = new DataView(buffer)

  // RIFF chunk descriptor
  view.setUint32(0, 0x52494646, false) // "RIFF"
  view.setUint32(4, 36 + dataSize, true)
  view.setUint32(8, 0x57415645, false) // "WAVE"

  // fmt sub-chunk
  view.setUint32(12, 0x666d7420, false) // "fmt "
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true) // PCM format
  view.setUint16(22, numChannels, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * numChannels * 2, true)
  view.setUint16(32, numChannels * 2, true)
  view.setUint16(34, 16, true)

  // data sub-chunk
  view.setUint32(36, 0x64617461, false) // "data"
  view.setUint32(40, dataSize, true)
}

export function audioBufferToBlob(audioBuffer: AudioBuffer) {
  const numberOfChannels = audioBuffer.numberOfChannels
  const length = audioBuffer.length * numberOfChannels * 2
  const dataSize = length
  const buffer = new ArrayBuffer(44 + dataSize)
  const data = new DataView(buffer)

  writeWavHeader(buffer, audioBuffer.sampleRate, numberOfChannels, dataSize)

  for (let channel = 0; channel < numberOfChannels; channel++) {
    const channelData = audioBuffer.getChannelData(channel)
    let offset = 44 + channel * 2

    for (let i = 0; i < channelData.length; i++) {
      const value = channelData[i] * 0x7fff // convert to 16-bit value
      data.setInt16(offset, value, true)
      offset += numberOfChannels * 2
    }
  }

  return new Blob([data], { type: 'audio/wav' })
}

// 音源データを再生する関数
export function playAudioBuffers(
  audioElements: HTMLMediaElement[],
  audioContext: AudioContext,
  gainNodes: GainNode[]
) {
  gainNodes.forEach((gainNode: GainNode, index) => {
    const mediaElementSource = audioContext.createMediaElementSource(audioElements[index])
    mediaElementSource.connect(gainNode.gainNode)
    gainNode.gainNode.connect(audioContext.destination)
    audioElements[index].loop = true
    //   audioElements[index].play();
  })
}
