//import './assets/main.css'
import axios from "axios";
import { createApp } from 'vue'
import App from './App.vue'
import ViewUIPlus from 'view-ui-plus'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import * as VueRouter from "vue-router"
import routers from './router.js'

const router=VueRouter.createRouter({
    history:VueRouter.createWebHashHistory(),
    routes:routers
})
const a=createApp(App)
a.config.globalProperties.$axios=axios
a.use(ViewUIPlus).use(router).mount('#app')
