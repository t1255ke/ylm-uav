<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import GlbViewer from './components/GlbViewer.vue'

const sessionId = ref('')
const status = ref('')
const videoUploading = ref(false)
const inpainting = ref(false)
const previewUrl = ref('')
const fileInputRef = ref(null) // 👈 用來觸發檔案選擇

onMounted(() => {
  document.title = 'test'
})

const handleVideoUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  videoUploading.value = true
  status.value = '處理影片中...'

  const formData = new FormData()
  formData.append('video', file)

  try {
    const res = await axios.post('http://localhost:8001/detect/', formData)
    sessionId.value = res.data.session_id
    status.value = '物件偵測完成'
  } catch (err) {
    status.value = '上傳失敗'
    console.error(err)
  } finally {
    videoUploading.value = false
  }
}

const callInpaint = async () => {
  if (!sessionId.value) return
  inpainting.value = true
  status.value = '移除人車與建立模型中...'

  const formData = new FormData()
  formData.append('session_id', sessionId.value)

  try {
    const res = await axios.post('http://localhost:8001/inpaint/', formData, {
      responseType: 'blob',
    })

    previewUrl.value = URL.createObjectURL(res.data)
    status.value = '完成！'
  } catch (err) {
    status.value = '失敗...'
    console.error(err)
  } finally {
    inpainting.value = false
  }
}
</script>

<template>
  <!-- 🔝 固定頂部 -->
  <div style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #f8f8f8;
    padding: 12px 20px;
    border-bottom: 1px solid #ccc;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    z-index: 1000;
  ">
    <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px;">
      <h1 style="margin: 0; font-size: 20px; flex-grow: 1;">test</h1>

      <!-- 檔案上傳按鈕觸發 input -->
      <input
        type="file"
        accept="video/*"
        @change="handleVideoUpload"
        :disabled="videoUploading"
        ref="fileInputRef"
        style="display: none"
      />
      <button :disabled="videoUploading" @click="fileInputRef?.click()">選擇影片</button>

      <button v-if="sessionId && !inpainting" @click="callInpaint">
        移除人車與建立模型
      </button>
    </div>
  </div>

  <!-- 主內容 -->
  <div style="padding: 100px 20px 20px;">
    <p v-if="status">{{ status }}</p>

    <!-- <div v-if="previewUrl" style="margin-top: 20px">
      <h3>移除人車影像預覽：</h3>
      <img :src="previewUrl" alt="Inpainted Result" style="max-width: 600px" />
    </div> -->

    <div v-if="sessionId" style="margin-top: 30px">
      <h3>模型預覽：</h3>
      <GlbViewer :sessionId="sessionId" />
    </div>
  </div>
</template>
