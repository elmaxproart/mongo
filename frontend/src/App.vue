<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './store/auth'
import { useI18n } from 'vue-i18n'
import { Sun, Moon, Languages, LogOut } from 'lucide-vue-next'
import axios from 'axios'

const auth = useAuthStore()
const router = useRouter()
const { t, locale } = useI18n()
const theme = ref(localStorage.getItem('theme') || 'dark')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme.value)
  localStorage.setItem('theme', theme.value)
}

const toggleLang = () => {
  locale.value = locale.value === 'fr' ? 'en' : 'fr'
}

const logout = () => {
  auth.logout()
  router.push('/')
}

onMounted(async () => {
  document.documentElement.setAttribute('data-theme', theme.value)
  if (auth.token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${auth.token}`
    try {
      const res = await axios.get('/auth/me')
      auth.user = { 
        role: res.data.role, 
        username: res.data.username,
        email: res.data.email,
        _id: res.data._id
      }
      localStorage.setItem('user', JSON.stringify(auth.user))
    } catch (e) {
      auth.logout()
    }
  }
})
</script>

<template>
  <header>
    <div class="container nav">
      <router-link to="/" class="logo">E-Gallery</router-link>
      <div class="nav-links">
        <router-link to="/">{{ t('nav.home') }}</router-link>
        <router-link to="/docs">{{ t('nav.docs') }}</router-link>
        <router-link v-if="auth.role === 'artist' || auth.role === 'admin'" to="/artist">{{ t('nav.artist') }}</router-link>
        <router-link v-if="auth.role === 'admin'" to="/admin">{{ t('nav.admin') }}</router-link>
        
        <button @click="toggleLang" class="theme-toggle" :title="locale === 'fr' ? 'English' : 'Français'">
          <Languages size="16" />
        </button>
        
        <button @click="toggleTheme" class="theme-toggle" title="Toggle Theme">
          <Sun v-if="theme === 'light'" size="16" />
          <Moon v-else size="16" />
        </button>

        <template v-if="!auth.isAuthenticated">
          <router-link to="/login" class="btn btn-primary" style="padding: 0.5rem 1.2rem; font-size: 0.8rem;">
            {{ t('nav.login') }}
          </router-link>
        </template>
        <template v-else>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="text-align: right; display: flex; flex-direction: column;">
              <span style="font-size: 0.85rem; font-weight: 600;">{{ auth.user.username }}</span>
              <span style="font-size: 0.7rem; color: var(--accent-color); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
                {{ auth.role }}
              </span>
            </div>
            <button @click="logout" class="theme-toggle" :title="t('nav.logout')" style="border-color: #ef4444; color: #ef4444;">
              <LogOut size="16" />
            </button>
          </div>
        </template>
      </div>
    </div>
  </header>

  <main class="container animate-fade-in" style="min-height: calc(100vh - 180px); padding-top: 2rem;">
    <router-view></router-view>
  </main>

  <footer style="margin-top: 6rem; padding: 3rem 0; border-top: 1px solid var(--border-color); text-align: center; font-size: 0.9rem; color: var(--text-muted);">
    <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
      <span style="font-family: 'Bodoni Moda', serif; font-size: 1.1rem; font-weight: 600; letter-spacing: 0.05em;">E-GALLERY</span>
      <span>&copy; 2026 E-Gallery. All rights reserved.</span>
    </div>
  </footer>
</template>

<style>
/* Reset container rules from default Vite config */
#app {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  border-inline: none !important;
  min-height: 100vh !important;
  display: block !important;
}
</style>
