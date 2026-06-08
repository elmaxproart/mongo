<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'
import { Plus, Trash2, Tag, DollarSign, ShoppingBag, Eye, Percent, CheckCircle } from 'lucide-vue-next'

const auth = useAuthStore()
const myArtworks = ref([])
const categories = ref([])
const sales = ref([])
const showSuccessAlert = ref(false)

const newArt = ref({
  title: '',
  description: '',
  price: '',
  category: '',
  image_url: ''
})

const fetchMyArt = async () => {
  try {
    const res = await axios.get(`/artworks?author_id=${auth.user._id}`)
    myArtworks.value = res.data
  } catch(e) {
    console.error('Error fetching artworks', e)
  }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get('/categories')
    categories.value = res.data
  } catch(e) {}
}

const fetchSales = async () => {
  try {
    const res = await axios.get('/orders')
    sales.value = res.data
  } catch(e) {}
}

onMounted(() => {
  fetchMyArt()
  fetchCategories()
  fetchSales()
})

const publish = async () => {
  try {
    const payload = {
      ...newArt.value,
      price: parseFloat(newArt.value.price)
    }
    await axios.post('/artworks', payload)
    newArt.value = { title: '', description: '', price: '', category: '', image_url: '' }
    showSuccessAlert.value = true
    setTimeout(() => { showSuccessAlert.value = false }, 4000)
    fetchMyArt()
  } catch(e) {
    alert('Error publishing artwork')
  }
}

const remove = async (id) => {
  if (confirm('Are you sure you want to delete this artwork?')) {
    try {
      await axios.delete(`/artworks/${id}`)
      fetchMyArt()
      fetchSales() // Refresh sales just in case
    } catch(e) {
      alert('Error deleting artwork')
    }
  }
}

// Stats computations
const totalRevenue = computed(() => {
  return sales.value.reduce((sum, item) => sum + item.price, 0)
})

const activeListingsCount = computed(() => {
  return myArtworks.value.filter(art => !art.is_sold).length
})
</script>

