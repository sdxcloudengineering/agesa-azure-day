<template>
  <div>
    <div class="section-header">
      <div>
        <h1>Hasar Talepleri</h1>
        <p class="page-subtitle">Bildirilen hasarları görüntüleyin ve yönetin</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ Yeni Hasar Talebi</button>
    </div>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <div class="card">
      <table v-if="claims.length">
        <thead>
          <tr>
            <th>Talep No</th>
            <th>Poliçe No</th>
            <th>Açıklama</th>
            <th>Tutar</th>
            <th>Durum</th>
            <th>Olay Tarihi</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in claims" :key="c.id">
            <td>{{ c.claim_number }}</td>
            <td>{{ c.policy ? c.policy.policy_number : '—' }}</td>
            <td>{{ c.description }}</td>
            <td>{{ formatCurrency(c.amount) }}</td>
            <td><span class="badge" :class="claimStatusBadgeClass(c.status)">{{ claimStatusLabel(c.status) }}</span></td>
            <td>{{ c.incident_date }}</td>
            <td>
              <button class="btn btn-danger" @click="remove(c.id)">Sil</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">Henüz hasar talebi yok.</div>
    </div>

    <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
      <div class="modal">
        <h3>Yeni Hasar Talebi</h3>
        <div class="form-grid">
          <div class="form-field full">
            <label>Poliçe</label>
            <select v-model="form.policy_id">
              <option value="" disabled>Seçiniz</option>
              <option v-for="p in policies" :key="p.id" :value="p.id">
                {{ p.policy_number }}
              </option>
            </select>
          </div>
          <div class="form-field full">
            <label>Açıklama</label>
            <textarea v-model="form.description" rows="2"></textarea>
          </div>
          <div class="form-field">
            <label>Tutar (TL)</label>
            <input v-model.number="form.amount" type="number" />
          </div>
          <div class="form-field">
            <label>Olay Tarihi</label>
            <input v-model="form.incident_date" type="date" />
          </div>
          <div class="form-field">
            <label>Durum</label>
            <select v-model="form.status">
              <option value="beklemede">Beklemede</option>
              <option value="inceleniyor">İnceleniyor</option>
              <option value="onaylandi">Onaylandı</option>
              <option value="reddedildi">Reddedildi</option>
            </select>
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
import { claimStatusBadgeClass, claimStatusLabel } from '../utils/labels'

const claims = ref([])
const policies = ref([])
const error = ref('')
const showForm = ref(false)

const form = reactive({
  policy_id: '',
  description: '',
  amount: 0,
  incident_date: '',
  status: 'beklemede',
})

function formatCurrency(value) {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(
    value || 0
  )
}

async function load() {
  try {
    const [claimsRes, policiesRes] = await Promise.all([
      apiClient.get('/claims'),
      apiClient.get('/policies'),
    ])
    claims.value = claimsRes.data
    policies.value = policiesRes.data
  } catch (e) {
    error.value = 'Hasar talebi listesi alınamadı.'
  }
}

function openCreate() {
  Object.assign(form, {
    policy_id: '',
    description: '',
    amount: 0,
    incident_date: '',
    status: 'beklemede',
  })
  showForm.value = true
}

async function create() {
  try {
    await apiClient.post('/claims', form)
    showForm.value = false
    await load()
  } catch (e) {
    error.value = 'Hasar talebi oluşturulamadı. Alanları kontrol edin.'
  }
}

async function remove(id) {
  try {
    await apiClient.delete(`/claims/${id}`)
    await load()
  } catch (e) {
    error.value = 'Hasar talebi silinemedi.'
  }
}

onMounted(load)
</script>
