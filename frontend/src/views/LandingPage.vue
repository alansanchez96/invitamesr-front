<template>
  <div class="landing-page bg-gradient-to-b from-brand-navy to-gray-900 min-h-screen">
    <!-- Hero Section -->
    <section class="hero min-h-screen flex items-center justify-center relative overflow-hidden">
      <!-- Decorative background -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-20 left-10 w-72 h-72 bg-brand-gold rounded-full blur-3xl"></div>
        <div class="absolute bottom-20 right-10 w-96 h-96 bg-brand-silver rounded-full blur-3xl"></div>
      </div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center">
          <!-- Logo -->
          <div class="mb-8 flex justify-center">
            <img 
              :src="logoUrl" 
              alt="INVITAME SR Logo" 
              class="h-48 w-auto animate-fade-in"
            />
          </div>

          <!-- Headline -->
          <h1 class="text-6xl md:text-7xl font-elegant text-white mb-6 animate-slide-up">
            Invitaciones Digitales
            <span class="block text-brand-gold mt-2">de Lujo</span>
          </h1>

          <p class="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto animate-slide-up-delay">
            Crea invitaciones elegantes y memorables para tus eventos más especiales.
            Diseño profesional, personalización completa, experiencia única.
          </p>

          <!-- CTA Button -->
          <button 
            @click="startOnboarding"
            class="btn-primary text-lg px-12 py-4 shadow-2xl hover:shadow-brand-gold/50 animate-bounce-soft"
            data-testid="cta-crear-invitacion"
          >
            Crear Mi Invitación 💍
          </button>

          <!-- Stats -->
          <div class="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            <div class="text-center">
              <div class="text-4xl font-bold text-brand-gold">100+</div>
              <div class="text-gray-400 mt-2">Eventos Creados</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold text-brand-gold">95%</div>
              <div class="text-gray-400 mt-2">Satisfacción</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold text-brand-gold">24/7</div>
              <div class="text-gray-400 mt-2">Soporte</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
        </svg>
      </div>
    </section>

    <!-- Events Section -->
    <section class="py-20 bg-white" id="eventos">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-5xl font-elegant text-brand-navy mb-4">
            Eventos Especiales
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Creamos invitaciones personalizadas para tus momentos más importantes
          </p>
        </div>

        <div class="max-w-4xl mx-auto">
          <!-- Boda Card -->
          <div class="card hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
            <div class="flex items-center gap-6">
              <div class="text-7xl">💍</div>
              <div class="flex-1">
                <h3 class="text-3xl font-elegant text-brand-navy mb-2">Bodas</h3>
                <p class="text-gray-600 text-lg mb-4">
                  Invitaciones elegantes para tu día más especial. Diseños únicos que reflejan 
                  el amor y la elegancia de tu celebración.
                </p>
                <ul class="space-y-2">
                  <li class="flex items-center text-gray-700">
                    <svg class="w-5 h-5 text-brand-gold mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    Personalización completa de diseño
                  </li>
                  <li class="flex items-center text-gray-700">
                    <svg class="w-5 h-5 text-brand-gold mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    Múltiples plantillas elegantes
                  </li>
                  <li class="flex items-center text-gray-700">
                    <svg class="w-5 h-5 text-brand-gold mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    Vista previa en tiempo real
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Coming Soon -->
          <div class="mt-8 text-center text-gray-500">
            <p class="text-lg">Próximamente: XV Años, Cumpleaños, y más... 🎉</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section class="py-20 bg-gray-50" id="planes">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-5xl font-elegant text-brand-navy mb-4">
            Planes y Precios
          </h2>
          <p class="text-xl text-gray-600">
            Elige el plan perfecto para tu evento
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Basic Plan -->
          <div class="card hover:shadow-2xl transition-all duration-300 transform hover:scale-105" data-testid="plan-basic">
            <div class="text-center">
              <div class="inline-block p-3 bg-gray-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-brand-navy" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-elegant text-brand-navy mb-2">Basic</h3>
              <div class="text-4xl font-bold text-brand-navy mb-2">
                $2,500
                <span class="text-lg text-gray-600 font-normal">ARS</span>
              </div>
              <p class="text-gray-600 mb-6">Pago único</p>
              
              <ul class="space-y-3 text-left mb-8">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">1 Plantilla personalizable</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Hasta 50 invitados</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Soporte por email</span>
                </li>
              </ul>

              <button 
                @click="startOnboarding"
                class="w-full px-6 py-3 border-2 border-brand-navy text-brand-navy font-semibold rounded-lg hover:bg-brand-navy hover:text-white transition-all duration-300"
              >
                Comenzar
              </button>
            </div>
          </div>

          <!-- PRO Plan - Featured -->
          <div class="card hover:shadow-2xl transition-all duration-300 transform hover:scale-105 border-2 border-brand-gold relative" data-testid="plan-pro">
            <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span class="bg-brand-gold text-white px-4 py-1 rounded-full text-sm font-semibold">
                MÁS POPULAR
              </span>
            </div>
            
            <div class="text-center">
              <div class="inline-block p-3 bg-brand-gold/10 rounded-full mb-4">
                <svg class="w-8 h-8 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-elegant text-brand-navy mb-2">PRO</h3>
              <div class="text-4xl font-bold text-brand-gold mb-2">
                $5,000
                <span class="text-lg text-gray-600 font-normal">ARS</span>
              </div>
              <p class="text-gray-600 mb-6">Pago único</p>
              
              <ul class="space-y-3 text-left mb-8">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Todas las plantillas</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Invitados ilimitados</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Personalización avanzada</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Soporte prioritario</span>
                </li>
              </ul>

              <button 
                @click="startOnboarding"
                class="w-full btn-secondary"
              >
                Comenzar
              </button>
            </div>
          </div>

          <!-- Planner Plan -->
          <div class="card hover:shadow-2xl transition-all duration-300 transform hover:scale-105" data-testid="plan-planner">
            <div class="text-center">
              <div class="inline-block p-3 bg-purple-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-elegant text-brand-navy mb-2">Planner</h3>
              <div class="text-4xl font-bold text-purple-600 mb-2">
                $1,500
                <span class="text-lg text-gray-600 font-normal">ARS</span>
              </div>
              <p class="text-gray-600 mb-6">Por mes</p>
              
              <ul class="space-y-3 text-left mb-8">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">3 eventos por mes</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Todas las plantillas</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Análisis de invitados</span>
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-brand-gold mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">Soporte 24/7</span>
                </li>
              </ul>

              <button 
                @click="startOnboarding"
                class="w-full px-6 py-3 border-2 border-purple-600 text-purple-600 font-semibold rounded-lg hover:bg-purple-600 hover:text-white transition-all duration-300"
              >
                Comenzar
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-brand-navy to-brand-gold">
      <div class="container mx-auto px-6 text-center">
        <h2 class="text-5xl font-elegant text-white mb-6">
          ¿Listo para crear tu invitación?
        </h2>
        <p class="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
          Comienza ahora y sorprende a tus invitados con una invitación digital única y elegante
        </p>
        <button 
          @click="startOnboarding"
          class="bg-white text-brand-navy px-12 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 shadow-2xl"
        >
          Crear Mi Invitación Ahora
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-brand-navy text-white py-12">
      <div class="container mx-auto px-6">
        <div class="grid md:grid-cols-3 gap-8">
          <div>
            <h3 class="text-xl font-elegant mb-4">INVITAME SR</h3>
            <p class="text-gray-400">
              Invitaciones digitales de lujo para tus eventos más especiales
            </p>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Enlaces</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#eventos" class="hover:text-brand-gold transition-colors">Eventos</a></li>
              <li><a href="#planes" class="hover:text-brand-gold transition-colors">Planes</a></li>
              <li><a href="#" class="hover:text-brand-gold transition-colors">Contacto</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Contacto</h4>
            <ul class="space-y-2 text-gray-400">
              <li>📧 info@invitamesr.com</li>
              <li>📱 +54 11 1234-5678</li>
              <li>📍 Buenos Aires, Argentina</li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 INVITAME SR. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const logoUrl = ref(import.meta.env.VITE_LOGO_URL)

const startOnboarding = () => {
  router.push('/onboarding/step1')
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce-soft {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.8s ease-out;
}

.animate-slide-up-delay {
  animation: slide-up 0.8s ease-out 0.2s both;
}

.animate-bounce-soft {
  animation: bounce-soft 2s ease-in-out infinite;
}
</style>
