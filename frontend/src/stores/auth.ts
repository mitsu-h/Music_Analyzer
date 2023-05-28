import { defineStore } from "pinia";
import axios from "axios";

interface AuthState {
  token: string | null;
  user: { email: string } | null;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    token: null,
    user: null,
  }),
  persist: true,
  getters: {
    async isLoggedIn(state){
        return state.token !== null && await this.checkToken();
      }
    },
  actions: {
    async login({ email, password }: { email: string; password: string }) {
      try {
        const response = await axios.post("http://localhost:8081/api/account/token/", {
          email: email,
          password: password,
        });
        console.log("login success!")

        if (response.data.access) {
          this.token = response.data.access;
          this.user = { email: email };
           // Set JWT token to axios headers
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
        } else {
          throw new Error('Authentication failed');
        }
      } catch (error) {
        console.error('Login error:', error.message);
        throw error;
      }
    },
    
    logout() {
      this.token = null;
      this.user = null;
      // Remove JWT token from axios headers
      delete axios.defaults.headers.common["Authorization"];
    },
    async checkToken() {
      try {
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
        const response = await axios.get('http://localhost:8081/api/check_token/');
        return response.status === 200;
      } catch (error) {
        console.error('Token check error:', error.message);
        return false;
      }
    },
  },
});
