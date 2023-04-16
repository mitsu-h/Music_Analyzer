<!-- PasswordInput.vue -->
<template>
    <div>
      <label for="password">Password:</label>
      <input
        id="password"
        :value="modelValue"
        @input="inputChange"
        type="password"
      />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    props: {
      modelValue: {
        type: String,
        default: '',
      },
    },
    setup(props, { emit }) {
      const inputChange = (event) => {
        emit('update:modelValue', event.target.value);
      };
  
      return {
        inputChange,
      };
    },
  });
  </script>
  