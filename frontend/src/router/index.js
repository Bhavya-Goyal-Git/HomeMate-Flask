import { createRouter, createWebHistory } from 'vue-router'
import HomeComponent from "../views/Homeview.vue"
import SignUpComponent from "../views/SignUp.vue"
import LoginComponent from "../views/Loginview.vue"
import CustomerData from "../views/UserViews/CustomerData.vue"
import WorkerData from "../views/WorkerViews/WorkerData.vue"
import CustomerHome from "../views/UserViews/CustomerHome.vue"
import WorkerHome from "../views/WorkerViews/WorkerHome.vue"
import AdminHome from "../views/AdminViews/AdminHome.vue"

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
    },
    {
      path: "/professional/data",
      name: "workerdata",
      component: WorkerData,
    },
    {
      path: "/customer/home",
      name: "customerHome",
      component: CustomerHome,
    },
    {
      path: "/professional/home",
      name: "workerHome",
      component: WorkerHome,
    },
    {
      path: "/admin/home",
      name: "adminHome",
      component: AdminHome,
    }
  ]
})

export default router
