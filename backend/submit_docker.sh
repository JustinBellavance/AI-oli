gcloud builds submit --tag gcr.io/ai-oli-453119/fastapi-backend

gcloud run deploy fastapi-backend \
  --image gcr.io/ai-oli-453119/fastapi-backend \
  --platform managed \
  --region us-central1 \
  --memory 2G \
  --env-vars-file .env.yaml \
  --allow-unauthenticated
