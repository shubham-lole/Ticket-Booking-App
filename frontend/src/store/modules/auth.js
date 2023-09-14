import axios from "axios";

const state = {
  user: null,
  access_token: null,
  role: null,
  theaters: null,
  shows: null,
  allShows: null
};

const getters = {
  isAuthenticated: (state) => !!state.user,
  StateToken: (state) => state.access_token,
  StateUser: (state) => state.user,
  StateRole: (state) => state.role,
  StateTheaters: (state) => state.theaters,
  StateShows: (state) => state.shows,
  StateAllShows: (state) => state.allShows,
};

const actions = {
  async Register({ commit }, user) {
    try {
      let api_url;
      api_url = "/api/register/user";
      const response = await axios.post(api_url, user)
      const responseData = response.data
      commit("setUser", user.get("username"))
      return responseData;
    }
    catch (error) {
      return error['response']['data']['message'];
    }
  },

  async LogIn({ commit }, user) {
    try {
      let api_url;
      if (user.get("role") == "admin") {
        api_url = "/api/login/admin";
      } else if (user.get("role") == "user") {
        api_url = "/api/login/user";
      }
      const response = await axios.post(api_url, user)
      const responseData = response.data;
      console.log(user.get("username"));
      console.log(!!user.get("username"));
      commit("setUser", { username: user.get("username"), access_token: responseData.access_token, role: user.get("role") });
      console.log(getters.StateToken);


      return responseData;
    }
    catch (error) {
      return error['response']['data']['message'];
    }
  },

  async AddTheater({ commit }, theater) {
    try {
      const response = await axios.post("/api/admin/theater", theater, {
        headers: {
          'Authorization': `Bearer ${this.getters.StateToken}`
        }
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      console.log(responseData);
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };

    }
  },

  async AddShow({ commit }, show) {
    try {
      const response = await axios.post("/api/admin/show", show, {
        headers: {
          'Authorization': `Bearer ${this.getters.StateToken}`
        }
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      console.log(responseData);
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };
    }
  },

  async BookShow({ commit }, booking) {
    try {
      const response = await axios.post("/api/booking", booking, {
        headers: {
          'Authorization': `Bearer ${this.getters.StateToken}`
        }
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      //console.log(responseData);
      return responseData;
    }
    catch (error) {
      if (error.response.data.message) {
        const errorMessage = error.response.data.message;
        throw new Error(errorMessage); // Throw the error here
      } else {
        const errorMessage = error.response.data.msg;
        throw new Error(errorMessage); // Throw the error here
      }
    }
  },

  async GetBookings() {

    try {
      let user = this.getters.StateUser;
      const response = await axios.get("/api/booking", {
        params: { user: user },
        headers: {
          'Authorization': `Bearer ${this.getters.StateToken}`
        }
      });
      console.log(response);
      const responseData = response.data;
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };
    }
  },


  async GetTheaters({ commit }) {
    const theaters = await axios.get("/api/admin/theater");
    const shows = await axios.get("/api/admin/show?current=1");
    const allShows = await axios.get("/api/admin/show?current=0");
    commit("setTheater", { theaters: theaters.data, shows: shows.data, allShows: allShows.data });
  },

  async LogOut({ commit }) {
    let user = null;
    let access_token = null;
    commit("logout", user, access_token);
  },

  async DeleteTheater({ commit }, theaterId) {
    try {
      const response = await axios.delete(`/api/admin/theater/${theaterId}`, {
        headers: {
          'Authorization': `Bearer ${this.getters.StateToken}`
        }
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };
    }
  },

  async DeleteShow({ commit }, showId) {
    try {
      const response = await axios.delete(`/api/admin/show/${showId}`, {
        headers: {
          Authorization: `Bearer ${this.getters.StateToken}`,
        },
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      return responseData;
    } catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };
    }
  },

  async UpdateTheater({ commit }, theater) {
    try {
      const response = await axios.put(`/api/admin/theater/${theater.theaterId}`, theater, {
        headers: {
          Authorization: `Bearer ${this.getters.StateToken}`,
        },
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };
    }
  },

  async UpdateShow({ commit }, show) {
    try {
      const response = await axios.put(`/api/admin/show/${show.showId}`, show, {
        headers: {
          Authorization: `Bearer ${this.getters.StateToken}`,
        },
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      return { error: errorMessage };
    }
  },

  async SearchTheater({ commit }, search) {
    try {
      const response = await axios.get(`/api/theater/search?location=${search}`, {
        headers: {
          Authorization: `Bearer ${this.getters.StateToken}`,
        },
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      throw new Error(errorMessage);
    }
  },

  async SearchShow({ commit }, search) {
    try {
      const response = await axios.get(`/api/show/search?tags=${search}`, {
        headers: {
          Authorization: `Bearer ${this.getters.StateToken}`,
        },
      });
      const responseData = response.data;
      const theaters = await axios.get("/api/admin/theater");
      const shows = await axios.get("/api/admin/show");
      commit("setTheater", { theaters: theaters.data, shows: shows.data });
      return responseData;
    }
    catch (error) {
      const errorMessage = error.response.data.message;
      throw new Error(errorMessage);
    }
  },
};

const mutations = {
  setUser(state, { username, access_token, role }) {
    state.user = username;
    state.access_token = access_token;
    state.role = role
  },
  setTheater(state, { theaters, shows, allShows }) {
    state.theaters = theaters;
    state.shows = shows;
    state.allShows = allShows;
  },
  logout(state, user) {
    state.user = user;
    state.role = null;
    state.access_token = null;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
