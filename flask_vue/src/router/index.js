// 该文件专门用于创建整个应用的路由器
import VueRouter from 'vue-router'

//创建并暴露一个路由器
const router =  new VueRouter({
	routes:[
		{
			path:'/',
			name:'Form',
			component:() => import('../components/Form.vue'),
		},
		{
			path:'/Home',
			name:'Home',
			component:() => import('../components/Home.vue'),
		},
	]
})

export default router
