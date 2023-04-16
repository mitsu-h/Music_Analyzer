<!-- src/components/AuthSwitcher.vue -->
<template>
    <div>
      <!-- <button @click="showLogin">Login</button> -->
      <!-- <button @click="showSignup">Sign Up</button> -->
  
      <component :is="currentComponent"></component>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import Login from "../components/Login.vue";
  import Signup from "../components/Signup.vue";
  
  export default {
    components: {
      Login,
      Signup,
    },
    setup() {
      const currentComponent = ref("Login");
  
      function showLogin() {
        currentComponent.value = "Login";
      }
  
      function showSignup() {
        currentComponent.value = "Signup";
      }
  
      return {
        currentComponent,
        showLogin,
        showSignup,
      };
    },
  };
  </script>
  