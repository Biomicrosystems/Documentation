<template>
  <section class="container is-fluid">
    <div class="chart-header">
      <nav class="level">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Start Point (V)</p>
            <input
              class="input_"
              id="Start_Point"
              type="number"
              value="0.000"
              step="0.001"
            />
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">First Vertex (V)</p>
            <input
              class="input_"
              id="First_Vertex"
              type="number"
              value="0.700"
              step="0.001"
            />
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Second Vertex (V)</p>
            <input
              class="input_"
              id="Second_Vertex"
              type="number"
              value="-0.700"
              step="0.001"
            />
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Zero Crosses</p>
            <input
              class="input_"
              id="Zero_Crosses"
              type="number"
              value="4"
              step="1"
            />
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Scan Rate (V/S)</p>
            <input
              class="input_"
              id="Scan_Rate"
              type="number"
              value="0.050"
              step="0.001"
            />
          </div>
        </div>
      </nav>
    </div>

    <div class="chart-graph">
      <div class="columns">
        <div class="column">
          <the-scatter-component v-if="loaded"></the-scatter-component>
          <div class="modal" :class="{ 'is-active': isMeasurementStarted }">
            <div class="modal-background"></div>
            <div class="modal-content">
              <div>
                <h1 class="title is-1 has-text-centered has-text-white-bis">
                  Getting data from device
                </h1>
                <h2 class="subtitle is-3 has-text-centered has-text-white-bis">
                  Please wait...
                </h2>
                <progress
                  class="progress is-large is-primary"
                  max="100"
                ></progress>
                <button
                  class="button is-danger is-large is-fullwidth"
                  @click="stopMeasurement"
                >
                  Stop measurement
                </button>
              </div>
            </div>
          </div>
          <div class="active-device" v-if="!isMeasurementStarted && !loaded">
            <div class="active-device__item">
              <div class="active-device__image">
                <div class="active-device__description p-6">
                  <h2 class="has-text-centered">Potentiostat</h2>
                  <h4 class="has-text-centered">
                    Device ID: {{ selectedDevice }}
                  </h4>
                </div>
                <img src="../assets/microcontroller.png" alt="" />
                <h6 class="has-text-right">Image: https://www.flaticon.com/</h6>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-one-fifth">
          <div class="chart-control">
            <div
              class="notification is-danger is-light"
              v-if="validationErrorMessage"
            >
              <button class="delete" @click="acknowledgeError"></button>
              <h1 class="subtitle has-text-centered">
                {{ validationErrorMessage }}
              </h1>
            </div>
            <div class="field">
              <label class="label">Sample name</label>
              <div class="control">
                <input
                  class="input is-rounded is-primary"
                  type="text"
                  placeholder="Enter sample name"
                  v-model.trim="identifier"
                />
              </div>
            </div>
            <div class="buttons">
              <button
                class="button is-primary is-rounded is-fullwidth"
                :disabled="loaded"
                @click="startMeasurement"
              >
                Start
              </button>
              <button
                class="button is-rounded is-fullwidth"
                @click="reloadChart"
              >
                Clear Chart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="chart-logo">
      <img
        src="https://raw.githubusercontent.com/Biomicrosystems/Documentation/main/Logos/BiomicrosystemsLogo.png"
        class="chart-logo--image"
        alt="Logo"
      />
    </div>
  </section>
</template>

<script setup>
import TheScatterComponent from "@/components/TheScatterComponent";
import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();
const loaded = ref(false);
const identifier = ref("");
const validationErrorMessage = ref("");

const startMeasurement = async () => {
  loaded.value = false;
  validationErrorMessage.value = "";

  if (identifier.value === "") {
    validationErrorMessage.value = "Please enter a sample name";
    return;
  }

  await store.dispatch("isSampleNameUsedForDevice", {
    deviceId: selectedDevice.value,
    identifier: identifier.value,
  });

  if (store.getters.getIsSampleNameUsedForDevice) {
    validationErrorMessage.value = "Sample name already used for this device";
    return;
  }

  await store.dispatch("startMeasurement", {
    deviceId: selectedDevice.value,
    identifier: identifier.value,
  });

  if (store.getters.getLoadedChart) {
    loaded.value = true;
  }
};

const isMeasurementStarted = computed(() => {
  return store.getters.getMeasurementStarted;
});

const stopMeasurement = () => {
  store.dispatch("stopMeasurement", {
    deviceId: selectedDevice.value,
    identifier: identifier.value,
  });
};

const reloadChart = () => {
  loaded.value = false;
  identifier.value = "";
  validationErrorMessage.value = "";
};

const selectedDevice = computed(() => {
  return store.getters.getSelectedDevice;
});

onMounted(() => {
  if (store.getters.getSelectedDevice === null) {
    router.push("/dashboard");
  }
});

const acknowledgeError = () => {
  validationErrorMessage.value = "";
};
</script>
