<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <img :src="logo" alt="AgeSA" class="brand-logo" />
      </div>
      <nav class="nav">
        <RouterLink to="/" class="nav-link">📊 Genel Bakış</RouterLink>
        <RouterLink to="/musteriler" class="nav-link">👤 Müşteriler</RouterLink>
        <RouterLink to="/policeler" class="nav-link">📄 Poliçeler</RouterLink>
        <RouterLink to="/hasarlar" class="nav-link">⚠️ Hasar Talepleri</RouterLink>
      </nav>
    </aside>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import logo from './agesa-sigorta-seeklogo.svg'
</script>
