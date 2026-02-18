<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white py-12">
    <div class="container mx-auto px-6 max-w-6xl">
      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex items-center justify-center">
          <div class="flex items-center space-x-4">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-brand-navy text-white rounded-full flex items-center justify-center font-bold">1</div>
              <span class="ml-2 text-brand-navy font-semibold">Diseña</span>
            </div>
            <div class="w-16 h-1 bg-gray-300"></div>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gray-300 text-gray-600 rounded-full flex items-center justify-center font-bold">2</div>
              <span class="ml-2 text-gray-600">Registra</span>
            </div>
            <div class="w-16 h-1 bg-gray-300"></div>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gray-300 text-gray-600 rounded-full flex items-center justify-center font-bold">3</div>
              <span class="ml-2 text-gray-600">Paga</span>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mb-12">
        <h1 class="text-5xl font-elegant text-brand-navy mb-4">Crea Tu Invitación</h1>
        <p class="text-xl text-gray-600">Personaliza cada detalle de tu invitación</p>
      </div>

      <!-- Event Type Selection -->
      <div v-if="step === 'event'" class="max-w-4xl mx-auto">
        <div class="card mb-8">
          <h2 class="text-3xl font-elegant text-brand-navy mb-6">Selecciona el tipo de evento</h2>
          
          <div class="grid md:grid-cols-2 gap-6">
            <button
              @click="selectEvent('boda')"
              class="p-8 border-2 rounded-xl hover:border-brand-gold hover:shadow-lg transition-all duration-300"
              :class="{ 'border-brand-gold bg-brand-gold/5': formData.event_type === 'boda', 'border-gray-200': formData.event_type !== 'boda' }"
              data-testid="evento-boda"
            >
              <div class="text-6xl mb-4">💍</div>
              <h3 class="text-2xl font-elegant text-brand-navy mb-2">Boda</h3>
              <p class="text-gray-600">Invitaciones elegantes para tu día especial</p>
            </button>

            <div class="p-8 border-2 border-gray-200 rounded-xl opacity-50 cursor-not-allowed">
              <div class="text-6xl mb-4">🎉</div>
              <h3 class="text-2xl font-elegant text-gray-500 mb-2">Próximamente</h3>
              <p class="text-gray-500">XV Años, Cumpleaños, y más...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Template Selection -->
      <div v-if="step === 'template'" class="max-w-6xl mx-auto">
        <div class="card mb-8">
          <button 
            @click="step = 'event'" 
            class="mb-6 text-brand-navy hover:text-brand-gold transition-colors flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
            Volver
          </button>

          <h2 class="text-3xl font-elegant text-brand-navy mb-6">Elige tu plantilla</h2>
          
          <div class="grid md:grid-cols-2 gap-8" v-if="templates.length > 0">
            <div
              v-for="template in templates"
              :key="template.id"
              @click="selectTemplate(template.id)"
              class="cursor-pointer border-2 rounded-xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              :class="{ 'border-brand-gold ring-4 ring-brand-gold/20': formData.template_id === template.id, 'border-gray-200': formData.template_id !== template.id }"
              :data-testid="`template-${template.id}`"
            >
              <img :src="template.preview_url" :alt="template.name" class="w-full h-64 object-cover" />
              <div class="p-6">
                <h3 class="text-2xl font-elegant text-brand-navy mb-2">{{ template.name }}</h3>
                <p class="text-gray-600">{{ template.description }}</p>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-12">
            <p class="text-gray-600">Cargando plantillas...</p>
          </div>
        </div>
      </div>

      <!-- Customization Form -->
      <div v-if="step === 'customize'" class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-2 gap-8">
          <!-- Form -->
          <div class="card">
            <button 
              @click="step = 'template'" 
              class="mb-6 text-brand-navy hover:text-brand-gold transition-colors flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              Cambiar plantilla
            </button>

            <h2 class="text-3xl font-elegant text-brand-navy mb-6">Personaliza tu invitación</h2>
            
            <form @submit.prevent="saveInvitation" class="space-y-6">
              <div>
                <label class="block text-gray-700 font-semibold mb-2">Nombre del Novio</label>
                <input
                  v-model="formData.custom_data.groom_name"
                  type="text"
                  class="input-field"
                  placeholder="Ej: Juan"
                  required
                  data-testid="input-groom-name"
                />
              </div>

              <div>
                <label class="block text-gray-700 font-semibold mb-2">Nombre de la Novia</label>
                <input
                  v-model="formData.custom_data.bride_name"
                  type="text"
                  class="input-field"
                  placeholder="Ej: María"
                  required
                  data-testid="input-bride-name"
                />
              </div>

              <div>
                <label class="block text-gray-700 font-semibold mb-2">Fecha del Evento</label>
                <input
                  v-model="formData.custom_data.event_date"
                  type="date"
                  class="input-field"
                  required
                  data-testid="input-event-date"
                />
              </div>

              <div>
                <label class="block text-gray-700 font-semibold mb-2">Lugar del Evento</label>
                <input
                  v-model="formData.custom_data.venue"
                  type="text"
                  class="input-field"
                  placeholder="Ej: Salón Los Jardines"
                  required
                  data-testid="input-venue"
                />
              </div>

              <div>
                <label class="block text-gray-700 font-semibold mb-2">Mensaje Especial</label>
                <textarea
                  v-model="formData.custom_data.message"
                  class="input-field"
                  rows="4"
                  placeholder="Un mensaje para tus invitados..."
                  data-testid="input-message"
                ></textarea>
              </div>

              <div>
                <label class="block text-gray-700 font-semibold mb-2">Código de Vestimenta</label>
                <select v-model="formData.custom_data.dress_code" class="input-field" data-testid="select-dress-code">
                  <option value="">Seleccionar...</option>
                  <option value="formal">Formal</option>
                  <option value="semi-formal">Semi-formal</option>
                  <option value="casual-elegante">Casual Elegante</option>
                  <option value="cocktail">Cocktail</option>
                </select>
              </div>

              <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {{ error }}
              </div>

              <button
                type="submit"
                class="btn-primary w-full"
                :disabled="loading"
                data-testid="btn-guardar-continuar"
              >
                {{ loading ? 'Guardando...' : 'Guardar y Continuar' }}
              </button>
            </form>
          </div>

          <!-- Preview -->
          <div class="card bg-gradient-to-br from-brand-navy to-gray-900 text-white sticky top-6">
            <h3 class="text-2xl font-elegant mb-6 text-brand-gold">Vista Previa</h3>
            
            <div class="bg-white text-gray-900 rounded-lg p-8 space-y-4">
              <div class="text-center">
                <div class="text-4xl mb-4">💍</div>
                <h2 class="text-3xl font-elegant text-brand-navy mb-2">
                  {{ formData.custom_data.groom_name || 'Novio' }} & {{ formData.custom_data.bride_name || 'Novia' }}
                </h2>
                <p class="text-gray-600 text-lg mb-4">¡Se casan!</p>
                
                <div class="border-t border-b border-brand-gold/20 py-4 my-4">
                  <p class="text-brand-navy font-semibold mb-1">📅 Fecha</p>
                  <p class="text-gray-700">{{ formData.custom_data.event_date || 'Por definir' }}</p>
                </div>

                <div class="mb-4">
                  <p class="text-brand-navy font-semibold mb-1">📍 Lugar</p>
                  <p class="text-gray-700">{{ formData.custom_data.venue || 'Por definir' }}</p>
                </div>

                <div v-if="formData.custom_data.message" class="bg-gray-50 p-4 rounded-lg mb-4">
                  <p class="text-gray-700 italic">"{{ formData.custom_data.message }}"</p>
                </div>

                <div v-if="formData.custom_data.dress_code" class="mb-4">
                  <p class="text-brand-navy font-semibold mb-1">👔 Dress Code</p>
                  <p class="text-gray-700 capitalize">{{ formData.custom_data.dress_code }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useInvitationStore } from '../stores/invitation'

