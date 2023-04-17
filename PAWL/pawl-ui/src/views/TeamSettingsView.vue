<template>
  <section>
    <div class="container">
      <div class="pb-6">
        <h1 class="has-text-centered">Team Settings</h1>
      </div>
      <div>
        <div class="table-container">
          <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
            <thead>
            <tr>
              <th><p class="title">ID</p></th>
              <th><p class="title">Name ID</p></th>
              <th><p class="title">Email</p></th>
              <th><p class="title">Verified</p></th>
              <th><p class="title">Actions</p></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="user in users" :key="user._id">
              <td><p>{{ user._id }}</p></td>
              <td><p>{{ user.full_name }}</p></td>
              <td><p>{{ user.email }}</p></td>
              <td><p>{{ user.verified }}</p></td>
              <td>
                <div class="field is-grouped is-grouped-centered">
                  <p class="control">
                    <a class="button" :class=" user.verified ? 'is-warning' : 'is-success'" @click="verifyOrUnverifyUser(user._id)">
                      {{ user.verified ? 'Unverify' : 'Verify' }}
                    </a>
                  </p>
                  <p class="control">
                    <a class="button is-danger" @click="deleteUser(user._id)">
                      Delete
                    </a>
                  </p>
                </div>
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
import {onMounted, computed} from "vue";
import {useStore} from "vuex";

const store = useStore();

const deleteUser = (id) => {
  store.dispatch("deleteUser", id);
}

onMounted(() => {
  store.dispatch("getUsers");
})

const users = computed(() => store.getters.getUsers);

const verifyOrUnverifyUser = (id) => {
  store.dispatch("verifyUser", {
    id: id,
    verified: !users.value.find(user => user._id === id).verified
  });
}



</script>

