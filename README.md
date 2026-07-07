# Güven Sigorta – Demo Uygulaması

Kubernetes deploy demosu için hazırlanmış, dockerize edilmiş sigortacılık örnek uygulaması.

- **Backend:** Python / FastAPI + SQLAlchemy (PostgreSQL)
- **Frontend:** Vue 3 + Vite, üretimde Nginx üzerinden servis edilir
- **Veritabanı:** PostgreSQL (bu demoda **Azure Database for PostgreSQL** kullanılacak; yerel bir DB container'ı bu repoda yok)

Kapsam: Müşteriler, Poliçeler (sağlık / hayat / kasko / konut) ve Hasar Talepleri üzerinde CRUD + basit bir gösterge paneli.

## Klasör Yapısı

```
backend/    FastAPI servisi + Dockerfile
frontend/   Vue 3 + Vite SPA + Dockerfile (Nginx runtime)
```

## 1) Azure Database for PostgreSQL Hazırlığı

- Bir Azure Database for PostgreSQL Flexible Server (veya Single Server) oluşturun.
- Sunucu güvenlik duvarında, deploy edeceğiniz ortamın (yerel makine / AKS düğümleri / dış IP) erişimine izin verin.
- Bağlantı dizesini not alın:

```
postgresql://<kullanici>:<parola>@<sunucu-adi>.postgres.database.azure.com:5432/<veritabani>?sslmode=require
```

## 2) Backend'i Çalıştırma

Uygulama açılışta tabloları otomatik oluşturur (`Base.metadata.create_all`) ve veritabanı boşsa örnek veri ekler (`app/seed.py`).

### Docker ile

```powershell
cd backend
docker build -t guven-sigorta-backend .
docker run -d --name guven-backend -p 8000:8000 `
  -e DATABASE_URL="postgresql://<kullanici>:<parola>@<sunucu-adi>.postgres.database.azure.com:5432/<veritabani>?sslmode=require" `
  guven-sigorta-backend
```

API dokümantasyonu: http://localhost:8000/docs
Health check: http://localhost:8000/health

### Yerel olarak (Docker olmadan)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL = "postgresql://<kullanici>:<parola>@<sunucu-adi>.postgres.database.azure.com:5432/<veritabani>?sslmode=require"
uvicorn app.main:app --reload
```

## 3) Frontend'i Çalıştırma

Üretim imajı, statik dosyaları Nginx ile servis eder ve `/api/*` isteklerini `BACKEND_HOST`/`BACKEND_PORT` ortam değişkenleriyle belirtilen backend'e proxy'ler. Bu sayede aynı imaj hem Docker'da hem de yarınki Kubernetes ortamında (Service adını `BACKEND_HOST` olarak vererek) değişiklik yapmadan kullanılabilir.

### Docker ile

```powershell
cd frontend
docker build -t guven-sigorta-frontend .

# Backend'i ayrı bir container olarak çalıştırdıysanız, aynı Docker network'üne alın:
docker network create guven-net
docker network connect guven-net guven-backend

docker run -d --name guven-frontend --network guven-net -p 8080:80 `
  -e BACKEND_HOST=guven-backend `
  -e BACKEND_PORT=8000 `
  guven-sigorta-frontend
```

Uygulama: http://localhost:8080

### Yerel geliştirme (Docker olmadan)

```powershell
cd frontend
npm install
$env:VITE_DEV_API_TARGET = "http://localhost:8000"
npm run dev
```

Vite dev server `http://localhost:5173` adresinde çalışır ve `/api` isteklerini `VITE_DEV_API_TARGET`'a proxy'ler.

## 4) Tek İmaj (Backend + Frontend Birlikte)

Basit tek-konteyner demolar için, frontend derlenip doğrudan FastAPI üzerinden servis edilecek şekilde tek bir imaj da üretilebilir (repo kökündeki `Dockerfile`). Bu modda ayrı bir Nginx/proxy katmanı yoktur; `/api/*` ve statik dosyalar aynı uvicorn süreci tarafından sunulur.

```powershell
docker build -t guven-sigorta-app -f Dockerfile .
docker run -d --name guven-app -p 8000:8000 `
  -e DATABASE_URL="postgresql://<kullanici>:<parola>@<sunucu-adi>.postgres.database.azure.com:5432/<veritabani>?sslmode=require" `
  guven-sigorta-app
```

Uygulama ve API: http://localhost:8000 (frontend `/`, API `/api/*`)

Not: Kubernetes demosu için hâlâ `backend/Dockerfile` + `frontend/Dockerfile` (Nginx reverse proxy) ayrı imaj yaklaşımı önerilir; tek imaj seçeneği yalnızca hızlı/basit çalıştırmalar içindir.

## API Uç Noktaları (özet)

| Yöntem | Yol                     | Açıklama                    |
|--------|--------------------------|-----------------------------|
| GET/POST | /api/customers         | Müşteri listele / oluştur   |
| GET/PUT/DELETE | /api/customers/{id} | Müşteri detay / güncelle / sil |
| GET/POST | /api/policies          | Poliçe listele / oluştur    |
| GET/PUT/DELETE | /api/policies/{id}  | Poliçe detay / güncelle / sil |
| GET/POST | /api/claims            | Hasar talebi listele / oluştur |
| GET/PUT/DELETE | /api/claims/{id}    | Hasar talebi detay / güncelle / sil |
| GET | /api/stats/dashboard        | Gösterge paneli özet istatistikleri |
| GET | /health                     | Sağlık kontrolü |

## Notlar

- Bu bir demo uygulamasıdır; kimlik doğrulama, girdi doğrulama derinliği ve prod-seviyesi güvenlik sertleştirmeleri kapsam dışıdır.
- CORS backend'de `*` olarak açık bırakılmıştır (yalnızca demo amaçlı).
- Kubernetes manifestleri bu aşamada bilinçli olarak eklenmemiştir; imajlar `docker build` ile üretilip istediğiniz registry'ye push edildikten sonra yarınki deploy adımında manifestler ayrıca hazırlanabilir.
