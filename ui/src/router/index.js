import { createRouter, createWebHistory } from 'vue-router'
import ShiftPlanList from '../components/ShiftPlanList.vue'
import CrewAssignments from '../components/CrewAssignments.vue'

const routes = [
  {
    path: '/',
    name: 'shifts',
    component: ShiftPlanList
  },
  {
    path: '/crew',
    name: 'crew',
    component: CrewAssignments
  },
  // Add a catch-all redirect to home
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
