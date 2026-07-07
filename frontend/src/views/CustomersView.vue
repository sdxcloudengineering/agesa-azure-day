<template>
  <div>
    <div class="section-header">
      <div>
        <h1>Müşteriler</h1>
        <p class="page-subtitle">Tüm poliçe sahiplerini görüntüleyin ve yönetin</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ Yeni Müşteri</button>
    </div>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <div class="card">
      <table v-if="customers.length">
        <thead>
          <tr>
            <th>Ad Soyad</th>
            <th>TC Kimlik No</th>
            <th>E-posta</th>
            <th>Telefon</th>
            <th>Şehir</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in customers" :key="c.id">
            <td>{{ c.first_name }} {{ c.last_name }}</td>
            <td>{{ c.tc_no }}</td>
            <td>{{ c.email }}</td>
            <td>{{ c.phone }}</td>
            <td>{{ c.city }}</td>
            <td>
              <button class="btn btn-danger" @click="remove(c.id)">Sil</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">Henüz müşteri kaydı yok.</div>
    </div>

    <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
      <div class="modal">
        <h3>Yeni Müşteri</h3>
        <div class="form-grid">
          <div class="form-field">
            <label>Ad</label>
            <input v-model="form.first_name" type="text" />
          </div>
          <div class="form-field">
            <label>Soyad</label>
            <input v-model="form.last_name" type="text" />
          </div>
          <div class="form-field">
            <label>TC Kimlik No</label>
            <input v-model="form.tc_no" type="text" maxlength="11" />
          </div>
          <div class="form-field">
            <label>Doğum Tarihi</label>
            <input v-model="form.birth_date" type="date" />
          </div>
          <div class="form-field">
            <label>E-posta</label>
            <input v-model="form.email" type="email" />
          </div>
          <div class="form-field">
            <label>Telefon</label>
            <input v-model="form.phone" type="text" />
          </div>
          <div class="form-field full">
            <label>Şehir</label>
            <input v-model="form.city" type="text" />
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

const customers = ref([])
const error = ref('')
const showForm = ref(false)

const form = reactive({
  first_name: '',
  last_name: '',
  tc_no: '',
  birth_date: '',
  email: '',
  phone: '',
  city: '',
})

async function load() {
  try {
    const { data } = await apiClient.get('/customers')
    customers.value = data
  } catch (e) {
    error.value = 'Müşteri listesi alınamadı.'
  }
}

function openCreate() {
  Object.assign(form, {
    first_name: '',
    last_name: '',
    tc_no: '',
    birth_date: '',
    email: '',
    phone: '',
    city: '',
  })
  showForm.value = true
}

async function create() {
  try {
    await apiClient.post('/customers', form)
    showForm.value = false
    await load()
  } catch (e) {
    error.value = 'Müşteri oluşturulamadı. Alanları kontrol edin.'
  }
}

async function remove(id) {
  try {
    await apiClient.delete(`/customers/${id}`)
    await load()
  } catch (e) {
    error.value = 'Müşteri silinemedi.'
  }
}

onMounted(load)
</script>
