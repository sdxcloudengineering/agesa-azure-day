<template>
  <div>
    <div class="section-header">
      <div>
        <h1>Poliçeler</h1>
        <p class="page-subtitle">Sağlık, hayat, kasko ve konut poliçeleri</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ Yeni Poliçe</button>
    </div>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <div class="card">
      <table v-if="policies.length">
        <thead>
          <tr>
            <th>Poliçe No</th>
            <th>Müşteri</th>
            <th>Tür</th>
            <th>Durum</th>
            <th>Prim</th>
            <th>Teminat</th>
            <th>Bitiş Tarihi</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in policies" :key="p.id">
            <td>{{ p.policy_number }}</td>
            <td>{{ p.customer ? `${p.customer.first_name} ${p.customer.last_name}` : '—' }}</td>
            <td>{{ policyTypeLabel(p.type) }}</td>
            <td><span class="badge" :class="policyStatusBadgeClass(p.status)">{{ policyStatusLabel(p.status) }}</span></td>
            <td>{{ formatCurrency(p.premium) }}</td>
            <td>{{ formatCurrency(p.coverage_amount) }}</td>
            <td>{{ p.end_date }}</td>
            <td>
              <button class="btn btn-danger" @click="remove(p.id)">Sil</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">Henüz poliçe kaydı yok.</div>
    </div>

    <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
      <div class="modal">
        <h3>Yeni Poliçe</h3>
        <div class="form-grid">
          <div class="form-field full">
            <label>Müşteri</label>
            <select v-model="form.customer_id">
              <option value="" disabled>Seçiniz</option>
              <option v-for="c in customers" :key="c.id" :value="c.id">
                {{ c.first_name }} {{ c.last_name }}
              </option>
            </select>
          </div>
          <div class="form-field">
            <label>Poliçe No</label>
            <input v-model="form.policy_number" type="text" />
          </div>
          <div class="form-field">
            <label>Tür</label>
            <select v-model="form.type">
              <option value="saglik">Sağlık</option>
              <option value="hayat">Hayat</option>
              <option value="kasko">Kasko</option>
              <option value="konut">Konut</option>
            </select>
          </div>
          <div class="form-field">
            <label>Prim (TL)</label>
            <input v-model.number="form.premium" type="number" />
          </div>
          <div class="form-field">
            <label>Teminat (TL)</label>
            <input v-model.number="form.coverage_amount" type="number" />
          </div>
          <div class="form-field">
            <label>Başlangıç Tarihi</label>
            <input v-model="form.start_date" type="date" />
          </div>
          <div class="form-field">
            <label>Bitiş Tarihi</label>
            <input v-model="form.end_date" type="date" />
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showForm = false">Vazgeç</button>
          <button class="btn btn-primary" @click="create">Kaydet</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import { policyStatusBadgeClass, policyStatusLabel, policyTypeLabel } from '../utils/labels'

const policies = ref([])
const customers = ref([])
const error = ref('')
const showForm = ref(false)

const form = reactive({
  customer_id: '',
  policy_number: '',
  type: 'saglik',
  premium: 0,
  coverage_amount: 0,
  start_date: '',
  end_date: '',
})

function formatCurrency(value) {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(
    value || 0
  )
}

async function load() {
  try {
    const [policiesRes, customersRes] = await Promise.all([
      apiClient.get('/policies'),
      apiClient.get('/customers'),
    ])
    policies.value = policiesRes.data
    customers.value = customersRes.data
  } catch (e) {
    error.value = 'Poliçe listesi alınamadı.'
  }
}

function openCreate() {
  Object.assign(form, {
    customer_id: '',
    policy_number: '',
    type: 'saglik',
    premium: 0,
    coverage_amount: 0,
    start_date: '',
    end_date: '',
  })
  showForm.value = true
}

async function create() {
  try {
    await apiClient.post('/policies', form)
    showForm.value = false
    await load()
  } catch (e) {
    error.value = 'Poliçe oluşturulamadı. Alanları kontrol edin.'
  }
}

async function remove(id) {
  try {
    await apiClient.delete(`/policies/${id}`)
    await load()
  } catch (e) {
    error.value = 'Poliçe silinemedi.'
  }
}

onMounted(load)
</script>
