<template>
  <div>
    
<b-navbar toggleable="lg" type="dark" variant="dark" id="navbar">
  <b-navbar-brand href="#">BookMyShow</b-navbar-brand>
  <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

  <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav v-if="!(isLoggedIn)">
        <b-nav-item><router-link to="/register">Register</router-link></b-nav-item>
        <b-nav-item><router-link to="/login">Login</router-link></b-nav-item>
      </b-navbar-nav>

        <b-navbar-nav v-if="isLoggedIn">
          <b-nav-item><router-link to="/" >Dashboard</router-link> </b-nav-item>
          <b-nav-item><router-link :to="{ path: '/profile', query: { user: User } }">
        <span v-if="Role == 'user'"> My Bookings</span> 
        <span v-if="Role == 'admin'"> Booking Management</span> 
        </router-link> </b-nav-item>
        <b-nav-item v-if="Role == 'admin'"><router-link to="/export">Export</router-link></b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav v-if="isLoggedIn" class="ml-auto">
          <b-nav-item><router-link to="/search">Search</router-link></b-nav-item>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>{{ User }}</em>
            </template>
            <b-dropdown-item @click="logout">Log Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
  </b-collapse>
</b-navbar>

  <!--div id="nav">
    <span v-if="!(isLoggedIn)">
      <router-link to="/register">Register |</router-link>
      <router-link to="/login">Login</router-link>
    </span>
    <span v-if="isLoggedIn">
      <router-link to="/">Dashboard | </router-link> 
      <router-link :to="{ path: '/profile', query: { user: User } }">
      <span v-if="Role == 'user'"> My Bookings | </span> 
      <span v-if="Role == 'admin'"> Booking Management | </span> 
      </router-link> 
      <router-link to="/search">Search | </router-link>
      <a @click="logout"> Logout</a>
    </span>   
  </div-->
  </div>
</template>
<script>
import { mapGetters } from 'vuex';



export default {
  name: "NavBar",
  computed: {
    ...mapGetters({ User: "StateUser", Role: "StateRole" }),
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    async logout() {
      await this.$store.dispatch("LogOut");
      this.$router.push("/login");
    },
  },
};
</script>

<style>

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

a:hover {
  cursor: pointer;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
