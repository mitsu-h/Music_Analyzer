import { describe, it, expect } from 'vitest';

import { mount } from '@vue/test-utils'
import PasswordInput from '../PasswordInput.vue';

describe('PasswordInput', () => {
  it('renders a password input', () => {
    const wrapper = mount(PasswordInput);
    const input = wrapper.find('input[type="password"]');
    expect(input.exists()).toBe(true);
  });

  it('updates the password data when the input value changes', async () => {
    const wrapper = mount(PasswordInput);
    const input = wrapper.find('input[type="password"]');

    // パスワードを入力
    await input.setValue('mypassword');
    expect(wrapper.find('input[type="password"]').element.value).toBe('mypassword');
  });
});
