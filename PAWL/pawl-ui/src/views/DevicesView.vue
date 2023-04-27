<template>
  <section>
    <div class="container">
      <div class="device-registration-title pb-6">
        <h1 class="has-text-centered">Register A New Device</h1>
      </div>
      <div>
        <div class="notification is-danger is-light" v-if="globalErrorMessage">
          <button class="delete" @click="acknowledgeError"></button>
          <h1 class="subtitle has-text-centered">{{ globalErrorMessage }}</h1>
        </div>
        <div class="field has-addons">
          <div class="control is-expanded">
            <input class="input is-primary" type="text" placeholder="enter device id" v-model.trim="deviceId">
          </div>
          <div class="control">
            <a class="button is-primary" @click="registerDevice">
              Register Device
            </a>
          </div>
        </div>
        <div class="table-container">
          <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
            <thead>
            <tr>
              <th><p class="title">ID</p></th>
              <th><p class="title">Device ID</p></th>
              <th><p class="title">Status</p></th>
              <th><p class="title">Actions</p></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="device in registeredDevices" :key="device._id">
              <td><p>{{ device._id }}</p></td>
              <td><p>{{ device.deviceId }}</p></td>
              <td><p>{{ device.name }}</p></td>
              <td>
                <button class="button is-danger is-rounded is-fullwidth" @click="deleteDevice(device._id)">Delete
                </button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>

import {ref, onMounted, computed} from "vue";
import {useStore} from "vuex";

const store = useStore();

const deviceId = ref("");

const registerDevice = () => {
  acknowledgeError();
  store.dispatch("registerDevice", {
    deviceId: deviceId.value,
    identifier: deviceId.value
  });
  deviceId.value = "";
}

onMounted(async () => {
  await store.dispatch("getRegisteredDevices");
});

const registeredDevices = computed(() => store.getters.getRegisteredDevices);

const globalErrorMessage = computed(() => store.getters.getGlobalError);

const acknowledgeError = async () => {
  await store.dispatch("acknowledgeGlobalError");
}

const deleteDevice = async (_id) => {
  await store.dispatch("deleteDevice", _id);
}

</script>

