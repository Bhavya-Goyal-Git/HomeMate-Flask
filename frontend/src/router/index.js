import { createRouter, createWebHistory } from 'vue-router'
import HomeComponent from "../views/Homeview.vue"
import SignUpComponent from "../views/SignUp.vue"
import LoginComponent from "../views/Loginview.vue"
import CustomerData from "../views/UserViews/CustomerData.vue"
import WorkerData from "../views/WorkerViews/WorkerData.vue"
import CustomerHome from "../views/UserViews/CustomerHome.vue"
import CustomerStats from "../views/UserViews/CustomerStats.vue"
import WorkerHome from "../views/WorkerViews/WorkerHome.vue"
import WorkerStats from "../views/WorkerViews/WorkerStats.vue"
import AdminHome from "../views/AdminViews/AdminHome.vue"
import AdminStats from "../views/AdminViews/AdminStats.vue"
import FlagUsers from "../views/AdminViews/FlagUsers.vue"
import { useUserStore } from '@/stores/userstore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "homepage",
      component: HomeComponent,
    },
    {
      path: "/register",
      name: "signup",
      component: SignUpComponent,
    },
    {
      path: "/login",
      name: "login",
      component: LoginComponent,
    },
    {
      path: "/customer/data",
      name: "userdata",
      component: CustomerData,
      beforeEnter: customerAuth,
    },
    {
      path: "/professional/data",
      name: "workerdata",
      component: WorkerData,
      beforeEnter: workerAuth,
    },
    {
      path: "/customer/home",
      name: "customerHome",
      component: CustomerHome,
      beforeEnter: customerAuth,
    },
    {
      path: "/professional/home",
      name: "workerHome",
      component: WorkerHome,
      beforeEnter: workerAuth,
    },
    {
      path: "/admin/home",
      name: "adminHome",
      component: AdminHome,
      beforeEnter: adminAuth,
    },
    {
      path: "/admin/users",
      name: "adminFlagUsers",
      component: FlagUsers,
      beforeEnter: adminAuth,
    },
    {
      path: "/admin/stats",
      name: "adminStats",
      component: AdminStats,
      beforeEnter: adminAuth,
    },
    {
      path: "/customer/stats",
      name: "customerStats",
      component: CustomerStats,
      // beforeEnter: customerAuth,
    },
    {
      path: "/worker/stats",
      name: "workerStats",
      component: WorkerStats,
      beforeEnter: workerAuth,
    },
  ]
})

function customerAuth(to, from) {
  const userStore = useUserStore();
  if (userStore.is_loggedIn && userStore.role == "customer") return true;
  return false
}
function workerAuth(to, from) {
  const userStore = useUserStore();
  if (userStore.is_loggedIn && userStore.role == "professional") return true;
  return false

}
function adminAuth(to, from) {
  const userStore = useUserStore();
  if (userStore.is_loggedIn && userStore.role == "admin") return true;
  return false
}

export default router
