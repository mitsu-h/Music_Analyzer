<template>
  <div>
    <label for="email">Email:</label>
    <input
      id="email"
      :value="modelValue"
      @input="updateEmail"
      type="email"
      :class="{ 'is-invalid': isInvalidEmail }"
    />
    <span v-if="isInvalidEmail" class="error-message">Invalid email address</span>
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
    const isInvalidEmail = ref(false);

    const updateEmail = (event) => {
      const newEmail = event.target.value;
      const emailPattern = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
      isInvalidEmail.value = !emailPattern.test(newEmail);
      emit('update:modelValue', newEmail);
    };

    return {
      isInvalidEmail,
      updateEmail,
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
