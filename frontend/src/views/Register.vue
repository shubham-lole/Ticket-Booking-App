<template>
  <div class="register">
    <div>
      <br><br>
      <h1>Register</h1>
      <form @submit.prevent="submit">
        <div>
          <label for="username">Username:</label>
          <input type="text" name="username" v-model="form.username" />
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" name="email" v-model="form.email" />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" name="password" v-model="form.password" />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
    <p v-if="success" id="success" style="color: green;">{{ success }}</p>
    <p v-if="showError" id="error">{{ er }}</p>
    <span> Already a User? <router-link to="/login"> LogIn </router-link> </span>
  </div>
</template>

<script>
import { mapActions} from "vuex";

export default {
  name: "Register",
  components: {},
  data() {
    return {
      form: {
        username: "",
        password: "",
        email: "",
      },
      success: "",
      er: [],
      showError: false
    };
  },
  methods: {
    ...mapActions(["Register"]),
    async submit() {
        const User = new FormData();
        User.append("username", this.form.username);
      User.append("password", this.form.password);
      User.append("email", this.form.email);
      await this.Register(User).then((res) => {
        if (!(res["message"] == "User created successfully")) {
          this.er = res
          this.showError = true
        }
        else{
          this.success = res["message"] + " Please login to continue."
        }
      });
    },
  },
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
