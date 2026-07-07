<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-icon">🛡️</span>
        <span class="brand-name">AgeSA Demo</span>
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
</script>