<template>
  <div style="padding: 1rem 0 3rem;" class="animate-fade-in">
    <h1 style="font-size: 2.8rem; font-weight: 500; margin-bottom: 2rem;">Artist Studio Dashboard</h1>

    <!-- Stats Row -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
      <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem;">
        <div style="background: var(--accent-glow); color: var(--accent-color); padding: 0.85rem; border-radius: 50%;">
          <DollarSign size="24" />
        </div>
        <div>
          <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5;">Total Revenue</span>
          <h2 style="font-size: 1.8rem; font-weight: 600; margin-top: 0.15rem; font-family: 'Jost', sans-serif;">${{ totalRevenue.toLocaleString() }}</h2>
        </div>
      </div>

      <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem;">
        <div style="background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 0.85rem; border-radius: 50%;">
          <ShoppingBag size="24" />
        </div>
        <div>
          <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5;">Masterpieces Sold</span>
          <h2 style="font-size: 1.8rem; font-weight: 600; margin-top: 0.15rem; font-family: 'Jost', sans-serif;">{{ sales.length }}</h2>
        </div>
      </div>

      <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem;">
        <div style="background: rgba(59, 130, 246, 0.1); color: #3b82f6; padding: 0.85rem; border-radius: 50%;">
          <Eye size="24" />
        </div>
        <div>
          <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5;">Active Listings</span>
          <h2 style="font-size: 1.8rem; font-weight: 600; margin-top: 0.15rem; font-family: 'Jost', sans-serif;">{{ activeListingsCount }}</h2>
        </div>
      </div>
    </div>

    <!-- Main Section -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 3rem; align-items: start;">
      
      <!-- Left Column: Publish Form -->
      <div class="glass-panel" style="padding: 2.25rem; border-radius: var(--radius-md);">
        <h2 style="font-size: 1.6rem; font-weight: 500; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">Publish Masterpiece</h2>
        
        <div v-if="showSuccessAlert" class="glass-panel" style="padding: 1rem; border-color: #22c55e; background: rgba(34, 197, 94, 0.05); margin-bottom: 1.5rem; border-radius: var(--radius-sm); display: flex; gap: 0.75rem; align-items: center;">
          <CheckCircle size="18" style="color: #22c55e;" />
          <span style="font-size: 0.85rem; color: #22c55e;">Artwork published successfully!</span>
        </div>

        <form @submit.prevent="publish" style="display: flex; flex-direction: column; gap: 1.25rem;">
          <div style="display: flex; flex-direction: column; gap: 0.4rem;">
            <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">Title</label>
            <input v-model="newArt.title" placeholder="Masterpiece Title" class="input-control" required>
          </div>
          
          <div style="display: flex; flex-direction: column; gap: 0.4rem;">
            <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">Description</label>
            <textarea v-model="newArt.description" placeholder="Describe the creative intent, materials used, etc." rows="4" class="input-control" style="resize: vertical;"></textarea>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
              <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">Price ($)</label>
              <input v-model="newArt.price" type="number" step="0.01" min="1" placeholder="4500" class="input-control" required>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
              <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">Category</label>
              <select v-model="newArt.category" class="input-control" required style="cursor: pointer;">
                <option value="" disabled>Select Category</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.4rem;">
            <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">Image URL</label>
            <input v-model="newArt.image_url" placeholder="https://images.unsplash.com/..." class="input-control" required>
          </div>

          <button type="submit" class="btn btn-primary" style="justify-content: center; padding: 1rem; font-weight: 600; margin-top: 0.5rem;">
            <Plus size="16" /> Publish to Gallery
          </button>
        </form>
      </div>

      <!-- Right Column: Artwork & Sales List -->
      <div style="display: flex; flex-direction: column; gap: 2.5rem;">
        
        <!-- Artworks list -->
        <div>
          <h2 style="font-size: 1.6rem; font-weight: 500; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">My Artworks</h2>
          
          <div v-if="myArtworks.length > 0" style="display: flex; flex-direction: column; gap: 1rem;">
            <div v-for="art in myArtworks" :key="art._id" style="display: flex; align-items: center; gap: 1.5rem; padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); background: var(--card-bg); box-shadow: var(--shadow-sm); position: relative;">
              <img :src="art.image_url" style="width: 70px; height: 70px; object-fit: cover; border-radius: var(--radius-sm); border: 1px solid var(--border-color);">
              <div style="flex: 1;">
                <h4 style="font-weight: 600; font-size: 1.15rem;">{{ art.title }}</h4>
                <p style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.15rem;">
                  {{ art.category }} &bull; ${{ art.price.toLocaleString() }}
                </p>
              </div>
              
              <!-- Badges -->
              <div style="display: flex; align-items: center; gap: 1.5rem;">
                <span v-if="art.is_sold" class="badge-sold">Sold</span>
                <span v-else style="background: rgba(59, 130, 246, 0.1); color: #3b82f6; padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Active</span>
                
                <button @click="remove(art._id)" class="theme-toggle" style="border-color: #ef4444; color: #ef4444; padding: 0.5rem; border-radius: 4px;" title="Delete Artwork">
                  <Trash2 size="15" />
                </button>
              </div>
            </div>
          </div>
          <div v-else style="text-align: center; padding: 4rem 0; border: 1px dashed var(--border-color); border-radius: var(--radius-md); opacity: 0.65;">
            No published artworks in your portfolio yet.
          </div>
        </div>

        <!-- Sales History list -->
        <div>
          <h2 style="font-size: 1.6rem; font-weight: 500; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">Sales Transactions</h2>
          
          <div v-if="sales.length > 0" style="display: flex; flex-direction: column; gap: 1rem;">
            <div v-for="sale in sales" :key="sale._id" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); background: var(--card-bg);">
              <div>
                <h4 style="font-weight: 600; font-size: 1.05rem;">{{ sale.artwork_title }}</h4>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.15rem;">
                  Purchased by <span style="font-weight: 600; color: var(--text-color);">{{ sale.user_username }}</span> on {{ new Date(sale.created_at).toLocaleDateString() }}
                </p>
              </div>
              <span style="font-weight: 600; color: #22c55e; font-size: 1.1rem;">+${{ sale.price.toLocaleString() }}</span>
            </div>
          </div>
          <div v-else style="text-align: center; padding: 4rem 0; border: 1px dashed var(--border-color); border-radius: var(--radius-md); opacity: 0.65;">
            No sales recorded yet. Keep creating masterpieces!
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles */
</style>
