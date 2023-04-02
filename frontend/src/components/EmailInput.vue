<template>
    <div>
      <label for="email">Email:</label>
      <input
        id="email"
        v-model="email"
        type="email"
        @input="validateEmail"
        :class="{ 'is-invalid': isInvalidEmail }"
      />
      <span v-if="isInvalidEmail" class="error-message">Invalid email address</span>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    setup() {
      const email = ref('');
      const isInvalidEmail = ref(false);
  
      const validateEmail = () => {
        const emailPattern = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
        isInvalidEmail.value = !emailPattern.test(email.value);
      };
  
      return {
        email,
        isInvalidEmail,
        validateEmail,
      };
    },
  });
  </script>
  
  <style scoped>
  .is-invalid {
    border-color: red;
  }
  
  .error-message {
    color: red;
    font-size: 0.8rem;
  }
  </style>