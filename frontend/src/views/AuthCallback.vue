<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white flex items-center justify-center">
    <div class="text-center">
      <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-brand-navy mx-auto mb-4"></div>
      <h2 class="text-2xl font-elegant text-brand-navy mb-2">Procesando tu registro...</h2>
      <p class="text-gray-600">Espera un momento</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useInvitationStore } from '../stores/invitation'

const router = useRouter()
const authStore = useAuthStore()
const invitationStore = useInvitationStore()

const hasProcessed = ref(false)

onMounted(async () => {
  // Prevent double processing
  if (hasProcessed.value) return
  hasProcessed.value = true

  try {
    // Extract session_id from URL hash
    const hash = window.location.hash
    const sessionIdMatch = hash.match(/session_id=([^&]+)/)
    
    if (!sessionIdMatch) {
      console.error('No session_id found')
      router.push('/onboarding/step2')
      return
    }

    const sessionId = sessionIdMatch[1]
    
    // Process session with backend
    await authStore.processSession(sessionId)
    
    // Get pending invitation from localStorage
    const pendingInvitation = localStorage.getItem('pending_invitation')
    
    if (pendingInvitation) {
      const invitationData = JSON.parse(pendingInvitation)
      
      // Create invitation in backend
      await invitationStore.createInvitation(invitationData)
      
      // Clear pending data
      localStorage.removeItem('pending_invitation')
    }
    
    // Redirect to payment step
    router.push('/onboarding/payment')
    
  } catch (error) {
    console.error('Auth callback error:', error)
    alert('Error al procesar tu registro. Por favor intenta nuevamente.')
    router.push('/onboarding/step2')
  }
})
</script>