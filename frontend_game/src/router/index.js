import { createRouter, createWebHistory } from 'vue-router'
import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/LoginPage";
import InventoryPage from "@/pages/InventoryPage";
import ShopPage from "@/pages/ShopPage";

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
  },
  {
    path: '/inventory',
    name: 'inventory',
    component: InventoryPage
  },
  {
    path: '/shop',
    name: 'shop',
    component: ShopPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
