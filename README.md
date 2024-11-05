gcloud builds submit --tag gcr.io/chatbotproject-440711/CHATBOTPROJECT --project=chatbotproject-440711
gcloud run deploy my-app --image gcr.io/chatbotproject-440711/CHATBOTPROJECT:latest --platform managed --project=chatbotproject-440711
