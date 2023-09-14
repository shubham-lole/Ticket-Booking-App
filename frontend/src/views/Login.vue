<template>
  <div class="login">
    <div>
      <br /><br />
      <h1>Login</h1>
      <form @submit.prevent="submit">
        <div>
          <label>
      <input type="radio" name="role" value="admin" v-model="role" /> Admin
    </label>
    <label>
      <input type="radio" name="role" value="user" v-model="role" /> User
    </label>
        </div>
        <div>
          <label for="username">Username:</label>
          <input type="text" name="username" v-model="form.username" />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" name="password" v-model="form.password" />
        </div>
        <button type="submit">Submit</button>
      </form>
      <p v-if="showError" id="error">{{ er }}</p>
      <span> Not a User yet? <router-link to="/register"> Signup </router-link> </span>
    </div>
    <br><br>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import axios from "axios";

export default {
  name: "Login",
  components: {},
  data() {
    return {
      role: "user",
      form: {
        username: "",
        password: "",
        role: "user",
      },
      er: [],
      showError: false
    };
  },
  methods: {
    ...mapActions(["LogIn"]),
    async submit() {
      const User = new FormData();
      User.append("username", this.form.username);
      User.append("password", this.form.password);
      User.append("role", this.role);
      await this.LogIn(User).then((res) => {
        //console.log(res["access_token"])
        if (!(res["access_token"])) {
          this.er = res
          this.showError = true
        }
        else{
          this.$router.push("/")
        }
      })
      axios.get("/api/update_last_visited?user=" + this.form.username)
    },
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}

button[type="submit"] {
  background-color: #4caf50;
  color: white;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 30px;
}

button[type="submit"]:hover {
  background-color: #45a049;
}

input {
  margin: 5px;
  box-shadow: 0 0 15px 4px rgba(0, 0, 0, 0.06);
  padding: 10px;
  border-radius: 30px;
}
#error {
  color: red;
}
</style>
