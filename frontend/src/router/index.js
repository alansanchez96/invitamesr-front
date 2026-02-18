import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import OnboardingStep1 from '../views/OnboardingStep1.vue'
import OnboardingStep2 from '../views/OnboardingStep2.vue'
import OnboardingStep3 from '../views/OnboardingStep3.vue'
import OnboardingSuccess from '../views/OnboardingSuccess.vue'
import AuthCallback from '../views/AuthCallback.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPage
  },
  {
    path: '/onboarding/step1',
    name: 'onboarding-step1',
    component: OnboardingStep1
  },
  {
    path: '/onboarding/step2',
    name: 'onboarding-step2',
    component: OnboardingStep2
  },
  {
    path: '/onboarding/payment',
    name: 'onboarding-payment',
    component: OnboardingStep3
  },
  {
    path: '/onboarding/success',
    name: 'onboarding-success',
    component: OnboardingSuccess
  },
  {
    path: '/auth/callback',
    name: 'auth-callback',
    component: AuthCallback
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Check for session_id in URL hash during navigation
router.beforeEach((to, from, next) => {
  // Check if URL has session_id in hash
  if (window.location.hash && window.location.hash.includes('session_id=')) {
    // Redirect to auth callback
    next({ name: 'auth-callback' })
  } else {
    next()
  }
})

export default router