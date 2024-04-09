import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/vulns/:id',
      name: 'vuln',
      props: true,
      component: () => import('../views/VulnView.vue')
    }
  ]
})

export default router
