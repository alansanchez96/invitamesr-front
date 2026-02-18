import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_BACKEND_URL

export const useInvitationStore = defineStore('invitation', {
  state: () => ({
    currentInvitation: null,
    events: [],
    templates: [],
    plans: {},
    loading: false
  }),

  actions: {
    async fetchEvents() {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/events`)
        this.events = response.data.events
        return response.data.events
      } catch (error) {
        console.error('Fetch events error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTemplates(eventType) {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/events/${eventType}/templates`)
        this.templates = response.data.templates
        return response.data.templates
      } catch (error) {
        console.error('Fetch templates error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchPlans() {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/plans`)
        this.plans = response.data.plans
        return response.data.plans
      } catch (error) {
        console.error('Fetch plans error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createInvitation(data) {
      this.loading = true
      try {
        const token = localStorage.getItem('session_token')
        const response = await axios.post(`${API_URL}/invitations`, data, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true
        })

        this.currentInvitation = response.data.invitation
        localStorage.setItem('current_invitation', JSON.stringify(response.data.invitation))
        return response.data.invitation
      } catch (error) {
        console.error('Create invitation error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateInvitation(invitationId, customData) {
      this.loading = true
      try {
        const token = localStorage.getItem('session_token')
        const response = await axios.put(
          `${API_URL}/invitations/${invitationId}`,
          { custom_data: customData },
          {
            headers: {
              'Authorization': `Bearer ${token}`
            },
            withCredentials: true
          }
        )

        this.currentInvitation = response.data.invitation
        localStorage.setItem('current_invitation', JSON.stringify(response.data.invitation))
        return response.data.invitation
      } catch (error) {
        console.error('Update invitation error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    loadCurrentInvitation() {
      const stored = localStorage.getItem('current_invitation')
      if (stored) {
        this.currentInvitation = JSON.parse(stored)
      }
    },

    clearCurrentInvitation() {
      this.currentInvitation = null
      localStorage.removeItem('current_invitation')
    }
  }
})