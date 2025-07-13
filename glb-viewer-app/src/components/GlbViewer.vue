<script setup>
import { onMounted, ref, watch, onBeforeUnmount } from 'vue'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import * as THREE from 'three'
import axios from 'axios'

const props = defineProps({
  sessionId: String
})

const canvasRef = ref(null)
const containerRef = ref(null)
const modelLoaded = ref(false)
const intervalRef = ref(null)

const autoRotate = ref(true)
const showLight = ref(true)
const showSky = ref(true)
const wireframeMode = ref(false)

let renderer, camera, scene, controls, model
let hemiLight, dirLight, ambientLight

const renderModel = (blobUrl) => {
  scene = new THREE.Scene()
  updateBackground()

  camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000)
  camera.position.set(0, 1, 3)

  renderer = new THREE.WebGLRenderer({
    canvas: canvasRef.value,
    antialias: true,
    alpha: true
  })

  updateRendererSize()

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.1
  controls.minDistance = 0.01
  controls.maxDistance = 1000
  controls.maxPolarAngle = Math.PI / 2
  controls.autoRotate = autoRotate.value
  controls.autoRotateSpeed = 2.0
  controls.zoomSpeed = 1.0
  controls.panSpeed = 1.0

  setupLight()

  const loader = new GLTFLoader()
  loader.load(
    blobUrl,
    gltf => {
      model = gltf.scene
      model.scale.set(1.5, 1.5, 1.5)
      // 預設輸出真實顏色
      renderer.outputEncoding = THREE.sRGBEncoding

      scene.add(model)
      modelLoaded.value = true
      animate()
      console.log('✅ 模型載入完成')
    },
    undefined,
    err => {
      console.error('❌ GLB 載入錯誤:', err)
    }
  )

  window.addEventListener('resize', updateRendererSize)
}

const updateRendererSize = () => {
  if (!renderer || !camera || !containerRef.value) return
  const width = containerRef.value.clientWidth
  const height = containerRef.value.clientHeight
  renderer.setSize(width, height)
  camera.aspect = width / height
  camera.updateProjectionMatrix()
}

const setupLight = () => {
  if (hemiLight) scene.remove(hemiLight)
  if (dirLight) scene.remove(dirLight)
  if (ambientLight) scene.remove(ambientLight)

  if (showLight.value) {
    hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1)
    scene.add(hemiLight)

    dirLight = new THREE.DirectionalLight(0xffffff, 1)
    dirLight.position.set(5, 10, 7.5)
    scene.add(dirLight)

    ambientLight = new THREE.AmbientLight(0xffffff, 0.3)
    scene.add(ambientLight)
  }
}

const updateBackground = () => {
  if (!scene) return
  scene.background = new THREE.Color(showSky.value ? '#87ceeb' : '#000000')
}

const applyWireframe = () => {
  if (!model) return
  model.traverse(child => {
    if (child.isMesh && child.material) {
      const mats = Array.isArray(child.material) ? child.material : [child.material]
      mats.forEach(m => {
        // 提升亮度與彩度
        if (m.color) m.color.multiplyScalar(1.5)     // 增強顏色強度
        if (m.emissive) m.emissive.multiplyScalar(0.5) // 提升材質的自發光
        m.metalness = 0.1
        m.roughness = 0.4
        m.needsUpdate = true
        m.wireframe = wireframeMode.value
        m.needsUpdate = true
        
      })
    }
  })
}

const pollModel = async () => {
  if (!props.sessionId || modelLoaded.value) return

  try {
    const res = await axios.get('http://localhost:8001/get_model', {
      params: { session_id: props.sessionId },
      responseType: 'blob'
    })

    if (res.status === 200 && !modelLoaded.value) {
      clearInterval(intervalRef.value)
      intervalRef.value = null
      const blobUrl = URL.createObjectURL(res.data)
      renderModel(blobUrl)
    }
  } catch (err) {
    console.log('⏳ 尚未找到模型，繼續輪詢...')
  }
}

const resetView = () => {
  if (camera && controls) {
    camera.position.set(0, 1, 3)
    controls.target.set(0, 0, 0)
    controls.update()
  }
}

const toggleAutoRotate = () => {
  autoRotate.value = !autoRotate.value
  if (controls) controls.autoRotate = autoRotate.value
}

const toggleLight = () => {
  showLight.value = !showLight.value
  setupLight()
}

const toggleSky = () => {
  showSky.value = !showSky.value
  updateBackground()
}

const toggleMaterial = () => {
  wireframeMode.value = !wireframeMode.value
  applyWireframe()
}

const animate = () => {
  requestAnimationFrame(animate)
  if (controls) controls.update()
  if (renderer && scene && camera) renderer.render(scene, camera)
}

watch(() => props.sessionId, newId => {
  if (newId && !intervalRef.value && !modelLoaded.value) {
    intervalRef.value = setInterval(pollModel, 2000)
  }
})

onMounted(() => {
  if (props.sessionId && !intervalRef.value && !modelLoaded.value) {
    intervalRef.value = setInterval(pollModel, 2000)
  }
})

onBeforeUnmount(() => {
  if (intervalRef.value) clearInterval(intervalRef.value)
  window.removeEventListener('resize', updateRendererSize)
})
</script>

<template>
  <div ref="containerRef" style="width:100%; height:500px; position:relative;">
    <canvas ref="canvasRef" style="width:100%; height:100%; border:1px solid #ccc;" />

    <p v-if="!modelLoaded" style="position:absolute; top:10px; left:10px;">模型載入中...</p>
    <p v-else style="position:absolute; top:10px; left:10px;">模型已成功載入!</p>

    <div style="position:absolute; top:10px; right:10px; display:flex; flex-wrap:wrap; gap:8px;">
      <button @click="resetView">重置視角</button>
      <button @click="toggleAutoRotate">{{ autoRotate ? '停止旋轉' : '自動旋轉' }}</button>
      <button @click="toggleLight">{{ showLight ? '關閉光源' : '開啟光源' }}</button>
      <button @click="toggleSky">{{ showSky ? '黑色背景' : '天空背景' }}</button>
      <button @click="toggleMaterial">{{ wireframeMode ? '標準材質' : '線框材質' }}</button>
    </div>
  </div>
</template>
