import { describe, it, expect } from 'vitest';

import { mount } from '@vue/test-utils'
import EmailInput from '../EmailInput.vue';

describe('EmailInput', () => {
  it('renders an email input', () => {
    const wrapper = mount(EmailInput);
    const input = wrapper.find('input[type="email"]');
    expect(input.exists()).toBe(true);
  });

  it('updates the email data when the input value changes', async () => {
    const wrapper = mount(EmailInput);
    const input = wrapper.find('input[type="email"]');

    // 有効なメールアドレスを入力
    await input.setValue('test@example.com');
    expect(wrapper.find('input[type="email"]').element.value).toBe('test@example.com');
    expect(wrapper.find('.error-message').exists()).toBe(false);
    

    // 無効なメールアドレスを入力
    await input.setValue('invalid-email');
    expect(wrapper.find('input[type="email"]').element.value).toBe('invalid-email');
    expect(wrapper.find('.error-message').exists()).toBe(true);
  });
});
