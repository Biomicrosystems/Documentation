<template>
  <section>
    <div class="container is-fluid">
      <div class="columns pt-6 dashboard">
        <div class="column is-one-fifth dashboard__menu">
          <aside class="menu">
            <div class="hero-head">
              <div class="header">
                <h1 class="header__title">Pawl <span>UI</span></h1>
              </div>
            </div>
            <p class="menu-label">
              General
            </p>
            <ul class="menu-list">
              <li><router-link :class="{'is-active': routeName === 'dashboard' || routeName === 'chart'}" to="/dashboard">Dashboard</router-link></li>
            </ul>
            <p class="menu-label">
              Administration
            </p>
            <ul class="menu-list">
              <li><router-link :class="{'is-active': routeName === 'team-settings'}" to="/dashboard/team-settings">Team Settings</router-link></li>
            </ul>
            <ul class="menu-list">
              <li><router-link :class="{'is-active': routeName === 'register-device'}" to="/dashboard/register-device">Register A New Device</router-link></li>
            </ul>
            <p class="menu-label">
              Actions
            </p>
            <ul class="menu-list">
              <li><a @click="logOut">Logout</a></li>
            </ul>
          </aside>
        </div>
        <div class="column dashboard__content">

          <div class="device-container" v-if="currentRoute">
            <h1 class="has-text-centered pb-6">Registered Devices</h1>
            <div class="columns">
              <div class="column" v-for="device in registeredDevices" :key="device._id">
                <div class="registered-devices__item">
                  <div class="registered-devices__device-id pb-6">
                    <p class="title has-text-centered">Device</p>
                    <p class="subtitle has-text-centered">{{ device.deviceId }}</p>
                  </div>
                  <div class="registered-devices__device-logo">
                    <router-link to="/dashboard/chart" @click="onSelectedDevice(device.deviceId)">
                      <img src="../assets/microcontroller.png" alt="microcontroller">
                    </router-link>
                    <h6 class="has-text-right">Image: https://www.flaticon.com/</h6>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <router-view></router-view>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>

import {onMounted, computed} from "vue";
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'

const store = useStore()
const router = useRouter()

const logOut = () => {
  store.dispatch('logOut')
  router.push('/login')
}

onMounted(() => {
  store.dispatch('getRegisteredDevices')
})

const registeredDevices = computed(() => store.getters.getRegisteredDevices)

const currentRoute = computed(() => router.currentRoute.value.name === 'dashboard')

const routeName = computed(() => router.currentRoute.value.name)

const onSelectedDevice = (deviceId) => {
  store.dispatch('onSelectedDevice', {
    selectedDevice: deviceId
  })
}

</script>
