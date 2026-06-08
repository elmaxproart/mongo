<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { Search, ArrowUpDown, Tag, Sparkles, ArrowRight } from 'lucide-vue-next'

const { t } = useI18n()
const artworks = ref([])
const categories = ref([])
const activeCategory = ref('')
const searchQuery = ref('')
const sortBy = ref('date_desc')

const currentSlideIndex = ref(0)
let slideInterval = null

const fetchArtworks = async () => {
  let url = '/artworks?'
  const params = []
  if (activeCategory.value) params.push(`category=${encodeURIComponent(activeCategory.value)}`)
  if (searchQuery.value) params.push(`search=${encodeURIComponent(searchQuery.value)}`)
  if (sortBy.value) params.push(`sort_by=${encodeURIComponent(sortBy.value)}`)
  url += params.join('&')
  
  try {
    const res = await axios.get(url)
    artworks.value = res.data
  } catch (e) {
    console.error(e)
  }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get('/categories')
    categories.value = res.data
  } catch(e) {}
}

onMounted(() => {
  fetchArtworks()
  fetchCategories()
  
  slideInterval = setInterval(() => {
    if (artworks.value.length > 0) {
      currentSlideIndex.value = (currentSlideIndex.value + 1) % artworks.value.length
    }
  }, 4000)
})

onUnmounted(() => {
  if (slideInterval) clearInterval(slideInterval)
})

const setCategory = (cat) => {
  activeCategory.value = cat
  fetchArtworks()
}

