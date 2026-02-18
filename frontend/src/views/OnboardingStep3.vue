<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white py-12">
    <div class="container mx-auto px-6 max-w-6xl">
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
            <div class="w-16 h-1 bg-green-500"></div>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <span class="ml-2 text-gray-600">Registra</span>
            </div>
            <div class="w-16 h-1 bg-brand-navy"></div>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-brand-navy text-white rounded-full flex items-center justify-center font-bold">3</div>
              <span class="ml-2 text-brand-navy font-semibold">Paga</span>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mb-12">
        <h1 class="text-5xl font-elegant text-brand-navy mb-4">Finaliza tu Compra</h1>
        <p class="text-xl text-gray-600">Selecciona tu plan y método de pago</p>
      </div>

      <div class="grid lg:grid-cols-3 gap-8">
        <!-- Plan Selection & Payment -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Plan Selection -->
          <div class="card">
            <h2 class="text-2xl font-elegant text-brand-navy mb-6">Selecciona tu Plan</h2>
            
            <div class="space-y-4">
              <div
                v-for="(plan, key) in plans"
                :key="key"
                @click="selectedPlan = key"
                class="border-2 rounded-lg p-6 cursor-pointer transition-all duration-300"
                :class="{
                  'border-brand-gold bg-brand-gold/5 ring-2 ring-brand-gold/20': selectedPlan === key,
                  'border-gray-200 hover:border-brand-navy/30': selectedPlan !== key
                }"
                :data-testid="`select-plan-${key}`"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <h3 class="text-xl font-bold text-brand-navy mb-1">{{ plan.name }}</h3>
                    <p class="text-gray-600 text-sm mb-2">
                      {{ plan.type === 'one_time' ? 'Pago único' : 'Suscripción mensual' }}
                    </p>
                  </div>
                  <div class="text-right">
                    <div class="text-3xl font-bold text-brand-navy">
                      ${{ plan.price.toLocaleString() }}
                    </div>
                    <div class="text-sm text-gray-600">{{ plan.currency }}</div>
                  </div>
                  <div class="ml-4">
                    <div
                      class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                      :class="{
                        'border-brand-gold bg-brand-gold': selectedPlan === key,
                        'border-gray-300': selectedPlan !== key
                      }"
                    >
                      <svg v-if="selectedPlan === key" class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Method Selection -->
          <div class="card" v-if="selectedPlan">
            <h2 class="text-2xl font-elegant text-brand-navy mb-6">Método de Pago</h2>
            
            <div class="grid md:grid-cols-2 gap-4 mb-6">
              <button
                @click="paymentMethod = 'stripe'"
                class="p-6 border-2 rounded-lg transition-all duration-300 flex items-center justify-center"
                :class="{
                  'border-brand-navy bg-brand-navy/5 ring-2 ring-brand-navy/20': paymentMethod === 'stripe',
                  'border-gray-200 hover:border-brand-navy/30': paymentMethod !== 'stripe'
                }"
                data-testid="payment-method-stripe"
              >
                <div class="text-center">
                  <div class="text-4xl mb-2">💳</div>
                  <div class="font-semibold text-brand-navy">Stripe</div>
                  <div class="text-sm text-gray-600">Tarjetas internacionales</div>
                </div>
              </button>

              <button
                @click="paymentMethod = 'mercadopago'"
                class="p-6 border-2 rounded-lg transition-all duration-300 flex items-center justify-center"
                :class="{
                  'border-brand-navy bg-brand-navy/5 ring-2 ring-brand-navy/20': paymentMethod === 'mercadopago',
                  'border-gray-200 hover:border-brand-navy/30': paymentMethod !== 'mercadopago'
                }"
                data-testid="payment-method-mercadopago"
              >
                <div class="text-center">
                  <div class="text-4xl mb-2">🇦🇷</div>
                  <div class="font-semibold text-brand-navy">MercadoPago</div>
                  <div class="text-sm text-gray-600">Argentina & LATAM</div>
                </div>
              </button>
            </div>

            <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {{ error }}
            </div>

            <button
              @click="processPayment"
              :disabled="!selectedPlan || !paymentMethod || loading"
              class="btn-primary w-full text-lg"
              data-testid="btn-procesar-pago"
            >
              <span v-if="loading">Procesando...</span>
              <span v-else>Proceder al Pago</span>
            </button>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="card sticky top-6 bg-gradient-to-br from-brand-navy to-gray-900 text-white">
            <h3 class="text-2xl font-elegant mb-6 text-brand-gold">Resumen de Compra</h3>
            
            <div v-if="invitation" class="bg-white/10 rounded-lg p-4 mb-6">
              <div class="text-sm text-gray-300 mb-2">Tu invitación</div>
              <div class="text-lg font-semibold">
                {{ invitation.custom_data.groom_name }} & {{ invitation.custom_data.bride_name }}
              </div>
              <div class="text-sm text-gray-300 mt-1">
                📅 {{ invitation.custom_data.event_date }}
              </div>
              <div class="text-sm text-gray-300">
                📍 {{ invitation.custom_data.venue }}
              </div>
            </div>

            <div v-if="selectedPlan" class="space-y-4">
              <div class="border-t border-white/20 pt-4">
                <div class="flex justify-between mb-2">
                  <span class="text-gray-300">Plan seleccionado</span>
                  <span class="font-semibold">{{ plans[selectedPlan].name }}</span>
                </div>
                <div class="flex justify-between mb-2">
                  <span class="text-gray-300">Tipo</span>
                  <span class="text-sm">
                    {{ plans[selectedPlan].type === 'one_time' ? 'Pago único' : 'Mensual' }}
                  </span>
                </div>
              </div>

              <div class="border-t border-white/20 pt-4">
                <div class="flex justify-between items-center">
                  <span class="text-xl font-semibold">Total</span>
                  <div class="text-right">
                    <div class="text-3xl font-bold text-brand-gold">
                      ${{ plans[selectedPlan].price.toLocaleString() }}
                    </div>
                    <div class="text-sm text-gray-300">{{ plans[selectedPlan].currency }}</div>
                  </div>
                </div>
              </div>

              <div class="bg-white/10 rounded-lg p-4 mt-6">
                <div class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                  </svg>
                  <p class="text-sm text-gray-300">
                    Pago 100% seguro. Tus datos están protegidos con encriptación de nivel bancario.
                  </p>
                </div>
              </div>
            </div>

            <div v-else class="text-center text-gray-400 py-8">
              Selecciona un plan para continuar
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useInvitationStore } from '../stores/invitation'
import axios from 'axios'

