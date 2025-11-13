FROM python:3.11-slim

# Set working dir and copy repository
WORKDIR /app
COPY . /app

# Upgrade pip and install requirements (fall back if file missing)
RUN python -m pip install --upgrade pip
RUN if [ -f services/feature-002-ai-predictor/requirements.txt ]; then pip install -r services/feature-002-ai-predictor/requirements.txt; fi
RUN pip install gunicorn

# Run from the feature directory so imports using hyphenated folder work when
# importing `app` as a module.
WORKDIR /app/services/feature-002-ai-predictor

ENV FLASK_ENV=production
EXPOSE 5000

# Start with gunicorn binding to 0.0.0.0:5000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers", "1", "--timeout", "120"]
