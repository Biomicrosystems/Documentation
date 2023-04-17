<template>
  <section class="hero is-fullheight">
    <div class="hero-head">
      <div class="header">
        <h1 class="header__title">Pawl <span>UI</span></h1>
      </div>
    </div>
    <div class="hero-body">
      <form class="signup" @submit.prevent="submitForm">
        <div class="signup__header">
          <h2 class="signup__title">Create your account</h2>
          <p class="has-text-grey-light">Enter the fields below to get started</p>
        </div>
        <div class="field mb-6">
          <label class="label is-large">Full name*</label>
          <div class="control">
            <input
                class="input is-large"
                type="text"
                placeholder="Full name"
                maxlength="50"
                autocomplete="name"
                v-model.trim="fullName">
          </div>
        </div>
        <div class="field mb-6">
          <label class="label is-large">Email address*</label>
          <div class="control">
            <input
                class="input is-large"
                type="email"
                placeholder="Email"
                maxlength="50"
                autocomplete="username"
                v-model.trim="email">
          </div>
        </div>
        <div class="field mb-6">
          <label class="label is-large">Password*</label>
          <div class="control">
            <input
                class="input is-large"
                type="password"
                placeholder="Password"
                maxlength="15"
                autocomplete="new-password"
                v-model.trim="password">
          </div>
        </div>
        <div class="signup__validation-error" v-if="formIsValid">
          <p v-for="error in submitFormErrors" :key="error">{{ error }}</p>
        </div>
        <div class="signup__validation-error" v-if="errorOnSubmit">
          <p>{{ signupError }}</p>
        </div>
        <div class="field mb-6">
          <div class="control">
            <button class="button is-primary is-large is-fullwidth is-rounded">Sign up</button>
          </div>
        </div>
        <div class="signup__signup">
          <p>Already have an account? <span><router-link to="/login">Log in</router-link></span></p>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import {computed, ref} from 'vue'
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'

const store = useStore()
const router = useRouter()

const fullName = ref('')
const email = ref('')
const password = ref('')
const submitFormErrors = ref([])
const signupError = ref('')

const errorOnSubmit = computed(() => signupError.value !== '')

const submitForm = async () => {

  try {

    if (formIsValid()) {
      await store.dispatch('signUp', {fullName: fullName.value, email: email.value, password: password.value})
    }

    if (store.getters.getIsUserSignUp) {

      store.commit('setIsUserSignUp', false)
      await router.push('/signup-success')
    }

  } catch (error) {

    const errorMessage = error.response.data.errorMessage

    if (errorMessage.includes('duplicate key error')) {

      signupError.value = 'Email already exists'

    } else {

      signupError.value = `Something went wrong, please try again: ${errorMessage}`

    }
  }
}

const formIsValid = () => {

  submitFormErrors.value = []

  if (fullName.value.length < 3) {
    submitFormErrors.value.push('Full name must be at least 3 characters long')
  }
  if (email.value.length < 5) {
    submitFormErrors.value.push('Email must be at least 5 characters long')
  }
  if (password.value.length < 8) {
    submitFormErrors.value.push('Password must be at least 8 characters long')
  }

  return submitFormErrors.value.length === 0
}
</script>
