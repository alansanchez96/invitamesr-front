import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_BACKEND_URL

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false
  }),

  actions: {
    async processSession(sessionId) {
      this.loading = true
      try {
        const response = await axios.post(`${API_URL}/auth/session`, {
          session_id: sessionId
        }, {
          withCredentials: true
        })

        this.user = response.data.user
        this.isAuthenticated = true
        localStorage.setItem('session_token', response.data.session_token)
        
        return response.data
      } catch (error) {
        console.error('Session processing error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async checkAuth() {
      this.loading = true
      try {
        const token = localStorage.getItem('session_token')
        if (!token) {
          this.isAuthenticated = false
          return false
        }

        const response = await axios.get(`${API_URL}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true
        })

        this.user = response.data
        this.isAuthenticated = true
        return true
      } catch (error) {
        this.isAuthenticated = false
        localStorage.removeItem('session_token')
        return false
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        const token = localStorage.getItem('session_token')
        await axios.post(`${API_URL}/auth/logout`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true
        })
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('session_token')
      }
    }
  }
})