export const policyTypeLabels = {
  saglik: 'Sağlık',
  hayat: 'Hayat',
  kasko: 'Kasko',
  konut: 'Konut',
}

export const policyStatusLabels = {
  aktif: 'Aktif',
  askida: 'Askıda',
  iptal: 'İptal',
  sona_erdi: 'Sona Erdi',
}

export const claimStatusLabels = {
  beklemede: 'Beklemede',
  inceleniyor: 'İnceleniyor',
  onaylandi: 'Onaylandı',
  reddedildi: 'Reddedildi',
}

export function policyTypeLabel(value) {
  return policyTypeLabels[value] || value
}

export function policyStatusLabel(value) {
  return policyStatusLabels[value] || value
}

export function claimStatusLabel(value) {
  return claimStatusLabels[value] || value
}

export function claimStatusBadgeClass(value) {
  switch (value) {
    case 'onaylandi':
      return 'badge-success'
    case 'reddedildi':
      return 'badge-danger'
    case 'inceleniyor':
      return 'badge-warning'
    default:
      return 'badge-muted'
  }
}

export function policyStatusBadgeClass(value) {
  switch (value) {
    case 'aktif':
      return 'badge-success'
    case 'iptal':
      return 'badge-danger'
    case 'askida':
      return 'badge-warning'
    default:
      return 'badge-muted'
  }
}
