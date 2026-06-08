<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../store/auth'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Tag, Calendar, User, ShoppingBag, CheckCircle, AlertTriangle } from 'lucide-vue-next'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const artwork = ref(null)
const isLoading = ref(true)
const purchaseLoading = ref(false)
const purchaseSuccess = ref(false)
const errorMessage = ref('')

const fetchArtworkDetails = async () => {
  try {
    const res = await axios.get(`/artworks/${route.params.id}`)
    artwork.value = res.data
  } catch(e) {
    errorMessage.value = 'Failed to load artwork details.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchArtworkDetails()
})

const buy = async () => {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }
  
  purchaseLoading.value = true
  errorMessage.value = ''
  
  try {
    await axios.post('/orders', {
      artwork_id: artwork.value._id || artwork.value.id
    })
    purchaseSuccess.value = true
    artwork.value.is_sold = true
  } catch(e) {
    errorMessage.value = e.response?.data?.detail || 'An error occurred during purchase.'
  } finally {
    purchaseLoading.value = false
  }
}
</script>

<template>
  <div style="padding: 1.5rem 0;">
    <!-- Back Button -->
    <button @click="router.push('/')" class="btn btn-secondary" style="border: none; padding: 0.5rem 0; margin-bottom: 2rem;">
      <ArrowLeft size="18" /> Back to Gallery
    </button>

    <!-- Loading State -->
    <div v-if="isLoading" style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 300px; gap: 1rem;">
      <div class="loader" style="border: 3px solid var(--border-color); border-top: 3px solid var(--accent-color); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite;"></div>
      <p style="font-size: 0.95rem; opacity: 0.6;">Loading masterpiece details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="errorMessage && !artwork" class="glass-panel" style="padding: 3rem; text-align: center; border-color: #ef4444; max-width: 600px; margin: 0 auto;">
      <AlertTriangle size="48" style="color: #ef4444; margin-bottom: 1.5rem;" />
      <h2 style="font-size: 1.5rem; font-family: 'Bodoni Moda', serif; font-weight: 500; margin-bottom: 0.5rem;">Error Occurred</h2>
      <p style="opacity: 0.7; margin-bottom: 1.5rem;">{{ errorMessage }}</p>
      <button @click="router.push('/')" class="btn btn-primary">Go Home</button>
    </div>

    <!-- Details Presentation -->
    <div v-else-if="artwork" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 4rem; align-items: start;" class="animate-slide-up">
      <!-- Left side: Large Frame Image -->
      <div style="border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-lg); background-color: var(--secondary-bg); border: 1px solid var(--border-color);">
        <img :src="artwork.image_url" :alt="artwork.title" style="width: 100%; display: block; max-height: 600px; object-fit: contain; margin: 0 auto;">
      </div>
      
      <!-- Right side: Museum Description -->
      <div style="padding: 0.5rem 0;">
        <span style="font-size: 0.85rem; font-weight: 600; color: var(--accent-color); text-transform: uppercase; letter-spacing: 0.1em; display: inline-flex; align-items: center; gap: 0.4rem;">
          <Tag size="14" /> {{ artwork.category }}
        </span>
        <h1 style="font-size: clamp(2.5rem, 5vw, 3.5rem); font-weight: 500; margin: 0.5rem 0 1.5rem; line-height: 1.1;">
          {{ artwork.title }}
        </h1>
        
        <div style="margin-bottom: 2.5rem;">
          <p style="font-size: 1.15rem; font-weight: 300; opacity: 0.85; line-height: 1.7; margin-bottom: 2.5rem; font-family: 'Jost', sans-serif;">
            {{ artwork.description }}
          </p>
          
          <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; flex-direction: column; gap: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 0.9rem; opacity: 0.6; display: inline-flex; align-items: center; gap: 0.5rem;">
                <User size="16" /> {{ t('artwork.author') }}
              </span>
              <span style="font-weight: 600; font-size: 0.95rem;">{{ artwork.author_name }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 1rem;">
              <span style="font-size: 0.9rem; opacity: 0.6; display: inline-flex; align-items: center; gap: 0.5rem;">
                <Calendar size="16" /> {{ t('artwork.date') }}
              </span>
              <span style="font-weight: 500; font-size: 0.95rem;">{{ new Date(artwork.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
            </div>
          </div>
        </div>

        <!-- Order Result Alerts -->
        <div v-if="purchaseSuccess" class="glass-panel" style="padding: 1.5rem; border-color: #22c55e; background: rgba(34, 197, 94, 0.05); border-radius: var(--radius-md); margin-bottom: 2rem; display: flex; gap: 1rem; align-items: center;">
          <CheckCircle size="28" style="color: #22c55e; flex-shrink: 0;" />
          <div>
            <h4 style="font-weight: 600; color: #22c55e; margin-bottom: 0.2rem;">Purchase Confirmed</h4>
            <p style="font-size: 0.85rem; opacity: 0.85;">Congratulations! You are now the official owner of this masterpiece. Details have been logged in your dashboard.</p>
          </div>
        </div>

        <div v-if="errorMessage && artwork" class="glass-panel" style="padding: 1.5rem; border-color: #ef4444; background: rgba(239, 68, 68, 0.05); border-radius: var(--radius-md); margin-bottom: 2rem; display: flex; gap: 1rem; align-items: center;">
          <AlertTriangle size="28" style="color: #ef4444; flex-shrink: 0;" />
          <p style="font-size: 0.85rem; opacity: 0.85; color: #ef4444;">{{ errorMessage }}</p>
        </div>

        <!-- Price & Purchase Action -->
        <div style="display: flex; align-items: center; gap: 2rem; flex-wrap: wrap;">
          <div style="display: flex; flex-direction: column;">
            <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5; margin-bottom: 0.25rem;">Price</span>
            <span style="font-size: 2.8rem; font-weight: 600; line-height: 1;">${{ artwork.price.toLocaleString() }}</span>
          </div>
          
          <button 
            v-if="!artwork.is_sold"
            @click="buy" 
            class="btn btn-primary" 
            :disabled="purchaseLoading"
            style="flex: 1; padding: 1.25rem 2rem; justify-content: center; border-radius: var(--radius-sm); font-size: 0.95rem; font-weight: 600;"
          >
            <span v-if="purchaseLoading" class="loader" style="border: 2px solid white; border-top: 2px solid transparent; border-radius: 50%; width: 18px; height: 18px; animation: spin 0.6s linear infinite; display: inline-block;"></span>
            <span v-else style="display: inline-flex; align-items: center; gap: 0.5rem;"><ShoppingBag size="18" /> {{ t('artwork.buy') }}</span>
          </button>
          <div 
            v-else 
            style="flex: 1; text-align: center; border: 1.5px solid #ef4444; color: #ef4444; background: rgba(239, 68, 68, 0.05); padding: 1rem; border-radius: var(--radius-sm); font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; font-size: 1.1rem;"
          >
            Sold Out / Vendu
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
