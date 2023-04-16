// src/components/__tests__/Login.spec.ts
import { describe, afterEach, it, expect, vi } from "vitest";
import { mount } from '@vue/test-utils';
import Login from "../Login.vue";
import EmailInput from "../EmailInput.vue";
import PasswordInput from "../PasswordInput.vue";
import axios from "axios";


vi.mock("axios");


describe("Login.vue", () => {
  afterEach(() => {
    // モックのリセット
  axios.post.mockReset();
  });

  it("submits the form and logs in successfully", async () => {
    const wrapper = mount(Login, {
      global: {
        components: {
          EmailInput,
          PasswordInput,
        },
        mocks: {
          axios: axios,
        },
      },
    });

    // 成功した API レスポンスのシミュレーション
    axios.post.mockResolvedValueOnce({
      data: {
        access_token: "sample_access_token",
      },
    });

    await wrapper.findComponent(EmailInput).vm.$emit("update:modelValue", "test@example.com");
    await wrapper.findComponent(PasswordInput).vm.$emit("update:modelValue", "testpassword");

    await wrapper.find("form").trigger("submit.prevent");

    // axios.post が正しい引数で呼び出されることを確認
    expect(axios.post).toHaveBeenCalledWith("http://localhost:8081/api/account/token/", {
      email: "test@example.com",
      password: "testpassword",
    });

    // 成功したレスポンスが正しく処理されることを確認
    expect(wrapper.vm.email).toBe("test@example.com");
    expect(wrapper.vm.password).toBe("testpassword");
  });

  it("handles login failure", async () => {
    const wrapper = mount(Login, {
      global: {
        components: {
          EmailInput,
          PasswordInput,
        },
        mocks: {
          axios: axios,
        },
      },
    });

    // 失敗した API レスポンスのシミュレーション
    axios.post.mockRejectedValue(new Error("Login failed"));

    await wrapper.findComponent(EmailInput).vm.$emit("update:modelValue", "test@example.com");
    await wrapper.findComponent(PasswordInput).vm.$emit("update:modelValue", "wrongpassword");

    await wrapper.find("form").trigger("submit.prevent");

    // axios.post が正しい引数で呼び出されることを確認
    expect(axios.post).toHaveBeenCalledWith("http://localhost:8081/api/account/token/", {
      email: "test@example.com",
      password: "wrongpassword",
    });

    // エラーが正しく処理されることを確認
    expect(wrapper.vm.errorOccurred).toBeTruthy();
  });
});
