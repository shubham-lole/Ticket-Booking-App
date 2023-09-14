<template>
  <div class="home">
    <div class="container" v-if="!(User)">
      <br><br>
      <div class="header">
            <h1>Welcome to BookMyShow</h1>
            <p>Your Destination for Entertainment</p>
        </div>
        <div class="banner"></div>
        <div class="container">
            <div class="introduction">
                <h2>Discover the Best in Entertainment</h2>
                <p>Book tickets for movies, concerts, theater plays, and more!</p>
            </div>
            <div class="link">
              <span> Please <router-link to="/login">Login</router-link> to continue...</span>
            </div>
        </div>
    </div>

    <br>
    <h6 v-if="User">Welcome {{ User }} </h6>
    <div v-if="isauthenticated">
    <div v-if="Role == 'admin'">
        <div id="addtheater">
            <b-button v-b-modal.modal-1 type="submit">Add Theater</b-button>
            <b-modal id="modal-1" title="Add Theater" @ok.prevent="addtheater">
              <b-form @ok.stop="addtheater">

                <b-form-group
                  label="Theater Name"
                  label-for="name"
                  invalid-feedback="Name required">
                <b-form-input
                  id="name"
                  v-model="form.name"
                  required></b-form-input>  
                </b-form-group>

                <b-form-group
                    label="Place"
                    label-for="place"
                    invalid-feedback="Place required">
                  <b-form-input
                    id="place"
                    v-model="form.place"
                    required></b-form-input>    
                </b-form-group>

                <b-form-group
                    label="Capacity"
                    label-for="capacity"
                    invalid-feedback="Capacity required">
                  <b-form-input
                    id="capacity"
                    v-model="form.capacity"
                    required></b-form-input>  
                </b-form-group>
                    
              </b-form>
              <br>
              <div v-if="successMessage" id="success">{{ successMessage }}</div>
              <div v-if="errorMessage" class="error-message" id="error">{{ errorMessage }}</div>
            </b-modal>
          </div>
          <div id="addshow">
                <b-button v-b-modal.modal-2 type="submit">Add Show</b-button>
                <b-modal id="modal-2" title="Add Show" @ok.prevent="addshow">
                  <b-form @ok.stop="addshow">  

                    <!--b-form-group
                      label="Theater"
                      label-for="theater"
                      invalid-feedback="Theater required"
                    >
                      <b-form-select
                        id="theater"
                        v-model="theaterid"
                        :options="theaterOptions"
                        required
                      ></b-form-select>
                    </b-form-group-->

                    <b-form-group
                      label="Show Name"
                      label-for="name"
                      invalid-feedback="Name required">
                    <b-form-input
                      id="name"
                      v-model="form2.name"
                      required></b-form-input>  
                    </b-form-group>
  
                    <b-form-group
                        label="Show Date"
                        label-for="date"
                        invalid-feedback="Date required">
                      <b-form-datepicker
                        id="date"
                        v-model="date"
                        required></b-form-datepicker>  
                      </b-form-group>

                      <!--b-form-group
                          label="Show Time"
                          label-for="time"
                          invalid-feedback="Time required">
                        <b-form-timepicker
                          id="timw"
                          v-model="time"
                          required></b-form-timepicker>  
                        </b-form-group-->

                    <b-form-group
                        label="Ratings"
                        label-for="ratings"
                        invalid-feedback="Ratings required">
                      <b-form-input
                        id="ratings"
                        v-model="form2.ratings"
                        required></b-form-input>    
                    </b-form-group>
  
                    <b-form-group
                        label="Tags"
                        label-for="tags"
                        invalid-feedback="tags required">
                      <b-form-input
                        id="tags"
                        v-model="form2.tags"
                        required></b-form-input>  
                    </b-form-group>

                    <b-form-group
                          label="Ticket Price"
                          label-for="price"
                          invalid-feedback="Ticket Price required">
                        <b-form-input
                          id="price"
                          v-model="form2.ticket_price"
                          required></b-form-input>  
                    </b-form-group>

                     <!-- Theater and Timing Input -->
        <div v-for="(theater, index) in form2.theaters" :key="index">
    <b-form-group :label="`Theater ${index + 1}`" :label-for="`theater-${index}`">
      <b-form-select
      class="theater-options"
        :id="`theater-${index}`"
        v-model="theater.theater_id"
        :options="theaterOptions"
        required
      ></b-form-select>
    </b-form-group>

    <b-form-group :label="`Show Time ${index + 1}`" :label-for="`time-${index}`">
      <b-form-timepicker
        :id="`time-${index}`"
        v-model="theater.timing"
        required
      ></b-form-timepicker>
    </b-form-group>
  </div>

        <b-button @click="addTheaterTiming" variant="secondary">
          Add Another Theater & Timing
        </b-button>
                      
                  </b-form>
                  <br>
                  <div v-if="successMessage" id="success">{{ successMessage }}</div>
                  <div v-if="errorMessage" class="error-message" id="error">{{ errorMessage }}</div>
                </b-modal>
              </div>
    </div>

    <hr>

    <div id="filter">
      <b-row>
        <b-col>        </b-col>
        <b-col align-h="center" justify="center">   
            <b-row>
              <b-form-group label="Start Date" label-for="start-date">
              <b-form-datepicker id="start-date" v-model="startDate" required></b-form-datepicker>
            </b-form-group>
            </b-row> <br>
            <b-row>
              <b-form-group label="End Date" label-for="end-date">
              <b-form-datepicker id="end-date" v-model="endDate" required></b-form-datepicker>
            </b-form-group>
            </b-row> <br>
            <b-row>
              <b-button @click="filterShows" variant="primary">Filter Shows</b-button>
              
            </b-row>
            <br>
            <b-row>
              <b-button @click="resetFilter" variant="secondary">Reset Filter</b-button>
            </b-row>
        </b-col>
        <b-col>       </b-col>
      </b-row>
      <br>

       <!-- Show Cards Section -->
      <div class="filter-results">
        <b-row v-if="filteredShows.length > 0" align-h="center" justify="center">
          <b-col
            v-for="show in filteredShows"
            :key="show.ShowID"
            cols="12"
            md="6"
            lg="4"
          >
            <b-card v-for="timing in show.Timings" :key="timing.TimingID" class="show-card">
              <template #header>
                <h5>{{ show.Name }}</h5>
              </template>
              <b-card-text>
                <p>Ticket Price: <b>Rs{{ show.TicketPrice }}/-</b></p>
                <p>Rating: {{ show.Rating }}</p>
                <p>Tags: {{ show.Tags }}</p>
                <p>Timing: {{ timing.Timing }}</p>
                <!-- Add more show details here if needed -->
              </b-card-text>
              <!-- Add any other buttons or actions related to the show here -->
              <!-- For example, you can add a "Book Show" button here -->
              <template #footer>
                <b-button-group 
              :key="timing.TimingID" >
              <b-button
              v-if=" Role == 'user'"
              @click="bookticket(show, timing)" variant="primary"
              :disabled="timing.isShowFull == true"
            > Book Show</b-button>
              </b-button-group>
                <b-button v-if="Role == 'admin'" @click="editShow(show)">Edit Show</b-button>
                <b-button v-if="Role == 'admin'" variant="danger" @click="deleteShow(show.ShowID)">Delete Show</b-button>
              </template>
            </b-card>
          </b-col>
        </b-row>
        <div v-else>
          <p>No shows available for the selected date range.</p>
        </div>
      </div>

      </div>
      <hr>

    

     <div class="feed-section" v-if="filteredShows.length < 1">
    <b-row align-h="center" justify="center" v-for="theater in Theaters['theaters']" :key="theater.TheaterID" class="theater-card" :id="'theater-' + theater.TheaterID">
      <b-card>
        <template #header>
          <h5>{{ theater.Name }}</h5>
        </template>
        <b-card-text>
          <!-- Use a div with class="d-flex" to remove whitespace between b-row and b-col -->
          <div class="d-flex">
            <!-- Filter the shows array based on the current theater -->
            <b-col v-for="show in Shows['shows'].filter(show => show.Theaters.some(t => t.TheaterID === theater.TheaterID))" :key="show.ShowID" :id="'show-' + show.ShowID" cols="2">
              <b-card class="show-card">
                <template #header>
                  <h6>{{ show.Name }}</h6>
                </template>
                <!-- Show details can be displayed here -->
                <b-card-text>
                  <p>Ticket Price: <b>Rs{{ show.TicketPrice }}/-</b></p>
                  <p>Rating: {{ show.Rating }}</p>
                  <label v-for="timing in show.Timings" :key="timing.TimingID">
                <span v-if="timing.TheaterID == theater.TheaterID" class="mr-2">Timing:  {{ timing.Timing }}</span></label>
                  <!-- Add more show details here if needed -->
                </b-card-text>
                <!-- Add any other buttons or actions related to the show here -->
                <!-- For example, you can add a "Book Show" button here -->
                
                <template #footer>
                  <b-button-group v-for="timing in show.Timings"
              :key="timing.TimingID" >
            
          <b-button
            v-if="timing.TheaterID == theater.TheaterID && Role == 'user'"
            @click="bookticket(show, timing)" variant="primary"
            :disabled="timing.isShowFull == true"
          >
          <p v-if="timing.TheaterID == theater.TheaterID && timing.isShowFull">Show Housefull</p>
          <p v-else> Book Show</p>
          </b-button>
        </b-button-group>
                  <b-button v-if="Role == 'admin'" @click="editShow(show)">Edit Show</b-button>
                <b-button v-if="Role == 'admin'" variant="danger" @click="deleteShow(show.ShowID)">Delete Show</b-button>
                </template>
              </b-card>
            </b-col>
          </div>
        </b-card-text>
        <template #footer>
          <div v-if="Role == 'admin'">
            <b-button v-b-modal.modal-3 variant="primary" @click="editTheater(theater)">Edit Theater</b-button>&nbsp;
            <b-button variant="danger" @click="deleteTheater(theater.TheaterID)">Delete Theater</b-button>
          </div>
          </template>
      </b-card>
    </b-row>
  </div>
  

    </div>  
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      form: {
        name: "",
        place: "",
        capacity: "",
        admin: ""
      },
      form2: {
        name: "",
        ratings: "",
        tags: "",
        ticket_price: "",
        theaters: [],
      },
      selectedTheaters: [],
      theaterTimings: [],
      theaterid: "",
      date: "",
      time: "",
      timing: this.date + " " + this.time,
      errorMessage: "", // Variable to store the error message
      successMessage: "", // Variable to store the success message
      startDate: null,
      endDate: null,
      filteredShows: [],
    };
  },
  computed: {
    ...mapGetters({ User: "StateUser", Role: "StateRole", Theaters: "StateTheaters", Shows: "StateShows", isauthenticated: "isAuthenticated", allShows: "allShows" }),
        theaterOptions() {
      return this.Theaters.theaters.map((theater) => ({
        value: theater.TheaterID,
        text: theater.Name
      }));
    }

  },
  methods: {
    filterShows() {
      if (!this.startDate || !this.endDate) {
        // Handle case when dates are not selected
        console.error("Please select both start and end dates.");
        return;
      }

      // Convert the selected start and end dates to Date objects
      const startDate = new Date(this.startDate);
      const endDate = new Date(this.endDate);

      // Filter shows based on the selected date range
      const filteredShows = this.Shows.shows.filter((show) => {
        for (const timing of show.Timings) {
          const showDate = new Date(timing.Timing);
          if (showDate >= startDate && showDate <= endDate) {
            return true;
          }
        }
        return false;
      });

      // Update the filteredShows list in your data
      this.filteredShows = filteredShows;
    },
    resetFilter(){
      this.filteredShows = [];
      this.startDate = null;
      this.endDate = null;
    },
    showIsInTheFuture(timings) {
      const now = new Date();
      for (const timing of timings) {
        const showTime = new Date(timing.Timing);
        if (showTime > now) {
          return true; // Show is in the future, so display it
        }
      }
      return false; // None of the timings are in the future
    },
    addTheaterTiming() {
      this.form2.theaters.push({
        theater_id: null,
        timing: null,
      });
    },
    async addtheater() {
      this.form.admin = this.User;
      const response = await this.$store.dispatch("AddTheater", this.form);

      // Check for error response
      if (response.error) {
        this.errorMessage = response.error;
      } else {
        this.successMessage = response.message;
        setTimeout(() => {
          this.$bvModal.hide("modal-1");
        }, 1000);
        this.errorMessage = ""; // Clear the error message if successful
        this.form = {
          name: "",
          place: "",
          capacity: "",
          admin: ""
        };
      }
    },
    async addshow() {
      for (const theater of this.form2.theaters) {
        theater.timing = this.date + " " + theater.timing; // Update each theater's timing
      }
        const response = await this.$store.dispatch("AddShow", this.form2);

      if (response.error) {
        this.errorMessage = response.error;
      } else {
        this.successMessage = response.message;
        setTimeout(() => {
          this.$bvModal.hide("modal-2");
        }, 1000);
        this.errorMessage = ""; // Clear the error message if successful
        this.form2 = {
          name: "",
          ratings: "",
          tags: "",
          ticket_price: "",
          theaters: [],
        };
      }
    },
    async deleteTheater(theaterId) {
      const confirmation = window.confirm("Are you sure you want to delete this Theater?");
      if (confirmation) {
        const response = await this.$store.dispatch("DeleteTheater", theaterId);

        // Check for error response
        if (response.error) {
          this.errorMessage = response.error;
        } else {
          this.successMessage = response.message;
          this.errorMessage = ""; // Clear the error message if successful
        }
      }
    },
    async deleteShow(showId) {
      const confirmation = window.confirm("Are you sure you want to delete this Show?");
      if (confirmation) {
        try {
          const response = await this.$store.dispatch("DeleteShow", showId);

          // Check for error response
          if (response.error) {
            this.errorMessage = response.error;
          } else {
            this.successMessage = response.message;
            this.errorMessage = ""; // Clear the error message if successful
          }
        } catch (error) {
          console.error("Delete Show Error:", error);
          this.errorMessage = "An error occurred while deleting the show.";
        }
      }
    },

    getShowsByTheater(theaterId) {
      return this.Shows.shows.filter(show => show.theaters.TheaterID === theaterId);
    },
    editTheater(theater) {
      // Logic to handle editing the theater
      this.$router.push({
        path: "/edit",
        query: {
          theaterId: theater.TheaterID,
          name: theater.Name,
          place: theater.Place,
          capacity: theater.Capacity,
          // Add more theater details as needed
        },
      });
      console.log("Edit theater:", theater);
    },
    editShow(show) {
      // Logic to handle editing the show
      this.$router.push({
        path: "/edit",
        query: {
          showId: show.ShowID,
          name: show.Name,
          rating: show.Rating,
          ticketPrice: show.TicketPrice,
          tags: show.Tags,
          // Add more show details as needed
        },
      });
      console.log("Edit show:", show);
    },
    async bookticket(show, timing) {
      console.log("Book show:", show, timing);
      this.$router.push({
        path: "/booking",
        query: {
          showId: show.ShowID,
          name: show.Name,
          rating: show.Rating,
          ticketPrice: show.TicketPrice,
          timing: timing,
          theaterId: timing.TheaterID,
          // Add more show details as needed
        },
      });
    },
    ...mapActions(["GetTheaters"]),
  },
  created() {
    this.GetTheaters();
  },
};
</script>

<style>


.d-flex {
    display: flex;
  }

  .show-card{
    margin: 10px; /* Adjust the value to set the desired spacing between show cards */
  }

.theater-card{
  width: 100vw;
  margin-left: 5px;
  margin-right: 5px;
  margin-top: 10px;
  margin-bottom: 10px;
}

#error {
  color: red;
}

</style>