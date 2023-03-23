// @ts-nocheck
import Vue from 'vue'
import Router from 'vue-router'


import Homepage from '../components/Homepage'
import SearchResult from '../components/SearchResult'
import Detail from '../components/Detail.vue'
import Test from '../components/Test.vue'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Homepage',
      component: Homepage,
      meta: {
        keepAlive: false //此页面需要缓存
      }
    },
    {
      path: '/result',
      name: 'SearchResult',
      component: SearchResult,
      meta: {
        keepAlive: true //此页面需要缓存
      }
    },
    {
      path: '/detail',
      name: 'Detail',
      component: Detail,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/test',
      name: 'Test',
      component: Test
    },
  ]
})
