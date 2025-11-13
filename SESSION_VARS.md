# Session Variables & Environment Handoff

Bu dosya, sonraki asistanların ve geliştiricilerin CI/CD, yerel çalıştırma ve oturum (session) bilgilerini güncellerken nelere dikkat etmesi gerektiğini açıklar.

Önemli değişkenler (env vars)
- `RAPIDAPI_KEY`, `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2` — RapidAPI anahtarları (api-football).
- `GOOGLE_AI_API_KEY` — Gemini / Google Generative AI anahtarı.
- `REDIS_URL` — (opsiyonel) Redis cache bağlantısı.
- `SUPABASE_URL`, `SUPABASE_KEY` — (opsiyonel) persistent cache / DB.
- `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` — (opsiyonel) CI deploy için Vercel.
- `PROMPT_VERSION` — (opsiyonel) `v1` veya `v2` seçimi; prod A/B testleri için kullanılır.

Gizlilik ve güvenlik
- Bu değerleri `.env` içinde yerel makinede tutun; asla doğrudan repoya commit etmeyin.
- CI sırlarına (`Secrets`) yalnızca GitHub repo ayarları üzerinden ekleyin.

Güncelleme adımları (hangi dosyaları değiştirin)
1. Yerel test veya geliştirme için: `.env` dosyasına örnek değerleri ekleyin. Örnek için `.env.example` oluşturun, gerçek secret koymayın.
2. Prod/CI: GitHub -> Settings -> Secrets -> Actions içine ilgili anahtarları ekleyin.
3. `memory/context.md` içinde "CURRENT_SESSION" ve `SESSION_NOTES` bölümlerini güncelleyin. (Bu repo'da `memory/context.md` bulunur; session tarihini, yapılan değişiklikleri ve hangi secretların eklendiğini yazın.)
4. `TODO_NEXT_AGENT.md` içinde "Session Notes" bölümünü güncelleyin (hangi env vars eklendi, hangi testler çalıştırıldı).

Kontrol listesi (önceden deploy etmeden önce)
- [ ] `RAPIDAPI_KEY` test keys veya rate-limit uyarıları kontrol edildi.
- [ ] `GOOGLE_AI_API_KEY` prod için doğrulandı (rate/quotas gözlemlendi).
- [ ] `VERCEL_TOKEN` ve ilgili IDs ayarlandıysa deploy test edildi.
- [ ] `PROMPT_VERSION` default değeri repoda belirtilmiş mi (örn. `v2`)?

Hızlı komutlar
```powershell
# Local .env örneği oluştur
copy .env.example .env
# (PowerShell) .venv aktif etme
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r services/feature-002-ai-predictor/requirements.txt
# CI secrets eklenince lokal test
pytest -q services/feature-002-ai-predictor/tests/
```

Not: Bu dosya sadece rehber amaçlıdır — gerçek secret değerleri asla buraya veya repo'ya yazmayın.