const router = useRouter()
const invitationStore = useInvitationStore()

const API_URL = import.meta.env.VITE_BACKEND_URL

const plans = ref({})
const selectedPlan = ref('')
const paymentMethod = ref('stripe')
const invitation = ref(null)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    // Load current invitation
    invitationStore.loadCurrentInvitation()
    invitation.value = invitationStore.currentInvitation

    if (!invitation.value) {
      router.push('/onboarding/step1')
      return
    }

    // Fetch plans
    const plansData = await invitationStore.fetchPlans()
    plans.value = plansData

    // Pre-select PRO plan
    selectedPlan.value = 'pro'
  } catch (err) {
    console.error('Error loading payment page:', err)
    error.value = 'Error al cargar la información de pago'
  }
})

const processPayment = async () => {
  if (!selectedPlan.value || !paymentMethod.value) {
    error.value = 'Por favor selecciona un plan y método de pago'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const token = localStorage.getItem('session_token')
    const originUrl = window.location.origin

    if (paymentMethod.value === 'stripe') {
      // Create Stripe checkout session
      const response = await axios.post(
        `${API_URL}/payments/stripe/checkout`,
        {
          invitation_id: invitation.value.invitation_id,
          plan_type: selectedPlan.value,
          origin_url: originUrl
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true
        }
      )

      // Redirect to Stripe
      window.location.href = response.data.url

    } else if (paymentMethod.value === 'mercadopago') {
      // Create MercadoPago preference
      const response = await axios.post(
        `${API_URL}/payments/mercadopago/checkout`,
        {
          invitation_id: invitation.value.invitation_id,
          plan_type: selectedPlan.value,
          origin_url: originUrl
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true
        }
      )

      // Redirect to MercadoPago
      window.location.href = response.data.init_point
    }

  } catch (err) {
    console.error('Payment processing error:', err)
    error.value = err.response?.data?.detail || 'Error al procesar el pago. Por favor intenta nuevamente.'
    loading.value = false
  }
}
</script>