const scrollToFilters = () => {
  const element = document.getElementById('filter-section')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

// Watchers for search and sort changes
watch([searchQuery, sortBy], () => {
  fetchArtworks()
})
</script>

<template>
  <!-- Animated Ambient Background Blobs -->
  <div class="ambient-glow glow-1"></div>
  <div class="ambient-glow glow-2"></div>
  <div class="ambient-glow glow-3"></div>

  <!-- Hero Banner Section -->
  <div class="hero-banner animate-fade-in" style="padding: 4rem 0 5rem; position: relative; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 4rem; align-items: center; border-bottom: 1px solid var(--border-color); margin-bottom: 4rem;">
    <!-- Left Column: Branding Editorial -->
    <div style="text-align: left;">
      <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: var(--accent-glow); border: 1px solid var(--accent-color); padding: 0.4rem 1.1rem; border-radius: 99px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-color); margin-bottom: 2rem;">
        <Sparkles size="12" /> The New Age of Digital Art Collection
      </div>
      <h1 style="font-size: clamp(3.2rem, 6vw, 4.8rem); font-weight: 600; line-height: 1.05; margin-bottom: 2rem; font-family: 'Bodoni Moda', serif;">
        Collect & Curate <br/>Chefs-d’œuvre.
      </h1>
      <p style="font-size: 1.25rem; font-weight: 300; opacity: 0.75; letter-spacing: 0.02em; font-family: 'Jost', sans-serif; line-height: 1.6; max-width: 600px; margin-bottom: 3rem;">
        Discover an elite catalog of paintings, sculptures, and digital works. Experience fine art transactions powered by professional curators.
      </p>
      
      <!-- Call-To-Action buttons -->
      <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
        <button @click="scrollToFilters" class="btn btn-primary" style="padding: 1rem 2rem; font-weight: 600;">
          Explore Gallery <ArrowRight size="16" />
        </button>
        <router-link to="/login" class="btn btn-secondary" style="padding: 1rem 2rem; font-weight: 600;">
          Artist Studio Portal
        </router-link>
      </div>
    </div>

    <!-- Right Column: Immersive Floating Slide Frame -->
    <div class="animate-slide-up" style="animation-delay: 0.2s; justify-self: center; width: 100%; max-width: 380px;">
      <div class="glass-panel" style="padding: 1rem; border-radius: var(--radius-md); border-color: var(--accent-color); box-shadow: 0 20px 48px rgba(0,0,0,0.3), 0 0 24px var(--accent-glow); position: relative; overflow: hidden; height: 460px;">
        <transition name="slide-fade" mode="out-in">
          <div v-if="artworks.length > 0" :key="currentSlideIndex" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="height: 320px; overflow: hidden; border-radius: var(--radius-sm); border: 1px solid var(--border-color); background: #000;">
              <img 
                :src="artworks[currentSlideIndex]?.image_url" 
                :alt="artworks[currentSlideIndex]?.title"
                style="width: 100%; height: 100%; object-fit: cover; opacity: 0.9;"
              />
            </div>
            
            <div style="padding: 0.75rem 0.25rem 0.25rem;">
              <span style="font-size: 0.7rem; font-weight: 700; color: var(--accent-color); text-transform: uppercase; letter-spacing: 0.05em;">
                {{ artworks[currentSlideIndex]?.category }}
              </span>
              <h3 style="font-size: 1.35rem; font-family: 'Bodoni Moda', serif; font-weight: 500; margin-top: 0.15rem; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">
                {{ artworks[currentSlideIndex]?.title }}
              </h3>
              <p style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">
                By {{ artworks[currentSlideIndex]?.author_name }}
              </p>
            </div>
          </div>
          
          <div v-else style="height: 100%; display: flex; align-items: center; justify-content: center; color: var(--text-muted);">
            No previews available.
          </div>
        </transition>
      </div>
    </div>
  </div>

  <!-- Search & Sorting Filters Panel -->
  <div id="filter-section" class="glass-panel animate-slide-up" style="padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 2rem; display: flex; flex-direction: column; gap: 1.5rem; animation-delay: 0.3s;">
    <!-- Top Row: Search & Sort -->
    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center;">
      <!-- Search Input Container -->
      <div style="position: relative; flex: 1; min-width: 280px;">
        <Search style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); opacity: 0.4;" size="18" />
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search by title, description, artist..." 
          class="input-control" 
          style="padding-left: 2.8rem;"
        >
      </div>

      <!-- Sorting Selector -->
      <div style="position: relative; width: 220px; display: flex; align-items: center; gap: 0.5rem;">
        <ArrowUpDown size="16" style="opacity: 0.5;" />
        <select v-model="sortBy" class="input-control" style="cursor: pointer; padding-right: 2rem;">
          <option value="date_desc">Newest Artwork</option>
          <option value="price_asc">Price: Low to High</option>
          <option value="price_desc">Price: High to Low</option>
        </select>
      </div>
    </div>

    <!-- Bottom Row: Category Tabs -->
    <div style="display: flex; gap: 0.75rem; overflow-x: auto; padding-bottom: 0.5rem; border-top: 1px solid var(--border-color); padding-top: 1rem; scrollbar-width: none;">
      <button 
        @click="setCategory('')" 
        class="btn" 
        :class="activeCategory === '' ? 'btn-primary' : 'btn-secondary'"
        style="padding: 0.5rem 1.2rem; border-radius: 99px; font-size: 0.8rem;"
      >
        All Works
      </button>
      <button 
        v-for="cat in categories" 
        :key="cat" 
        @click="setCategory(cat)" 
        class="btn" 
        :class="activeCategory === cat ? 'btn-primary' : 'btn-secondary'"
        style="padding: 0.5rem 1.2rem; border-radius: 99px; font-size: 0.8rem;"
      >
        {{ cat }}
      </button>
    </div>
  </div>

  <!-- Artwork Showcase Grid -->
  <div v-if="artworks.length > 0" class="artwork-grid">
    <div 
      v-for="(art, index) in artworks" 
      :key="art._id" 
      class="card"
      :style="{ animationDelay: `${index * 0.1}s` }"
    >
      <div class="card-img-wrapper">
        <router-link :to="`/artwork/${art._id}`">
          <img :src="art.image_url" :alt="art.title" class="card-img">
        </router-link>
        
        <!-- Sold status badge overlay -->
        <div v-if="art.is_sold" style="position: absolute; top: 1.25rem; right: 1.25rem; z-index: 10;">
          <span class="badge-sold">Sold</span>
        </div>
        
        <!-- Category tag overlay -->
        <div style="position: absolute; bottom: 1.25rem; left: 1.25rem; z-index: 10;">
          <span style="background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(4px); color: white; padding: 0.25rem 0.65rem; border-radius: var(--radius-sm); font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; display: inline-flex; align-items: center; gap: 0.35rem;">
            <Tag size="10" /> {{ art.category }}
          </span>
        </div>

        <div class="card-overlay">
          <div class="overlay-text">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.8; margin-bottom: 0.25rem;">Artist Profile</p>
            <p style="font-family: 'Bodoni Moda', serif; font-size: 1.2rem; font-weight: 500;">{{ art.author_name }}</p>
          </div>
        </div>
      </div>

      <div class="card-content">
        <div>
          <h3 class="card-title">{{ art.title }}</h3>
          <p class="card-author">{{ t('artwork.author') }} {{ art.author_name }}</p>
        </div>
        
        <div class="card-footer">
          <span class="price">${{ art.price.toLocaleString() }}</span>
          <router-link 
            :to="`/artwork/${art._id}`" 
            class="btn" 
            :class="art.is_sold ? 'btn-secondary' : 'btn-primary'"
            style="padding: 0.45rem 1.1rem; font-size: 0.75rem;"
          >
            {{ art.is_sold ? 'View Details' : t('artwork.buy') }}
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <!-- Empty state -->
  <div v-else style="text-align: center; padding: 6rem 0; border: 1px dashed var(--border-color); border-radius: var(--radius-lg); margin-top: 2rem;">
    <p style="font-size: 1.5rem; font-family: 'Bodoni Moda', serif; font-weight: 500; margin-bottom: 0.5rem; opacity: 0.75;">No Artworks Found</p>
    <p style="font-size: 0.95rem; opacity: 0.5;">Try selecting a different category or refining your search term.</p>
  </div>

  <!-- About Gallery Philosophy -->
  <div class="animate-slide-up" style="margin-top: 6rem; border-top: 1px solid var(--border-color); padding-top: 5rem; animation-delay: 0.4s;">
    <div style="text-align: center; margin-bottom: 3.5rem;">
      <span style="font-size: 0.8rem; font-weight: 600; color: var(--accent-color); text-transform: uppercase; letter-spacing: 0.1em; display: inline-flex; align-items: center; gap: 0.4rem; justify-content: center;">
        <Sparkles size="12" /> The Gallery Philosophy
      </span>
      <h2 style="font-size: 2.2rem; font-weight: 500; font-family: 'Bodoni Moda', serif; margin-top: 0.5rem;">Dealers in Fine Art & Authenticity</h2>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2.5rem;">
      <div class="glass-panel" style="padding: 2rem; border-radius: var(--radius-md); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <h3 style="font-family: 'Bodoni Moda', serif; font-size: 1.4rem; font-weight: 500; margin-bottom: 0.75rem; color: var(--text-color);">Direct Relations</h3>
        <p style="font-size: 0.9rem; opacity: 0.8; line-height: 1.6;">
          Connecting collectors directly with modern digital creators. Our peer-to-peer structure eliminates high-street gallery markups.
        </p>
      </div>

      <div class="glass-panel" style="padding: 2rem; border-radius: var(--radius-md); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <h3 style="font-family: 'Bodoni Moda', serif; font-size: 1.4rem; font-weight: 500; margin-bottom: 0.75rem; color: var(--text-color);">Curator Verified</h3>
        <p style="font-size: 0.9rem; opacity: 0.8; line-height: 1.6;">
          Every canvas, print, digital token, and physical sculpture undergoes strict certification processes to ensure official copyrights.
        </p>
      </div>

      <div class="glass-panel" style="padding: 2rem; border-radius: var(--radius-md); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <h3 style="font-family: 'Bodoni Moda', serif; font-size: 1.4rem; font-weight: 500; margin-bottom: 0.75rem; color: var(--text-color);">Copyright Contracts</h3>
        <p style="font-size: 0.9rem; opacity: 0.8; line-height: 1.6;">
          Purchases generate an official deed of transfer and high-resolution raw master files, securing absolute provenance details.
        </p>
      </div>
    </div>
  </div>

  <!-- Featured Artist Spotlight Section -->
  <div class="glass-panel animate-slide-up" style="margin-top: 6rem; padding: 3.5rem; border-radius: var(--radius-lg); display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; background: var(--secondary-bg); animation-delay: 0.5s; margin-bottom: 4rem;">
    <div>
      <span style="font-size: 0.8rem; font-weight: 600; color: var(--accent-color); text-transform: uppercase; letter-spacing: 0.1em;">Artist Spotlight</span>
      <h2 style="font-size: 2.5rem; font-weight: 500; font-family: 'Bodoni Moda', serif; margin: 0.5rem 0 1.5rem; line-height: 1.1;">Vincent Van Gogh</h2>
      <p style="font-size: 1.25rem; font-style: italic; font-family: 'Bodoni Moda', serif; font-weight: 400; opacity: 0.9; line-height: 1.6; margin-bottom: 2rem; position: relative;">
        "Je rêve ma peinture et je peins mon rêve." <br/>
        <span style="font-size: 0.95rem; font-style: normal; font-family: 'Jost', sans-serif; opacity: 0.6; display: block; margin-top: 0.5rem;">— Arles, 1888</span>
      </p>
      <p style="font-size: 0.95rem; opacity: 0.8; line-height: 1.6; margin-bottom: 2rem;">
        Vincent is one of E-Gallery's featured partners. Specializing in digital painting conversions and impressionist styles, his virtual collection spans 24 certified master canvases.
      </p>
      <button @click="searchQuery = 'Vincent Van Gogh'; scrollToFilters();" class="btn btn-primary">
        Browse Vincent's Work <ArrowRight size="16" />
      </button>
    </div>
    <div style="border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-lg); border: 1px solid var(--border-color); background: #000; height: 350px;">
      <img src="https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=800&auto=format&fit=crop" style="width:100%; height:100%; object-fit:cover; opacity:0.85;" />
    </div>
  </div>
</template>

<style scoped>
/* Responsive tweaks */
@media (max-width: 768px) {
  .hero-banner {
    grid-template-columns: 1fr !important;
    text-align: center !important;
    gap: 2rem !important;
  }
  .hero-banner div {
    text-align: center !important;
    justify-content: center !important;
  }
}
</style>
