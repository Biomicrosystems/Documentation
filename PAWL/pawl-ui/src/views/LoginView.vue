<template>
  <section class="hero is-fullheight">
    <div class="hero-head">
      <div class="header">
        <h1 class="header__title">Pawl <span>UI</span></h1>
      </div>
    </div>
    <div class="hero-body">
      <form class="login" @submit.prevent="login">
        <div class="login__header">
          <h2 class="login__title">Welcome back</h2>
          <p class="has-text-grey-light">Please login to your account</p>
        </div>
        <div class="field mb-6">
          <label class="label is-large">Email</label>
          <div class="control">
            <input class="input is-large"
                   type="email"
                   placeholder="Email"
                   maxlength="50"
                   autocomplete="username"
                   v-model.trim="email"
            >
          </div>
        </div>
        <div class="field mb-6">
          <label class="label is-large">Password</label>
          <div class="control">
            <input class="input is-large"
                   type="password"
                   placeholder="Password"
                   maxlength="15"
                   minlength="8"
                   autocomplete="new-password"
                   v-model.trim="password"
            >
          </div>
        </div>
        <div class="signup__validation-error" v-if="loginFormIsValid">
          <p v-for="error in loginFormErrors" :key="error">{{ error }}</p>
        </div>
        <div class="login__validation-error" v-if="errorOnLogin">
          <p>{{ loginError }}</p>
        </div>
        <div class="field mb-6">
          <div class="control">
            <button class="button is-primary is-large is-fullwidth is-rounded">Login</button>
          </div>
        </div>
        <div class="login__signup">
          <p>Don't have an account? <span><router-link to="/signup">Sign up</router-link></span></p>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import {ref, computed} from 'vue'
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'

const store = useStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const loginFormErrors = ref([])
const loginError = ref('')

const errorOnLogin = computed(() => loginError.value !== '')

const login = async () => {

  try {
    if (loginFormIsValid()) {

      await store.dispatch('logIn', {
        email: email.value,
        password: password.value
      })

      await router.push('/dashboard')
    }
  } catch (error) {
    loginError.value = 'Invalid email or password, please try again'
  }


}

const loginFormIsValid = () => {

  loginFormErrors.value = []

  if (email.value.length < 5) {
    loginFormErrors.value.push('Email must be at least 5 characters long')
  }
  if (password.value.length < 8) {
    loginFormErrors.value.push('Password must be at least 8 characters long')
  }

  return loginFormErrors.value.length === 0
}


</script>

