import { createRouter, createWebHistory } from 'vue-router'
import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/LoginPage";
import InventoryPage from "@/pages/InventoryPage";
import ShopPage from "@/pages/ShopPage";
import BattlePage from "@/pages/BattlePage";
import SignUpPage from "@/pages/SignUpPage";
import WelcomePage from "@/pages/WelcomePage";

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: WelcomePage
  },
  {
    path: '/home',
    name: 'home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpPage
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
