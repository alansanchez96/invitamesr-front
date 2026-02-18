<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white py-12">
    <div class="container mx-auto px-6 max-w-4xl">
      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex items-center justify-center">
          <div class="flex items-center space-x-4">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <span class="ml-2 text-gray-600">Diseña</span>
            </div>
            <div class="w-16 h-1 bg-brand-navy"></div>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-brand-navy text-white rounded-full flex items-center justify-center font-bold">2</div>
              <span class="ml-2 text-brand-navy font-semibold">Registra</span>
            </div>
            <div class="w-16 h-1 bg-gray-300"></div>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gray-300 text-gray-600 rounded-full flex items-center justify-center font-bold">3</div>
              <span class="ml-2 text-gray-600">Paga</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card max-w-md mx-auto text-center">
        <div class="mb-8">
          <div class="text-6xl mb-4">🔐</div>
          <h1 class="text-4xl font-elegant text-brand-navy mb-4">Casi Listo</h1>
          <p class="text-xl text-gray-600">
            Guarda tu invitación creando tu cuenta
          </p>
        </div>

        <div class="bg-gray-50 rounded-lg p-6 mb-8">
          <h3 class="text-lg font-semibold text-gray-900 mb-3">Tu invitación incluye:</h3>
          <div class="space-y-2 text-left">
            <div class="flex items-start">
              <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-gray-700">Plantilla personalizada elegida</span>
            </div>
            <div class="flex items-start">
              <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-gray-700">Todos tus datos personalizados</span>
            </div>
            <div class="flex items-start">
              <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-gray-700">Acceso a tu panel de gestión</span>
            </div>
          </div>
        </div>

        <button
          @click="loginWithGoogle"
          class="w-full bg-white border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-lg font-semibold text-lg hover:border-brand-navy hover:bg-gray-50 transition-all duration-300 flex items-center justify-center space-x-3 shadow-md hover:shadow-lg"
          data-testid="btn-google-login"
        >
          <svg class="w-6 h-6" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          <span>Continuar con Google</span>
        </button>

        <p class="text-sm text-gray-500 mt-6">
          Al continuar, aceptas nuestros términos y condiciones
        </p>

        <button
          @click="goBack"
          class="mt-6 text-brand-navy hover:text-brand-gold transition-colors flex items-center mx-auto"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          Volver a editar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const loginWithGoogle = () => {
  // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
  const redirectUrl = window.location.origin + '/auth/callback'
  window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`
}

const goBack = () => {
  router.push('/onboarding/step1')
}
</script>