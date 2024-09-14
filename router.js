
import Login from './view/Login.vue'
import studentdata from './view/studentdata.vue'
import teacherdata from './view/teacherdata.vue'
const routers=[
    {path:'/',component:Login},
    {path:'/login',component: Login},
    {path:'/students',component:studentdata},
    {path:'/teachers',component:teacherdata}
]
export default routers