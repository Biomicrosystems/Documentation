import {createRouter, createWebHistory} from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import SignUpSuccessView from '../views/SignUpSuccessView.vue'
import DashboardView from '../views/DashboardView.vue'
import ChartView from '../views/ChartView.vue'
import DevicesView from '../views/DevicesView.vue'
import TeamSettingsView from '../views/TeamSettingsView.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: '/signup',
        name: 'signup',
        component: SignUpView
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView,
        children: [
            {
                path: 'chart',
                name: 'chart',
                component: ChartView
            },
            {
                path: 'register-device',
                name: 'register-device',
                component: DevicesView
            },
            {
                path: 'team-settings',
                name: 'team-settings',
                component: TeamSettingsView
            }
        ],
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/signup-success',
        name: 'signup-success',
        component: SignUpSuccessView
    },
    {
        path: '/:notFound(.*)',
        component: NotFoundView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        if (localStorage.getItem('accessToken')) {
            next()
        } else {
            next('/login')
        }
    } else if (to.name === 'login' && localStorage.getItem('accessToken')) {
        next('/dashboard')
    } else {
        next()
    }

})

export default router