const router = useRouter()
const invitationStore = useInvitationStore()

const step = ref('event') // 'event', 'template', 'customize'
const templates = ref([])
const loading = ref(false)
const error = ref('')

const formData = reactive({
  event_type: '',
  template_id: '',
  custom_data: {
    groom_name: '',
    bride_name: '',
    event_date: '',
    venue: '',
    message: '',
    dress_code: ''
  }
})

onMounted(async () => {
  // Check if there's a saved invitation in progress
  invitationStore.loadCurrentInvitation()
  if (invitationStore.currentInvitation) {
    formData.event_type = invitationStore.currentInvitation.event_type
    formData.template_id = invitationStore.currentInvitation.template_id
    formData.custom_data = { ...invitationStore.currentInvitation.custom_data }
    step.value = 'customize'
  }
})

const selectEvent = async (eventType) => {
  formData.event_type = eventType
  loading.value = true
  try {
    templates.value = await invitationStore.fetchTemplates(eventType)
    step.value = 'template'
  } catch (err) {
    error.value = 'Error al cargar plantillas'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const selectTemplate = (templateId) => {
  formData.template_id = templateId
  step.value = 'customize'
}

const saveInvitation = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Save to localStorage temporarily (user not authenticated yet)
    localStorage.setItem('pending_invitation', JSON.stringify(formData))
    
    // Move to authentication step
    router.push('/onboarding/step2')
  } catch (err) {
    error.value = 'Error al guardar la invitación'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>
