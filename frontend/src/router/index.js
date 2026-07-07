import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import CustomersView from '../views/CustomersView.vue'
import PoliciesView from '../views/PoliciesView.vue'
import ClaimsView from '../views/ClaimsView.vue'

const routes = [
  { path: '/', name: 'dashboard', component: DashboardView },
  { path: '/musteriler', name: 'customers', component: CustomersView },
  { path: '/policeler', name: 'policies', component: PoliciesView },
  { path: '/hasarlar', name: 'claims', component: ClaimsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
