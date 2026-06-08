import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Artwork from '../views/Artwork.vue'
import DashboardArtist from '../views/DashboardArtist.vue'
import DashboardAdmin from '../views/DashboardAdmin.vue'
import Documentation from '../views/Documentation.vue'
import { useAuthStore } from '../store/auth'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/artwork/:id', component: Artwork },
  { path: '/docs', component: Documentation },
  { 
    path: '/artist', 
    component: DashboardArtist,
    beforeEnter: (to, from, next) => {
      const auth = useAuthStore()
      if (auth.role === 'artist' || auth.role === 'admin') next()
      else next('/login')
    }
  },
  { 
    path: '/admin', 
    component: DashboardAdmin,
    beforeEnter: (to, from, next) => {
      const auth = useAuthStore()
      if (auth.role === 'admin') next()
      else next('/login')
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
