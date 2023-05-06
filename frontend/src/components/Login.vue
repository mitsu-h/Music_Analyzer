<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col sm="6" md="4">
          <v-card>
            <v-card-title>Login</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="submitLogin">
                <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  outlined
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  outlined
                  required
                ></v-text-field>
                <v-btn type="submit" color="primary">Login</v-btn>
                <v-alert v-if="errorOccurred" type="error" dense>
                  Email or password is incorrect
                </v-alert>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

export default defineComponent({
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
