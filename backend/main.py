from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uvicorn

# Initialize Firebase Admin SDK
cred_path = "../gcloud_setup/serviceAccount.json"
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'f1-management-bucket.appspot.com'
})

app = FastAPI(title="F1 Management App")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Get Firestore client
db = firestore.client()

# Function to create admin user
def create_admin_user():
    email = "admin@gmail.com"
    password = "admin123"
    
    try:
        # Check if the user already exists
        user = auth.get_user_by_email(email)
        print(f"Admin user already exists: {user.email}")
    except auth.UserNotFoundError:
        # Create the admin user
        user = auth.create_user(
            email=email,
            password=password,
        )
        print(f"Admin user created: {user.email}")

# Call the function to create admin user when the server starts
create_admin_user()

# Import routes
from routes.drivers import router as drivers_router
from routes.teams import router as teams_router
from routes.queries import router as queries_router
from routes.auth import router as auth_router

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(drivers_router, prefix="/api/drivers", tags=["Drivers"])
app.include_router(teams_router, prefix="/api/teams", tags=["Teams"])
app.include_router(queries_router, prefix="/api/queries", tags=["Queries"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "F1 Management API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)