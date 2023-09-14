<template>
    <div>
        <div v-if="Role=='admin'">
            <p> Admin logged in </p>
            <h1> Edit Theater/Show </h1>
            <br>
            <b-form v-if="TheaterID" @submit.prevent="submitEditForm">
                    <b-form-group label="Theater Name">
                        <b-form-input v-model="theaterName"></b-form-input>
                    </b-form-group>
                    <b-form-group label="Place">
                        <b-form-input v-model="place" disabled></b-form-input>
                    </b-form-group>
                    <b-form-group label="Capacity">
                        <b-form-input v-model="capacity"></b-form-input>
                    </b-form-group>
                    <!-- Add more form fields as needed -->
                    <b-button type="submit">Save Changes</b-button>
                </b-form>
            <b-form v-if="ShowID" @submit.prevent="submitEdit2Form">
                        <b-form-group label="Show Name">
                            <b-form-input v-model="showName"></b-form-input>
                        </b-form-group>
                        <b-form-group label="Show Rating">
                            <b-form-input v-model="showRating"></b-form-input>
                        </b-form-group>
                        <b-form-group label="Tags">
                            <b-form-input v-model="tags"></b-form-input>
                        </b-form-group>
                        <b-form-group label="Ticket Price">
                            <b-form-input v-model="ticketPrice"></b-form-input>
                        </b-form-group>
                        <!-- Add more form fields as needed -->
                        <b-button type="submit">Save Changes</b-button>
                    </b-form>
        </div>
        <div v-if="Role=='user'">
            <p> Unauthorised Access </p>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    name: "Edit",
    components: {},
    data() {
        return {
            TheaterID: "",
            theaterName: "",
            place: "",
            capacity: "",
            ShowID: "",
            showName: "",
            showRating: "",
            ticketPrice: "",
            tags: "",
            form: {
                theaterName: "",
                place: "",
                capacity: "",
            },
            form2: {
                showName: "",
                showRating: "",
                ticketPrice: "",
                tags: "",
            }
        }
    },
    created() {
        // Get the show details from query parameters
        this.TheaterID = this.$route.query.theaterId || "";
        this.theaterName = this.$route.query.name || "";
        this.place = this.$route.query.place || "";
        this.capacity = this.$route.query.capacity || "";
        this.ShowID = this.$route.query.showId || "";
        this.showName = this.$route.query.name || "";
        this.showRating = this.$route.query.rating || "";
        this.ticketPrice = this.$route.query.ticketPrice || "";
        this.tags = this.$route.query.tags || "";
    },
    methods: {
        ...mapActions(["UpdateTheater"]),
        async submitEditForm() {
            this.form.theaterId = this.TheaterID;
            this.form.theaterName = this.theaterName;
            this.form.place = this.place;
            this.form.capacity = this.capacity;
            console.log(this.form);
            try {
                const response = await this.$store.dispatch("UpdateTheater", this.form);
                console.log(response);
                alert("Theater updated successfully!");
                this.$router.push({ name: "Home" });
            }
            catch (err) {
                console.log(err);
            }
        },
        ...mapActions(["UpdateShow"]),
        async submitEdit2Form() {
            this.form2.showId = this.ShowID;
            this.form2.showName = this.showName;
            this.form2.showRating = this.showRating;
            this.form2.ticketPrice = this.ticketPrice;
            this.form2.tags = this.tags;
            console.log(this.form2);
            try {
                const response = await this.$store.dispatch("UpdateShow", this.form2);
                console.log(response);
                alert("Show updated successfully!");
                this.$router.push({ name: "Home" });
            }
            catch (err) {
                console.log(err);
            }
        },
    },
    computed: {
        ...mapGetters({Role: "StateRole", StateToken: "StateToken"})
    },
    }

</script>

<style>

</style>