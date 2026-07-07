# SabancıDx - AgeSA Azure Day – Demo Uygulaması

Kubernetes deploy demosu için hazırlanmış, dockerize edilmiş sigortacılık örnek uygulaması.

- **Backend:** Python / FastAPI + SQLAlchemy (PostgreSQL)
- **Frontend:** Vue 3 + Vite, derlenip FastAPI tarafından statik dosya olarak servis edilir
- **Veritabanı:** PostgreSQL (bu demoda **Azure Database for PostgreSQL** kullanılacak; yerel bir DB container'ı bu repoda yok)

Kapsam: Müşteriler, Poliçeler (sağlık / hayat / kasko / konut) ve Hasar Talepleri üzerinde CRUD + basit bir gösterge paneli.

## Klasör Yapısı

```
Dockerfile  Backend + Frontend tek imaj build (repo kökünde, tek Dockerfile)
backend/    FastAPI servisi
frontend/   Vue 3 + Vite SPA
```

Not: Artık ayrı `backend/Dockerfile` ve `frontend/Dockerfile` yoktur; imaj build'i tek bir kök `Dockerfile` üzerinden yapılır (bkz. bölüm 4).

## 1) Azure Database for PostgreSQL Hazırlığı

- Bir Azure Database for PostgreSQL Flexible Server (veya Single Server) oluşturun.
- Sunucu güvenlik duvarında, deploy edeceğiniz ortamın (yerel makine / AKS düğümleri / dış IP) erişimine izin verin.
- Bağlantı dizesini not alın:

```
postgresql://<kullanici>:<parola>@<sunucu-adi>.postgres.database.azure.com:5432/<veritabani>?sslmode=require
```

## 2) Backend'i Çalıştırma

Uygulama açılışta tabloları otomatik oluşturur (`Base.metadata.create_all`) ve veritabanı boşsa örnek veri ekler (`app/seed.py`).

Backend'i tek başına Docker imajı olarak build etmek istemiyorsanız (artık ayrı bir `backend/Dockerfile` yoktur), aşağıdaki yerel çalıştırma yöntemini kullanın ya da doğrudan bölüm 4'teki birleşik imajı build edin.

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

Üretimde frontend ayrı bir imaj/Nginx olarak değil; `npm run build` ile derlenip çıktısı (`dist/`) kök `Dockerfile` tarafından backend imajının içine (`app/static`) kopyalanarak FastAPI üzerinden servis edilir (bkz. bölüm 4). Frontend'in artık kendine ait bir `Dockerfile`'ı yoktur.

### Yerel geliştirme (Docker olmadan)

```powershell
cd frontend
npm install
$env:VITE_DEV_API_TARGET = "http://localhost:8000"
npm run dev
```

Vite dev server `http://localhost:5173` adresinde çalışır ve `/api` isteklerini `VITE_DEV_API_TARGET`'a proxy'ler.

## 4) Docker ile Çalıştırma (Tek İmaj)

Backend ve frontend, repo kökündeki tek bir `Dockerfile` ile tek bir imaj olarak build edilir: frontend derlenir (`npm run build`) ve çıktısı FastAPI'nin static dosyaları olarak (`app/static`) imaja kopyalanır. Ayrı bir Nginx/proxy katmanı yoktur; `/api/*` ve statik dosyalar aynı uvicorn süreci tarafından sunulur.

```powershell
docker build -t agesa-demo-app .
docker run -d --name guven-app -p 8000:8000 `
  -e DATABASE_URL="postgresql://<kullanici>:<parola>@<sunucu-adi>.postgres.database.azure.com:5432/<veritabani>?sslmode=require" `
  agesa-demo-app
```

Uygulama ve API: http://localhost:8000 (frontend `/`, API `/api/*`)

Kubernetes deploy demosu için de bu tek imaj kullanılacaktır; imaj build edilip istediğiniz registry'ye push edildikten sonra deploy adımında manifestler bu imaj referans alınarak hazırlanır.

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

## 5) Kubernetes'e Deploy Etme

`k8s/` klasöründe AKS (veya herhangi bir Kubernetes kümesi) için hazır manifestler bulunur:

| Dosya | Açıklama |
|-------|----------|
| `00-namespace.yaml` | `agesa-demo` namespace'i |
| `01-secret.yaml` | `DATABASE_URL` için Secret (demo amaçlı; değerleri kendi bağlantı dizenizle değiştirin) |
| `02-deployment.yaml` | Uygulama Deployment'ı (2 replica, `/health` üzerinden readiness/liveness probe) |
| `03-service.yaml` | ClusterIP Service (port 80 → 8000) |
| `04-ingress.yaml` | NGINX Ingress (host: `demo.agesa.com`) |
| `kustomization.yaml` | Tüm manifestleri tek komutla uygulamak için |

### Ön koşullar

1. İmajı build edip bir Azure Container Registry'ye (ACR) push edin:

```powershell
az acr build --registry <acr-adi> --image agesa-demo-app:latest .
```

2. `k8s/02-deployment.yaml` içindeki `<acr-adi>.azurecr.io/agesa-demo-app:latest` referansını kendi ACR adınızla güncelleyin.
3. AKS kümenizin ACR'dan imaj çekebilmesi için gerekli izni tanımlayın (`az aks update -n <aks-adi> -g <rg> --attach-acr <acr-adi>`).
4. `k8s/01-secret.yaml` içindeki `DATABASE_URL` değerini kendi Azure Database for PostgreSQL bağlantı dizenizle değiştirin.
5. Küme üzerinde bir NGINX Ingress Controller kurulu olmalı (Ingress kullanmak istemiyorsanız `04-ingress.yaml`'ı kustomization'dan çıkarıp `03-service.yaml`'ı `type: LoadBalancer` yapabilirsiniz).

### Deploy

```powershell
kubectl apply -k k8s/
```

Durumu kontrol etmek için:

```powershell
kubectl get pods,svc,ingress -n agesa-demo
```

Ingress kullanıyorsanız `demo.agesa.com` domainini Ingress'in dış IP'sine yönlendirmeniz (DNS ya da yerel `hosts` dosyası) gerekir.

## Notlar

- Bu bir demo uygulamasıdır; kimlik doğrulama, girdi doğrulama derinliği ve prod-seviyesi güvenlik sertleştirmeleri kapsam dışıdır.
- CORS backend'de `*` olarak açık bırakılmıştır (yalnızca demo amaçlı).
- `k8s/01-secret.yaml` demo/örnek amaçlıdır; gerçek kimlik bilgilerini repoya committ etmeyin, gerekirse `kubectl create secret` ile imperative olarak oluşturun.
