<template>
  <v-main>
    <h1>Login</h1>
    <form @submit.prevent="submitLogin">
      <EmailInput v-model="email" />
      <PasswordInput v-model="password" />
      <button type="submit">Login</button>
      <span v-if="errorOccurred" class="error-message">Email or password is incorrect</span>
    </form>
  </v-main>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
// import { useStore } from "pinia";
import { useRouter } from "vue-router";
import EmailInput from './EmailInput.vue';
import PasswordInput from './PasswordInput.vue';
import { useAuthStore } from "@/stores/auth";

export default defineComponent({
  components: {
    EmailInput,
    PasswordInput,
  },
  setup() {
    const email = ref('');
    const password = ref('');
    const store = useAuthStore();
    const router = useRouter();
    const errorOccurred = ref(false);

    const submitLogin = async () => {
      try {
        await store.login({ email: email.value, password: password.value });
        // ログイン成功後、ホーム画面に遷移
        router.push({ name: "home" });
      } catch (error) {
        // Set errorOccurred to true to show the error message in the UI
        errorOccurred.value = true;
      }
    };

    return {
      email,
      password,
      errorOccurred,
      submitLogin,
    };
  },
});
</script>

<style scoped>
.error-message {
  color: red;
  font-size: 0.8rem;
}
</style>
