<template>
<div>
    <br>
    <h3 v-if="bookings.length < 1">No Bookings Yet</h3>


    <div id="container" name="user" v-if="Role=='user'">
    
    <b-table striped hover :items="bookings" :fields="fields"></b-table>

    </div>
    <div id="container" name="admin" v-if="Role=='admin'">
        <b-table striped hover :items="bookings" :fields="fields"></b-table>
    </div>

    </div>
</template>

<script>
import { mapGetters } from 'vuex';


export default {
    name: "Profile",
    data() {
        return{
            bookings: [],
        };
    },
    methods: {
        
    },
    async beforeCreate() {
        const response = await this.$store.dispatch("GetBookings");
        this.bookings = response.bookings;
    },
    computed: {
        ...mapGetters({ User: "StateUser", Role: "StateRole", Theaters: "StateTheaters", Shows: "StateShows", isauthenticated: "isAuthenticated" }),
    }
}
</script>

<style>
button[type="submit"] {
  background-color: #4caf50;
  color: white;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 30px;
  margin: 10px;
}

#image-div{
    vertical-align: middle;
  width: 250px;
  height: 250px;
  border-radius: 50%;
}
</style>