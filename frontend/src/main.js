import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import './assets/main.css'
import axios from 'axios'

// Set dynamic base URL for backend connection
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
