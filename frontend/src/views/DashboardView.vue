<template>
  <div>
    <h1>Genel Bakış</h1>
    <p class="page-subtitle">AgeSA Demo portföy özeti</p>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <div v-if="stats" class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Toplam Müşteri</div>
        <div class="stat-value">{{ stats.total_customers }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Toplam Poliçe</div>
        <div class="stat-value">{{ stats.total_policies }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Aktif Poliçe</div>
        <div class="stat-value">{{ stats.active_policies }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Bekleyen Hasar Talebi</div>
        <div class="stat-value">{{ stats.pending_claims }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Toplam Prim Geliri</div>
        <div class="stat-value">{{ formatCurrency(stats.total_premium) }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Toplam Hasar Tutarı</div>
        <div class="stat-value">{{ formatCurrency(stats.total_claim_amount) }}</div>
      </div>
    </div>

    <div v-if="stats" class="card" style="margin-bottom: 20px;">
      <div class="section-header"><strong>Poliçe Türlerine Göre Dağılım</strong></div>
      <table>
        <thead>
          <tr><th>Tür</th><th>Adet</th></tr>
        </thead>
        <tbody>
          <tr v-for="(count, type) in stats.policies_by_type" :key="type">
            <td>{{ policyTypeLabel(type) }}</td>
            <td>{{ count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="stats" class="card">
      <div class="section-header"><strong>Hasar Durumlarına Göre Dağılım</strong></div>
      <table>
        <thead>
          <tr><th>Durum</th><th>Adet</th></tr>
        </thead>
        <tbody>
          <tr v-for="(count, status) in stats.claims_by_status" :key="status">
            <td>{{ claimStatusLabel(status) }}</td>
            <td>{{ count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import apiClient from '../api/client'
import { claimStatusLabel, policyTypeLabel } from '../utils/labels'

const stats = ref(null)
const error = ref('')

function formatCurrency(value) {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(
    value || 0
  )
}

onMounted(async () => {
  try {
    const { data } = await apiClient.get('/stats/dashboard')
    stats.value = data
  } catch (e) {
    error.value = 'Veriler alınamadı. Backend servisine ulaşılamıyor.'
  }
})
</script>
