<template>
  <router-view></router-view>
</template>

<style lang="scss">
@use '~@/styles/main.scss';
</style>

<script setup>

import {onMounted} from "vue";
import {useStore} from "vuex";

onMounted(() => {
  const store = useStore()
  store.dispatch("autoLogIn")
})

</script>
