# Vercel setup (quick steps)

Bu proje için otomatik deploy CI adımı opsiyoneldir. En hızlı yol:

1) Vercel hesabına giriş yapın ve yeni bir proje oluşturun (GitHub entegrasyonu önerilir).

2) Vercel token oluşturma:
   - Vercel dashboard > Settings > Tokens > Create Token
   - Token'ı kopyalayın (bir daha gösterilmeyebilir).

3) GitHub repository için Secrets ekleyin:
   - Repository > Settings > Secrets and variables > Actions > New repository secret
   - Anahtar ve değerler:
     - `VERCEL_TOKEN` = (eksikse buraya yapıştırın)
     - `VERCEL_ORG_ID` = (isteğe bağlı; Vercel ekibiniz/org id'si)
     - `VERCEL_PROJECT_ID` = (isteğe bağlı; proje id'si)

   Not: CI job'u `VERCEL_TOKEN` var ise `vercel --prod --token $VERCEL_TOKEN` komutunu çalıştırır. `ORG_ID`/`PROJECT_ID` opsiyoneldir.

4) Çevresel değişkenleri Vercel proje ayarlarına ekleyin (Environment Variables):
   - `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2`, `RAPIDAPI_KEY`, `GOOGLE_AI_API_KEY`, `REDIS_URL`, `SUPABASE_URL`, `SUPABASE_KEY`

5) Manuel deploy (lokal) — hızlı test için:

```powershell
# Vercel CLI kurulu değilse:
npm install -g vercel

# Login
vercel login

# Proje klasöründen
vercel --prod --confirm --token YOUR_TOKEN_HERE
```

Hızlı notlar:
- Otomatik CI deploy yalnızca `main` dalından çalışacak (daha az gürültü).
- Eğer Vercel yerine Render/Heroku kullanmayı tercih ederseniz `Dockerfile` aynı şekilde işe yarar.
