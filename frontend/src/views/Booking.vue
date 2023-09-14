<template>
    <div>
        <b-container fluid>
            <h3>Booking Form</h3>
            <b-form @submit.prevent="submitBookingForm">
                <b-form-group label="Show Name">
                    <b-form-input v-model="showName" disabled></b-form-input>
                </b-form-group>
                <b-form-group label="Show Rating">
                    <b-form-input v-model="showRating" disabled></b-form-input>
                </b-form-group>
                <b-form-group label="Ticket Price">
                    <b-form-input v-model="ticketPrice" disabled></b-form-input>
                </b-form-group>
                <b-form-group label="Timing">
                        <b-form-input v-model="timing.Timing" disabled></b-form-input>
                    </b-form-group>
                <b-form-group label="Number of Tickets">
                    <b-form-input v-model="number_ticket" type="number" required></b-form-input>
                </b-form-group>
                <br>
                The total amount to be paid is <b> Rs.{{ number_ticket * ticketPrice }}/- </b>
                <br>
                <!-- Add more form fields as needed -->
                <b-button type="submit">Book Ticket</b-button>
            </b-form>
            <p v-if="showError" id="error">{{ er }}</p>
        </b-container>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            showName: "",
            showRating: "",
            ticketPrice: "",
            number_ticket: "",
            timing: "",
            showId: "",
            form: {
                num_tickets: "",
                show_timing_id: "",
                user: "",
            },
            er: [],
            showError: false
            // Add more data properties for other form fields
        };
    },
    created() {
        // Get the show details from query parameters
        this.showName = this.$route.query.name || "";
        this.showRating = this.$route.query.rating || "";
        this.ticketPrice = this.$route.query.ticketPrice || "";
        this.timing = this.$route.query.timing || "";
        this.showId = this.$route.query.showId || "";
        // Pre-fill other form fields with query parameters as needed
    },
    computed: {
        ...mapGetters({ User: "StateUser", Role: "StateRole", Theaters: "StateTheaters", Shows: "StateShows", isauthenticated: "isAuthenticated" }),
    },
    methods: {
         async submitBookingForm() {
            this.form.num_tickets = this.number_ticket;
            this.form.show_timing_id = this.timing.TimingID;
            this.form.user = this.User;

            try {
                const response = await this.$store.dispatch("BookShow", this.form);
                alert("Your tickets are booked successfully!");
                this.$router.push({ name: "Home" });
                console.log(response);
            } catch (error) {
                this.showError = true;
                this.er = error
            }
        },
    },
};
</script>
