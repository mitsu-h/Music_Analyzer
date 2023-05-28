import { createRouter, createWebHistory } from 'vue-router'
import AuthSwitcher from "../views/AuthSwitcher.vue";
import Home from "../views/Home.vue";
import Analysis from "../views/Analysis.vue"
import { useAuthStore } from '../stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "AuthSwitcher",
      component: AuthSwitcher,
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: {requiresAuth: true}
    },
    {
      path: '/analysis',
      name: 'Analysis',
      component: Analysis,
      meta: {requiresAuth: true}
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})
router.beforeEach((to, from, next) => {
  // `requiresAuth`がtrueに設定されているルートに対して認証を要求します。
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // ユーザーがログインしていない場合、ログインページにリダイレクトします。
    const authStore = useAuthStore()
    if (!authStore.isLoggedIn) {
      next({
        path: '/',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  } else {
    next(); // 認証が必要でない場合はそのまま次へ進みます。
  }
});


export default router
