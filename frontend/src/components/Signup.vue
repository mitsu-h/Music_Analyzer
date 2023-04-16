<template>
    <div>
      <h2>Sign Up</h2>
      <form @submit.prevent="submitSignup">
        <EmailInput v-model="email" />
        <PasswordInput v-model="password" />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  import axios from "axios";
  import EmailInput from "./EmailInput.vue";
  import PasswordInput from "./PasswordInput.vue";
  
  export default defineComponent({
    components: {
      EmailInput,
      PasswordInput,
    },
    setup() {
      const email = ref("");
      const password = ref("");
  
      const submitSignup = async () => {
        try {
          const response = await axios.post("http://localhost:8081/api/account/register/", {
            email: email.value,
            password: password.value,
          });
          console.log(response.data);
          // サインアップ後の処理（ログイン画面への遷移など）を追加
        } catch (error) {
          console.error("Sign up failed:", error);
        }
      };
  
      return {
        email,
        password,
        submitSignup,
      };
    },
  });
  </script>
  