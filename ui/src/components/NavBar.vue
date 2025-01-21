<template>
  <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <div class="toggle-btn" @click="toggleSidebar">
      <span>☰</span>
    </div>
    <nav class="nav-links">
      <router-link to="/">
        <span class="icon">📅</span>
        <span class="text" v-show="!isCollapsed">Shift Plans</span>
      </router-link>
      <router-link to="/crew">
        <span class="icon">👥</span>
        <span class="text" v-show="!isCollapsed">Crew Assignments</span>
      </router-link>
      <router-link to="/availability/1">
        <span class="icon">🎯</span>
        <span class="text" v-show="!isCollapsed">My Availability</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      isCollapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  background-color: #1a1a1a;
  width: 240px;
  transition: width 0.3s ease;
  color: white;
}

.collapsed {
  width: 60px;
}

.toggle-btn {
  padding: 20px;
  cursor: pointer;
  color: #fff;
}

.nav-links {
  display: flex;
  flex-direction: column;
  padding: 20px 0;
}

.nav-links a {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: white;
  text-decoration: none;
  transition: background-color 0.2s;
}

.nav-links a:hover {
  background-color: #2c2c2c;
}

.nav-links .icon {
  margin-right: 15px;
}

.router-link-active {
  background-color: #2c2c2c;
}
</style>
