import { createRouter, createWebHistory } from 'vue-router'
import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/LoginPage";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
