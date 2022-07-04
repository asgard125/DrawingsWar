import { createRouter, createWebHistory } from 'vue-router'
import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/LoginPage";
import InventoryPage from "@/pages/InventoryPage";
import ShopPage from "@/pages/ShopPage";
import BattlePage from "@/pages/BattlePage";

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
  },
        {
    path: '/battle/:id',
    name: 'battle',
    component: BattlePage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
