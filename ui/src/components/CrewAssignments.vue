<template>
  <div class="crew-assignments">
    <h2>Crew Assignments</h2>
    <div v-for="member in crewMembers" :key="member.id" class="crew-member">
      <h3>{{ member.name }} ({{ member.role }})</h3>
      <div class="assignments">
        <div v-for="assignment in member.assignments" 
             :key="assignment.id" 
             class="assignment-card">
          <div class="time">
            {{ formatDateTime(getShiftTime(assignment.shift_id)) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CrewAssignments',
  data() {
    return {
      crewMembers: [],
      shifts: {}
    }
  },
  methods: {
    formatDateTime(shiftTime) {
      if (!shiftTime) return ''
      return `${new Date(shiftTime.start).toLocaleDateString()} ${new Date(shiftTime.start).toLocaleTimeString()} - ${new Date(shiftTime.end).toLocaleTimeString()}`
    },
    getShiftTime(shiftId) {
      return this.shifts[shiftId]
    }
  },
  async created() {
    try {
      const [crewResponse, shiftsResponse] = await Promise.all([
        axios.get('http://localhost:8000/crew/'),
        axios.get('http://localhost:8000/shifts/')
      ])
      
      this.shifts = shiftsResponse.data.reduce((acc, shift) => {
        acc[shift.id] = {
          start: shift.start_time,
          end: shift.end_time
        }
        return acc
      }, {})
      
      this.crewMembers = crewResponse.data
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
}
</script>

<style scoped>
.crew-member {
  margin: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.assignment-card {
  background-color: #f5f5f5;
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
}
</style>
