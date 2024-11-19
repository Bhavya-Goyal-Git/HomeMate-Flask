import { createRouter, createWebHistory } from 'vue-router'
import HomeComponent from "../views/Homeview.vue"
import SignUpComponent from "../views/SignUp.vue"
import LoginComponent from "../views/Loginview.vue"

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
    }
  ]
})

export default router
