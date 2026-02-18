<template>
  <div class="min-h-screen bg-gradient-to-b from-green-50 to-white py-12">
    <div class="container mx-auto px-6 max-w-4xl">
      <div v-if="loading" class="text-center py-20">
        <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-brand-navy mx-auto mb-4"></div>
        <h2 class="text-2xl font-elegant text-brand-navy mb-2">Verificando tu pago...</h2>
        <p class="text-gray-600">Espera un momento</p>
      </div>

      <div v-else-if="paymentStatus === 'success'" class="text-center">
        <!-- Success Animation -->
        <div class="mb-8">
          <div class="inline-flex items-center justify-center w-24 h-24 bg-green-100 rounded-full mb-6 animate-bounce">
            <svg class="w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          
          <h1 class="text-5xl font-elegant text-brand-navy mb-4">
            ¡Pago Exitoso! 🎉
          </h1>
          <p class="text-xl text-gray-600 mb-8">
            Tu invitación ha sido creada exitosamente
          </p>
        </div>

        <div class="card max-w-2xl mx-auto mb-8">
          <div class="bg-gradient-to-r from-brand-navy to-brand-gold text-white rounded-lg p-8 mb-6">
            <h2 class="text-3xl font-elegant mb-4">Tu Invitación Está Lista</h2>
            <div class="text-lg opacity-90">
              <p class="mb-2">📧 Te hemos enviado un correo con todos los detalles</p>
              <p>🔗 Podrás compartir tu invitación con tus invitados</p>
            </div>
          </div>

          <div class="space-y-4 text-left">
            <div class="flex items-start p-4 bg-green-50 rounded-lg">
              <svg class="w-6 h-6 text-green-500 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Invitación Creada</h3>
                <p class="text-gray-600 text-sm">Tu invitación personalizada está lista para compartir</p>
              </div>
            </div>

            <div class="flex items-start p-4 bg-blue-50 rounded-lg">
              <svg class="w-6 h-6 text-blue-500 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
              </svg>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Email Enviado</h3>
                <p class="text-gray-600 text-sm">Revisa tu bandeja de entrada para más información</p>
              </div>
            </div>

            <div class="flex items-start p-4 bg-purple-50 rounded-lg">
              <svg class="w-6 h-6 text-purple-500 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
              </svg>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Próximos Pasos</h3>
                <p class="text-gray-600 text-sm">Accede a tu panel para gestionar tus invitados y más</p>
              </div>
            </div>
          </div>

          <div class="mt-8 pt-8 border-t border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Detalles del Pago</h3>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-gray-600">ID de Transacción:</span>
                <p class="font-mono text-xs text-gray-900 mt-1">{{ sessionId }}</p>
              </div>
              <div>
                <span class="text-gray-600">Fecha:</span>
                <p class="text-gray-900 mt-1">{{ new Date().toLocaleDateString('es-AR') }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            @click="goToDashboard"
            class="btn-primary px-8 py-4 text-lg"
            data-testid="btn-ir-panel"
          >
            Ir a Mi Panel
          </button>
          
          <button
            @click="goToHome"
            class="px-8 py-4 border-2 border-brand-navy text-brand-navy font-semibold rounded-lg hover:bg-brand-navy hover:text-white transition-all duration-300"
          >
            Volver al Inicio
          </button>
        </div>

        <div class="mt-12 text-center">
          <p class="text-gray-600 mb-4">¿Necesitas ayuda?</p>
          <a href="mailto:soporte@invitamesr.com" class="text-brand-navy hover:text-brand-gold font-semibold">
            Contacta con Soporte
          </a>
        </div>
      </div>

      <div v-else-if="paymentStatus === 'pending'" class="text-center">
        <div class="mb-8">
          <div class="inline-flex items-center justify-center w-24 h-24 bg-yellow-100 rounded-full mb-6">
            <svg class="w-12 h-12 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          
          <h1 class="text-5xl font-elegant text-brand-navy mb-4">
            Pago Pendiente
          </h1>
          <p class="text-xl text-gray-600 mb-8">
            Tu pago está siendo procesado
          </p>
        </div>

        <div class="card max-w-2xl mx-auto mb-8">
          <p class="text-gray-700 mb-4">
            Tu pago está en proceso de verificación. Te notificaremos por email cuando esté confirmado.
          </p>
          <p class="text-gray-600 text-sm">
            Esto puede tomar algunos minutos. Si tienes alguna duda, contacta con soporte.
          </p>
        </div>

        <button
          @click="goToHome"
          class="btn-primary"
        >
          Volver al Inicio
        </button>
      </div>

      <div v-else class="text-center">
        <div class="mb-8">
          <div class="inline-flex items-center justify-center w-24 h-24 bg-red-100 rounded-full mb-6">
            <svg class="w-12 h-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </div>
          
          <h1 class="text-5xl font-elegant text-brand-navy mb-4">
            Pago No Completado
          </h1>
          <p class="text-xl text-gray-600 mb-8">
            No se pudo completar tu pago
          </p>
        </div>

        <div class="card max-w-2xl mx-auto mb-8">
          <p class="text-gray-700 mb-4">
            {{ errorMessage || 'Hubo un problema al procesar tu pago. Por favor intenta nuevamente.' }}
          </p>
        </div>

        <div class="flex gap-4 justify-center">
          <button
            @click="retryPayment"
            class="btn-primary"
          >
            Intentar Nuevamente
          </button>
          
          <button
            @click="goToHome"
            class="px-8 py-3 border-2 border-brand-navy text-brand-navy font-semibold rounded-lg hover:bg-brand-navy hover:text-white transition-all duration-300"
          >
            Volver al Inicio
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const API_URL = import.meta.env.VITE_BACKEND_URL

const loading = ref(true)
const paymentStatus = ref('pending')
const sessionId = ref('')
const errorMessage = ref('')

onMounted(async () => {
  // Get session_id from URL query params
  const urlParams = new URLSearchParams(window.location.search)
  sessionId.value = urlParams.get('session_id')

  if (!sessionId.value) {
    paymentStatus.value = 'error'
    errorMessage.value = 'No se encontró información del pago'
    loading.value = false
    return
  }

  // Poll for payment status
  await checkPaymentStatus()
})

const checkPaymentStatus = async (attempt = 0) => {
  const maxAttempts = 5
  
  try {
    const response = await axios.get(
      `${API_URL}/payments/stripe/status/${sessionId.value}`
    )

    if (response.data.payment_status === 'paid') {
      paymentStatus.value = 'success'
      loading.value = false
    } else if (response.data.status === 'expired') {
      paymentStatus.value = 'error'
      errorMessage.value = 'La sesión de pago ha expirado'
      loading.value = false
    } else if (attempt < maxAttempts) {
      // Continue polling
      setTimeout(() => checkPaymentStatus(attempt + 1), 2000)
    } else {
      paymentStatus.value = 'pending'
      loading.value = false
    }
  } catch (error) {
    console.error('Error checking payment status:', error)
    if (attempt < maxAttempts) {
      setTimeout(() => checkPaymentStatus(attempt + 1), 2000)
    } else {
      paymentStatus.value = 'error'
      errorMessage.value = 'Error al verificar el estado del pago'
      loading.value = false
    }
  }
}

const goToDashboard = () => {
  alert('Panel administrativo próximamente. Por ahora puedes crear otra invitación.')
  router.push('/')
}

const goToHome = () => {
  router.push('/')
}

const retryPayment = () => {
  router.push('/onboarding/payment')
}
</script>
