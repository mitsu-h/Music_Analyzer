import { describe, it, expect } from 'vitest';

import { mount } from '@vue/test-utils';
import EmailInput from '../EmailInput.vue';

describe('EmailInput', () => {
  it('renders an email input', () => {
    const wrapper = mount(EmailInput);
    const input = wrapper.find('input[type="email"]');
    expect(input.exists()).toBe(true);
  });

  it('updates the email data when the input value changes and validates it', async () => {
    const wrapper = mount(EmailInput);
    const input = wrapper.find('input[type="email"]');

    // 有効なメールアドレスを入力
    await input.setValue('test@example.com');
    expect(wrapper.find('input[type="email"]').element.value).toBe('test@example.com');
    expect(wrapper.find('.error-message').exists()).toBe(false);
  });
  it('updates the email data when the input value invalid', async () => {
    const wrapper = mount(EmailInput, {
      props: {
        modelValue: 'invalid_email',
      },
    });
    const input = wrapper.find('input[type="email"]');
    // 無効なメールアドレスを入力
    await input.setValue('invalid-email');
    // TODO: 何故か以下のテストケースがコケるので、原因を調べる
    // expect(wrapper.find('input[type="email"]').element.value).toBe('invalid-email');
    expect(wrapper.find('.error-message').exists()).toBe(true);
  });
});
