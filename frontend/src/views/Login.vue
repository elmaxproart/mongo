<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
import { LogIn, UserPlus, AlertCircle, Sparkles } from 'lucide-vue-next'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const username = ref('')
const role = ref('user')
const error = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  error.value = ''
  isLoading.value = true
  try {
    if (isLogin.value) {
      await auth.login(email.value, password.value)
      router.push('/')
    } else {
      await axios.post('/auth/register', {
        email: email.value,
        password: password.value,
        username: username.value,
        role: role.value
      })
      isLogin.value = true
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'An error occurred during authentication.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div style="max-width: 440px; margin: 4rem auto 6rem; padding: 0.5rem;" class="animate-slide-up">
    <!-- Header visual -->
    <div style="text-align: center; margin-bottom: 2rem;">
      <div style="font-family: 'Bodoni Moda', serif; font-size: 2.2rem; font-weight: 600; letter-spacing: 0.05em; display: inline-flex; align-items: center; gap: 0.5rem; justify-content: center; margin-bottom: 0.5rem;">
        E-GALLERY
      </div>
      <p style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.6; display: flex; align-items: center; justify-content: center; gap: 0.35rem;">
        <Sparkles size="12" style="color: var(--accent-color);" /> Fine Art Marketplace
      </p>
    </div>

    <!-- Main Form Glass Panel -->
    <div class="glass-panel" style="padding: 2.5rem; border-radius: var(--radius-md);">
      
      <!-- Form Toggle Tabs -->
      <div style="display: flex; border-bottom: 1.5px solid var(--border-color); margin-bottom: 2rem;">
        <button 
          @click="isLogin = true; error = ''" 
          :style="{
            flex: 1,
            background: 'none',
            border: 'none',
            paddingBottom: '0.85rem',
            fontWeight: isLogin ? '600' : '400',
            fontSize: '0.9rem',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: isLogin ? 'var(--text-color)' : 'var(--text-muted)',
            borderBottom: isLogin ? '2px solid var(--text-color)' : '2px solid transparent',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }"
        >
          {{ t('auth.login_title') }}
        </button>
        <button 
          @click="isLogin = false; error = ''" 
          :style="{
            flex: 1,
            background: 'none',
            border: 'none',
            paddingBottom: '0.85rem',
            fontWeight: !isLogin ? '600' : '400',
            fontSize: '0.9rem',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: !isLogin ? 'var(--text-color)' : 'var(--text-muted)',
            borderBottom: !isLogin ? '2px solid var(--text-color)' : '2px solid transparent',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }"
        >
          {{ t('auth.register_title') }}
        </button>
      </div>

      <!-- Error alert -->
      <div v-if="error" class="glass-panel" style="padding: 1rem; border-color: #ef4444; background: rgba(239, 68, 68, 0.05); margin-bottom: 1.5rem; border-radius: var(--radius-sm); display: flex; gap: 0.75rem; align-items: center;">
        <AlertCircle size="18" style="color: #ef4444; flex-shrink: 0;" />
        <span style="font-size: 0.85rem; color: #ef4444;">{{ error }}</span>
      </div>

      <!-- Form Fields -->
      <form @submit.prevent="handleSubmit" style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <!-- Username (Register only) -->
        <div v-if="!isLogin" style="display: flex; flex-direction: column; gap: 0.4rem;" class="animate-fade-in">
          <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">Username</label>
          <input v-model="username" type="text" placeholder="Claude Monet" class="input-control" required>
        </div>

        <!-- Email -->
        <div style="display: flex; flex-direction: column; gap: 0.4rem;">
          <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">
            {{ t('auth.email') }}
          </label>
          <input v-model="email" type="email" placeholder="artist@egallery.com" class="input-control" required>
        </div>

        <!-- Password -->
        <div style="display: flex; flex-direction: column; gap: 0.4rem;">
          <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">
            {{ t('auth.password') }}
          </label>
          <input v-model="password" type="password" placeholder="••••••••" class="input-control" required>
        </div>

        <!-- Role Select (Register only) -->
        <div v-if="!isLogin" style="display: flex; flex-direction: column; gap: 0.4rem;" class="animate-fade-in">
          <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;">
            Account Type
          </label>
          <select v-model="role" class="input-control" style="cursor: pointer;">
            <option value="user">Collector / Client</option>
            <option value="artist">Artist Creator</option>
          </select>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary" :disabled="isLoading" style="justify-content: center; padding: 1rem; font-weight: 600; margin-top: 0.5rem; font-size: 0.9rem;">
          <span v-if="isLoading" class="loader" style="border: 2px solid white; border-top: 2px solid transparent; border-radius: 50%; width: 16px; height: 16px; animation: spin 0.6s linear infinite; display: inline-block;"></span>
          <span v-else style="display: inline-flex; align-items: center; gap: 0.5rem;">
            <LogIn v-if="isLogin" size="16" />
            <UserPlus v-else size="16" />
            {{ isLogin ? 'Sign Into Studio' : 'Create Studio Account' }}
          </span>
        </button>

      </form>
    </div>

    <!-- Credentials Helper Box for Demo -->
    <div class="glass-panel" style="padding: 1.25rem; border-radius: var(--radius-sm); margin-top: 2rem; font-size: 0.8rem; line-height: 1.5; opacity: 0.85;">
      <p style="font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-color); margin-bottom: 0.5rem;">Demo Credentials</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
        <div>
          <strong>Collector/User:</strong><br>
          user@egallery.com / user123
        </div>
        <div>
          <strong>Artist Creator:</strong><br>
          artist@egallery.com / artist123
        </div>
        <div style="grid-column: span 2; border-top: 1px solid var(--border-color); padding-top: 0.5rem; margin-top: 0.25rem;">
          <strong>Administrator:</strong><br>
          admin@egallery.com / admin123
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
