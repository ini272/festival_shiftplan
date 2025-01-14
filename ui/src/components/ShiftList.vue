<template>
  <div class="shift-list">
    <h3>Shifts for {{ planName }}</h3>
    <div v-for="date in getDates()" :key="date" class="day-table">
      <h4>{{ formatDate(date) }}</h4>
      <vue-good-table
        :columns="getColumnsForDay()"
        :rows="getRowsForDay(date)"
        styleClass="vgt-table"
      >
        <template #table-row="props">
          <span v-if="props.column.field === 'assignment'" 
                class="shift-bar"
                :style="getShiftStyle(date, props.row.time)">
            <div class="assignment-slots" 
                 :style="`grid-template-columns: repeat(${props.row.capacity}, 1fr)`">
              <div v-for="i in props.row.capacity" :key="i" class="slot">
                {{ props.row.crew_members && props.row.crew_members[i-1] ? 
                   props.row.crew_members[i-1].name : '-' }}
              </div>
            </div>
          </span>
          <span v-else>{{ props.row[props.column.field] }}</span>
        </template>
      </vue-good-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ShiftList',
  props: {
    planId: {
      type: Number,
      required: true
    },
    planName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      shifts: []
    }
  },
  methods: {
    getDates() {
      return [...new Set(this.shifts.map(shift => 
        shift.start_time.split('T')[0]
      ))]
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', { 
        weekday: 'long', 
        month: 'short', 
        day: 'numeric' 
      })
    },
    getColumnsForDay() {
      return [
        { field: 'time', label: 'Time' },
        { field: 'assignment', label: 'Assignment' },
        { field: 'capacity', label: 'Capacity' }
      ]
    },
    getRowsForDay(date) {
      const dayShifts = this.shifts.filter(shift => 
        shift.start_time.split('T')[0] === date
      )

      return dayShifts.map(shift => ({
        time: `${shift.start_time.split('T')[1].substring(0, 5)} - ${shift.end_time.split('T')[1].substring(0, 5)}`,
        assignment: 'placeholder',  // Will be handled by template
        capacity: shift.capacity,
        crew_members: shift.crew_members || []
      })).sort((a, b) => a.time.localeCompare(b.time))
    },
    getShiftStyle(date, timeSlot) {
      const shift = this.shifts.find(s => 
        s.start_time.split('T')[0] === date &&
        s.start_time.split('T')[1].startsWith(timeSlot.split(' - ')[0])
      )
      
      if (shift) {
        const startTime = new Date(shift.start_time)
        const endTime = new Date(shift.end_time)
        const duration = (endTime - startTime) / (1000 * 60 * 60)
        
        return {
          borderLeft: '4px solid #2196f3',
          height: `${Math.max(40, duration * 20)}px`,
          display: 'flex',
          alignItems: 'center',
          padding: '0 10px'
        }
      }
      return {}
    }  },
  async created() {
    try {
      const shiftsResponse = await axios.get(`http://localhost:8000/shifts/?plan_id=${this.planId}`)
      const shifts = shiftsResponse.data

      const assignmentsResponse = await axios.get('http://localhost:8000/assignments/')
      const assignments = assignmentsResponse.data

      const crewResponse = await axios.get('http://localhost:8000/crew/')
      const crewMembers = crewResponse.data

      this.shifts = shifts.map(shift => {
        const shiftAssignments = assignments.filter(a => a.shift_id === shift.id)
        if (shiftAssignments.length > 0) {
          const assignedCrew = shiftAssignments
            .map(assignment => crewMembers.find(c => c.id === assignment.crew_member_id))
            .filter(Boolean)
          shift.crew_members = assignedCrew
        }
        return shift
      })
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
}
</script>

<style scoped>
.day-table {
  margin-bottom: 30px;
}

.shift-bar {
  border-radius: 4px;
  margin: 4px 0;
  transition: all 0.2s ease;
  width: 100%;
}

.assignment-slots {
  display: grid;
  gap: 8px;
  width: 100%;
}

.slot {
  padding: 4px;
  border: 1px dashed #ccc;
  border-radius: 4px;
  background-color: white;
  text-align: center;
}

.shift-bar:hover {
  transform: scale(1.02);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
