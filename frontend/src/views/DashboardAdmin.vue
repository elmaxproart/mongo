<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Users, Settings, Tag, Plus, UserPlus, Grid, CheckCircle } from 'lucide-vue-next'

const users = ref([])
const categories = ref([])
const newCat = ref('')
const showSuccessAlert = ref(false)

const fetchUsers = async () => {
  try {
    const res = await axios.get('/admin/users')
    users.value = res.data
  } catch(e) {
    console.error('Error fetching users', e)
  }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get('/categories')
    categories.value = res.data
  } catch(e) {}
}

onMounted(() => {
  fetchUsers()
  fetchCategories()
})

const addCategory = async () => {
  if (!newCat.value) return
  try {
    await axios.post('/categories', { name: newCat.value })
    newCat.value = ''
    showSuccessAlert.value = true
    setTimeout(() => { showSuccessAlert.value = false }, 3000)
    fetchCategories()
  } catch(e) {
    alert('Error adding category')
  }
}

// Compute metrics
const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const artistCount = computed(() => users.value.filter(u => u.role === 'artist').length)
const clientCount = computed(() => users.value.filter(u => u.role === 'user').length)
</script>

<template>
  <div style="padding: 1rem 0 3rem;" class="animate-fade-in">
    <h1 style="font-size: 2.8rem; font-weight: 500; margin-bottom: 2rem;">Gallery Administration</h1>

    <!-- Stats summary row -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
      <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem;">
        <div style="background: var(--accent-glow); color: var(--accent-color); padding: 0.85rem; border-radius: 50%;">
          <Users size="24" />
        </div>
        <div>
          <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5;">Total Members</span>
          <h2 style="font-size: 1.8rem; font-weight: 600; margin-top: 0.15rem; font-family: 'Jost', sans-serif;">{{ users.length }}</h2>
        </div>
      </div>

      <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem;">
        <div style="background: rgba(168, 85, 247, 0.1); color: #a855f7; padding: 0.85rem; border-radius: 50%;">
          <Grid size="24" />
        </div>
        <div>
          <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5;">Categories</span>
          <h2 style="font-size: 1.8rem; font-weight: 600; margin-top: 0.15rem; font-family: 'Jost', sans-serif;">{{ categories.length }}</h2>
        </div>
      </div>
      
      <div class="glass-panel" style="padding: 1.5rem; border-radius: var(--radius-md); display: flex; flex-direction: column; justify-content: center; gap: 0.5rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
          <span style="opacity: 0.6;">Artists:</span>
          <span style="font-weight: 600;">{{ artistCount }}</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; border-top: 1px solid var(--border-color); padding-top: 0.4rem;">
          <span style="opacity: 0.6;">Admins:</span>
          <span style="font-weight: 600;">{{ adminCount }}</span>
        </div>
      </div>
    </div>

    <!-- Main grid layout -->
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 3rem; align-items: start; flex-wrap: wrap;">
      
      <!-- User Management Table -->
      <div>
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
          <Users size="22" style="opacity: 0.8;" />
          <h2 style="font-size: 1.6rem; font-weight: 500;">User Registry</h2>
        </div>
        
        <div class="glass-panel" style="overflow: hidden; border-radius: var(--radius-md);">
          <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem;">
            <thead>
              <tr style="background: var(--secondary-bg); border-bottom: 1px solid var(--border-color);">
                <th style="padding: 1.25rem 1.5rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.8rem; opacity: 0.7;">Username</th>
                <th style="padding: 1.25rem 1.5rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.8rem; opacity: 0.7;">Email</th>
                <th style="padding: 1.25rem 1.5rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.8rem; opacity: 0.7;">Role</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in users" :key="u._id" style="border-bottom: 1px solid var(--border-color); background: var(--card-bg); transition: background 0.2s;" hover-bg>
                <td style="padding: 1.25rem 1.5rem; font-weight: 500;">{{ u.username }}</td>
                <td style="padding: 1.25rem 1.5rem; opacity: 0.7;">{{ u.email }}</td>
                <td style="padding: 1.25rem 1.5rem;">
                  <span :style="{ 
                    padding: '0.3rem 0.75rem', 
                    borderRadius: '99px', 
                    fontSize: '0.7rem', 
                    fontWeight: '700', 
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                    background: u.role === 'admin' ? 'rgba(234, 179, 8, 0.15)' : (u.role === 'artist' ? 'rgba(59, 130, 246, 0.15)' : 'rgba(120, 113, 108, 0.15)'),
                    color: u.role === 'admin' ? 'var(--accent-color)' : (u.role === 'artist' ? '#3b82f6' : 'var(--text-muted)'),
                    border: u.role === 'admin' ? '1px solid var(--accent-color)' : (u.role === 'artist' ? '1px solid #3b82f6' : '1px solid var(--text-muted)')
                  }">{{ u.role }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Gallery Configuration Panel -->
      <div>
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
          <Settings size="22" style="opacity: 0.8;" />
          <h2 style="font-size: 1.6rem; font-weight: 500;">Gallery Options</h2>
        </div>
        
        <div class="glass-panel" style="padding: 2rem; border-radius: var(--radius-md);">
          <h3 style="font-size: 1.25rem; font-weight: 500; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            <Tag size="18" /> Manage Categories
          </h3>
          
          <div v-if="showSuccessAlert" class="glass-panel" style="padding: 0.85rem; border-color: #22c55e; background: rgba(34, 197, 94, 0.05); margin-bottom: 1rem; border-radius: var(--radius-sm); display: flex; gap: 0.5rem; align-items: center;">
            <CheckCircle size="16" style="color: #22c55e;" />
            <span style="font-size: 0.8rem; color: #22c55e;">Category added!</span>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.85rem; margin-bottom: 2rem;">
            <input 
              v-model="newCat" 
              placeholder="e.g. Neo-Expressionism" 
              class="input-control"
              @keyup.enter="addCategory"
            >
            <button @click="addCategory" class="btn btn-primary" style="justify-content: center; width: 100%;">
              <Plus size="16" /> Add Category
            </button>
          </div>

          <!-- Existing Categories Capsules -->
          <p style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.6; margin-bottom: 0.75rem;">Active Categories</p>
          <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            <span 
              v-for="cat in categories" 
              :key="cat" 
              style="padding: 0.45rem 1rem; background: var(--secondary-bg); border-radius: var(--radius-sm); font-size: 0.8rem; font-weight: 500; border: 1px solid var(--border-color); text-transform: capitalize;"
            >
              {{ cat }}
            </span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Scoped table row hover helper */
tbody tr:hover {
  background-color: var(--secondary-bg) !important;
}
</style>
