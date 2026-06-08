import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role || 'guest',
  },
  actions: {
    async login(email, password) {
      const res = await axios.post('/auth/login', { email, password })
      this.token = res.data.access_token
      this.user = { 
        role: res.data.role, 
        username: res.data.username,
        email: email,
        _id: res.data._id
      }
      localStorage.setItem('token', this.token)
      localStorage.setItem('user', JSON.stringify(this.user))
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
