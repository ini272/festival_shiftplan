<template>
  <div class="crew-availability">
    <h3>My Availability</h3>
    <table class="availability-grid">
      <thead>
        <tr>
          <th>Time Slot</th>
          <th v-for="date in getDates()" :key="date">
            {{ formatDate(date) }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="timeSlot in getUniqueTimeSlots()" :key="timeSlot">
          <td>{{ timeSlot }}</td>
          <td v-for="date in getDates()" :key="date"
              :class="{
                'unavailable': isTimeSlotUnavailable(timeSlot, date),
                'no-shift': !hasShiftForTimeSlot(timeSlot, date)
              }"
              @click="hasShiftForTimeSlot(timeSlot, date) && toggleTimeSlotForDate(timeSlot, date)">
            {{ getAreasForTimeSlot(timeSlot, date).join(', ') }}
            <div class="toggle-overlay" v-if="hasShiftForTimeSlot(timeSlot, date)">
              {{ isTimeSlotUnavailable(timeSlot, date) ? '❌' : '✓' }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CrewAvailability',
  props: {
    crewId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      shifts: [],
      areas: [],
      unavailableShifts: new Set()
    }
  },
  methods: {
    getDates() {
      const dates = [...new Set(this.shifts.map(shift => 
        shift.start_time.split('T')[0]
      ))].sort()
      return dates
    },
    getUniqueTimeSlots() {
      const timeSlots = new Set(this.shifts.map(shift => 
        `${this.formatTime(shift.start_time)} - ${this.formatTime(shift.end_time)}`
      ))
      return [...timeSlots].sort()
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', { 
        weekday: 'short', 
        day: 'numeric' 
      })
    },
    formatTime(datetime) {
      return new Date(datetime).toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    getAreasForTimeSlot(timeSlot, date) {
      return this.shifts
        .filter(shift => {
          const shiftTime = `${this.formatTime(shift.start_time)} - ${this.formatTime(shift.end_time)}`
          const shiftDate = shift.start_time.split('T')[0]
          return shiftTime === timeSlot && shiftDate === date
        })
        .map(shift => this.getAreaName(shift.area_id))
    },
    getAreaName(areaId) {
      const area = this.areas.find(a => a.id === areaId)
      return area ? area.name : ''
    },
    isTimeSlotUnavailable(timeSlot, date) {
      const shifts = this.getShiftsForTimeSlot(timeSlot, date)
      return shifts.every(shift => this.unavailableShifts.has(shift.id))
    },
    hasShiftForTimeSlot(timeSlot, date) {
      return this.getShiftsForTimeSlot(timeSlot, date).length > 0
    },
    getShiftsForTimeSlot(timeSlot, date) {
      return this.shifts.filter(shift => {
        const shiftTime = `${this.formatTime(shift.start_time)} - ${this.formatTime(shift.end_time)}`
        const shiftDate = shift.start_time.split('T')[0]
        return shiftTime === timeSlot && shiftDate === date
      })
    },
    async toggleTimeSlotForDate(timeSlot, date) {
      const shifts = this.getShiftsForTimeSlot(timeSlot, date)
      const allUnavailable = shifts.every(shift => this.unavailableShifts.has(shift.id))

      for (const shift of shifts) {
        try {
          if (allUnavailable) {
            const preferencesResponse = await axios.get(`http://localhost:8000/crew/${this.crewId}/preferences/`)
            const preferenceToDelete = preferencesResponse.data.find(p => 
              p.shift_id === shift.id && 
              p.preference_type === 'AVOID'
            )
            if (preferenceToDelete) {
              await axios.delete(`http://localhost:8000/crew/${this.crewId}/preferences/${preferenceToDelete.id}`)
              this.unavailableShifts.delete(shift.id)
            }
          } else {
            await axios.post(`http://localhost:8000/crew/${this.crewId}/preferences/`, {
              preference_type: 'AVOID',
              crew_member_id: parseInt(this.crewId),
              shift_id: shift.id
            })
            this.unavailableShifts.add(shift.id)
          }
        } catch (error) {
          console.error('Error updating preference:', error)
        }
      }
    }
  },
  async created() {
    try {
      const [shiftsResponse, areasResponse] = await Promise.all([
        axios.get('http://localhost:8000/shifts/'),
        axios.get('http://localhost:8000/areas/')
      ])
      console.log('Shifts response:', shiftsResponse.data)
      this.shifts = shiftsResponse.data
      this.areas = areasResponse.data
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
}
</script>

<style scoped>
.crew-availability {
  margin: 20px;
  padding: 0 20px;
}
.availability-grid {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.availability-grid th,
.availability-grid td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
  position: relative;
}
.availability-grid td:not(:first-child) {
  cursor: pointer;
}
.availability-grid td:not(:first-child):hover:not(.no-shift) {
  background-color: #f5f5f5;
}
.unavailable {
  background-color: #ffebee;
}
.no-shift {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}
.toggle-overlay {
  position: absolute;
  top: 4px;
  right: 4px;
  font-size: 0.8em;
  opacity: 0.7;
}
</style>
