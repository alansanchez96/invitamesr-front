from fastapi import FastAPI, HTTPException, Request, Response, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
import uuid
import httpx
import logging

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="INVITAME SR API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/invitame_db")
db_client = None
db = None

# Stripe Configuration
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_emergent")

# MercadoPago Configuration
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")

# ==================== DATABASE CONNECTION ====================

@app.on_event("startup")
async def startup_db():
    global db_client, db
    try:
        db_client = AsyncIOMotorClient(MONGO_URL)
        db = db_client.get_database()
        await db_client.admin.command('ping')
        logger.info("✅ Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db():
    if db_client:
        db_client.close()
        logger.info("MongoDB connection closed")

# ==================== PYDANTIC MODELS ====================

class User(BaseModel):
    user_id: str
    email: str
    name: str
    picture: str
    created_at: datetime

class UserSession(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

class InvitationCustomData(BaseModel):
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    event_date: Optional[str] = None
    venue: Optional[str] = None
    message: Optional[str] = None
    dress_code: Optional[str] = None

class Invitation(BaseModel):
    invitation_id: str
    user_id: str
    event_type: str
    template_id: str
    custom_data: InvitationCustomData
    status: str = "draft"
    created_at: datetime
    updated_at: datetime

class PaymentTransaction(BaseModel):
    transaction_id: str
    user_id: str
    invitation_id: str
    amount: float
    currency: str
    payment_method: str
    payment_provider_id: Optional[str] = None
    session_id: Optional[str] = None
    status: str = "pending"
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

# ==================== REQUEST/RESPONSE MODELS ====================

class SessionRequest(BaseModel):
    session_id: str

class CreateInvitationRequest(BaseModel):
    event_type: str
    template_id: str
    custom_data: InvitationCustomData

class UpdateInvitationRequest(BaseModel):
    custom_data: InvitationCustomData

class StripeCheckoutRequest(BaseModel):
    invitation_id: str
    plan_type: str
    origin_url: str

class MercadoPagoCheckoutRequest(BaseModel):
    invitation_id: str
    plan_type: str
    origin_url: str

# ==================== HELPER FUNCTIONS ====================

def generate_user_id() -> str:
    return f"user_{uuid.uuid4().hex[:12]}"

def generate_invitation_id() -> str:
    return f"inv_{uuid.uuid4().hex[:12]}"

def generate_transaction_id() -> str:
    return f"txn_{uuid.uuid4().hex[:12]}"

async def get_current_user(
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = None
) -> Dict[str, Any]:
    """Get current authenticated user from session token"""
    token = None
    
    # Try to get token from Authorization header
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Find session in database
    session_doc = await db.user_sessions.find_one(
        {"session_token": token},
        {"_id": 0}
    )
    
    if not session_doc:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check if session expired
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Get user data
    user_doc = await db.users.find_one(
        {"user_id": session_doc["user_id"]},
        {"_id": 0}
    )
    
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_doc

# Mock data for plans
PLANS = {
    "basic": {"name": "Basic", "price": 2500.0, "currency": "ARS", "type": "one_time"},
    "pro": {"name": "PRO", "price": 5000.0, "currency": "ARS", "type": "one_time"},
    "planner": {"name": "Planner", "price": 1500.0, "currency": "ARS", "type": "subscription"}
}

# Mock data for event types
EVENT_TYPES = [
    {
        "id": "boda",
        "name": "Boda",
        "description": "Invitaciones elegantes para tu día especial",
        "icon": "💍"
    }
]

# Mock data for templates
TEMPLATES = {
    "boda": [
        {
            "id": "template_1",
            "name": "Elegancia Clásica",
            "description": "Diseño atemporal con detalles dorados",
            "preview_url": "https://via.placeholder.com/400x600/000851/FFFFFF?text=Elegancia+Clásica"
        },
        {
            "id": "template_2",
            "name": "Romance Moderno",
            "description": "Estilo contemporáneo con toques románticos",
            "preview_url": "https://via.placeholder.com/400x600/D4AF37/FFFFFF?text=Romance+Moderno"
        }
    ]
}

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/auth/session")
async def process_session(request: SessionRequest, response: Response):
    """
    Process session_id from Emergent Auth and create user session
    REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    """
    try:
        # Call Emergent Auth API to get session data
        async with httpx.AsyncClient() as client:
            auth_response = await client.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": request.session_id}
            )
            
            if auth_response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid session_id")
            
            session_data = auth_response.json()
        
        # Check if user exists
        existing_user = await db.users.find_one(
            {"email": session_data["email"]},
            {"_id": 0}
        )
        
        if existing_user:
            user_id = existing_user["user_id"]
            # Update user info
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {
                    "name": session_data["name"],
                    "picture": session_data["picture"]
                }}
            )
        else:
            # Create new user
            user_id = generate_user_id()
            user_doc = {
                "user_id": user_id,
                "email": session_data["email"],
                "name": session_data["name"],
                "picture": session_data["picture"],
                "created_at": datetime.now(timezone.utc)
            }
            await db.users.insert_one(user_doc)
        
        # Create session
        session_token = session_data["session_token"]
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        session_doc = {
            "user_id": user_id,
            "session_token": session_token,
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc)
        }
        
        await db.user_sessions.insert_one(session_doc)
        
        # Set httpOnly cookie
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/",
            max_age=7*24*60*60
        )
        
        # Get user data
        user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
        
        return {
            "success": True,
            "user": user,
            "session_token": session_token
        }
        
    except Exception as e:
        logger.error(f"Session processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/me")
async def get_current_user_info(user: Dict = Depends(get_current_user)):
    """Get current authenticated user information"""
    return user

@app.post("/api/auth/logout")
async def logout(response: Response, user: Dict = Depends(get_current_user)):
    """Logout user and clear session"""
    try:
        # Delete session from database
        await db.user_sessions.delete_many({"user_id": user["user_id"]})
        
        # Clear cookie
        response.delete_cookie(key="session_token", path="/")
        
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== EVENT & TEMPLATE ENDPOINTS ====================

@app.get("/api/events")
async def get_events():
    """Get all available event types"""
    return {"events": EVENT_TYPES}

@app.get("/api/events/{event_type}/templates")
async def get_templates(event_type: str):
    """Get templates for specific event type"""
    templates = TEMPLATES.get(event_type, [])
    return {"templates": templates}

@app.get("/api/plans")
async def get_plans():
    """Get all available pricing plans"""
    return {"plans": PLANS}

# ==================== INVITATION ENDPOINTS ====================

@app.post("/api/invitations")
async def create_invitation(
    request: CreateInvitationRequest,
    user: Dict = Depends(get_current_user)
):
    """Create a new invitation (draft)"""
    try:
        invitation_id = generate_invitation_id()
        
        invitation_doc = {
            "invitation_id": invitation_id,
            "user_id": user["user_id"],
            "event_type": request.event_type,
            "template_id": request.template_id,
            "custom_data": request.custom_data.dict(),
            "status": "draft",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        await db.invitations.insert_one(invitation_doc)
        
        invitation_doc.pop("_id", None)
        return {"success": True, "invitation": invitation_doc}
        
    except Exception as e:
        logger.error(f"Create invitation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/invitations/{invitation_id}")
async def get_invitation(invitation_id: str, user: Dict = Depends(get_current_user)):
    """Get specific invitation"""
    invitation = await db.invitations.find_one(
        {"invitation_id": invitation_id, "user_id": user["user_id"]},
        {"_id": 0}
    )
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    return invitation

@app.put("/api/invitations/{invitation_id}")
async def update_invitation(
    invitation_id: str,
    request: UpdateInvitationRequest,
    user: Dict = Depends(get_current_user)
):
    """Update invitation data"""
    try:
        result = await db.invitations.update_one(
            {"invitation_id": invitation_id, "user_id": user["user_id"]},
            {"$set": {
                "custom_data": request.custom_data.dict(),
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        invitation = await db.invitations.find_one(
            {"invitation_id": invitation_id},
            {"_id": 0}
        )
        
        return {"success": True, "invitation": invitation}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update invitation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/invitations/{invitation_id}/complete")
async def complete_invitation(invitation_id: str, user: Dict = Depends(get_current_user)):
    """Mark invitation as completed after payment"""
    try:
        result = await db.invitations.update_one(
            {"invitation_id": invitation_id, "user_id": user["user_id"]},
            {"$set": {
                "status": "completed",
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        return {"success": True, "message": "Invitation completed"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Complete invitation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STRIPE PAYMENT ENDPOINTS ====================

@app.post("/api/payments/stripe/checkout")
async def create_stripe_checkout(
    request: StripeCheckoutRequest,
    user: Dict = Depends(get_current_user)
):
    """Create Stripe checkout session"""
    try:
        # Validate invitation exists
        invitation = await db.invitations.find_one(
            {"invitation_id": request.invitation_id, "user_id": user["user_id"]},
            {"_id": 0}
        )
        
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        # Get plan details
        plan = PLANS.get(request.plan_type)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Import Stripe integration
        from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
        
        # Initialize Stripe
        stripe_checkout = StripeCheckout(
            api_key=STRIPE_API_KEY,
            webhook_url=f"{request.origin_url}/api/payments/stripe/webhook"
        )
        
        # Build URLs
        success_url = f"{request.origin_url}/onboarding/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{request.origin_url}/onboarding/payment"
        
        # Create checkout request
        checkout_request = CheckoutSessionRequest(
            amount=plan["price"],
            currency=plan["currency"].lower(),
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": user["user_id"],
                "invitation_id": request.invitation_id,
                "plan_type": request.plan_type
            }
        )
        
        # Create session
        session = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create transaction record
        transaction_id = generate_transaction_id()
        transaction_doc = {
            "transaction_id": transaction_id,
            "user_id": user["user_id"],
            "invitation_id": request.invitation_id,
            "amount": plan["price"],
            "currency": plan["currency"],
            "payment_method": "stripe",
            "session_id": session.session_id,
            "status": "pending",
            "metadata": {
                "plan_type": request.plan_type
            },
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        await db.payment_transactions.insert_one(transaction_doc)
        
        return {"url": session.url, "session_id": session.session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Stripe checkout error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payments/stripe/status/{session_id}")
async def get_stripe_status(session_id: str):
    """Get Stripe payment status"""
    try:
        from emergentintegrations.payments.stripe.checkout import StripeCheckout
        
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
        status_response = await stripe_checkout.get_checkout_status(session_id)
        
        # Update transaction in database
        if status_response.payment_status == "paid":
            result = await db.payment_transactions.update_one(
                {"session_id": session_id, "status": {"$ne": "approved"}},
                {"$set": {
                    "status": "approved",
                    "payment_provider_id": session_id,
                    "updated_at": datetime.now(timezone.utc)
                }}
            )
            
            # If this is the first time we're marking as approved, complete the invitation
            if result.modified_count > 0:
                transaction = await db.payment_transactions.find_one(
                    {"session_id": session_id},
                    {"_id": 0}
                )
                if transaction:
                    await db.invitations.update_one(
                        {"invitation_id": transaction["invitation_id"]},
                        {"$set": {"status": "completed"}}
                    )
        
        return {
            "status": status_response.status,
            "payment_status": status_response.payment_status,
            "amount": status_response.amount_total,
            "currency": status_response.currency
        }
        
    except Exception as e:
        logger.error(f"Get Stripe status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payments/stripe/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        from emergentintegrations.payments.stripe.checkout import StripeCheckout
        
        body = await request.body()
        signature = request.headers.get("Stripe-Signature")
        
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        logger.info(f"Stripe webhook: {webhook_response.event_type}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Stripe webhook error: {e}")
        return JSONResponse({"status": "error"}, status_code=200)

# ==================== MERCADOPAGO PAYMENT ENDPOINTS ====================

@app.post("/api/payments/mercadopago/checkout")
async def create_mercadopago_checkout(
    request: MercadoPagoCheckoutRequest,
    user: Dict = Depends(get_current_user)
):
    """Create MercadoPago checkout preference"""
    try:
        import mercadopago
        
        # Validate invitation exists
        invitation = await db.invitations.find_one(
            {"invitation_id": request.invitation_id, "user_id": user["user_id"]},
            {"_id": 0}
        )
        
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        # Get plan details
        plan = PLANS.get(request.plan_type)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Initialize MercadoPago SDK
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        
        # Create transaction record first
        transaction_id = generate_transaction_id()
        
        # Create preference data
        preference_data = {
            "items": [
                {
                    "title": f"Plan {plan['name']} - INVITAME SR",
                    "quantity": 1,
                    "unit_price": plan["price"],
                    "currency_id": plan["currency"]
                }
            ],
            "payer": {
                "email": user["email"],
                "name": user["name"]
            },
            "back_urls": {
                "success": f"{request.origin_url}/onboarding/success",
                "failure": f"{request.origin_url}/onboarding/payment",
                "pending": f"{request.origin_url}/onboarding/pending"
            },
            "auto_return": "approved",
            "external_reference": transaction_id,
            "notification_url": f"{request.origin_url}/api/payments/mercadopago/webhook"
        }
        
        # Create preference
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Save transaction
        transaction_doc = {
            "transaction_id": transaction_id,
            "user_id": user["user_id"],
            "invitation_id": request.invitation_id,
            "amount": plan["price"],
            "currency": plan["currency"],
            "payment_method": "mercadopago",
            "payment_provider_id": preference["id"],
            "status": "pending",
            "metadata": {
                "plan_type": request.plan_type
            },
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        await db.payment_transactions.insert_one(transaction_doc)
        
        return {
            "init_point": preference["init_point"],
            "preference_id": preference["id"],
            "transaction_id": transaction_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MercadoPago checkout error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payments/mercadopago/status/{payment_id}")
async def get_mercadopago_status(payment_id: str):
    """Get MercadoPago payment status"""
    try:
        import mercadopago
        
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        payment_response = sdk.payment().get(payment_id)
        payment_data = payment_response["response"]
        
        # Update transaction if approved
        if payment_data["status"] == "approved":
            external_ref = payment_data.get("external_reference")
            if external_ref:
                result = await db.payment_transactions.update_one(
                    {"transaction_id": external_ref, "status": {"$ne": "approved"}},
                    {"$set": {
                        "status": "approved",
                        "payment_provider_id": str(payment_data["id"]),
                        "updated_at": datetime.now(timezone.utc)
                    }}
                )
                
                if result.modified_count > 0:
                    transaction = await db.payment_transactions.find_one(
                        {"transaction_id": external_ref},
                        {"_id": 0}
                    )
                    if transaction:
                        await db.invitations.update_one(
                            {"invitation_id": transaction["invitation_id"]},
                            {"$set": {"status": "completed"}}
                        )
        
        return {
            "status": payment_data["status"],
            "status_detail": payment_data.get("status_detail"),
            "amount": payment_data["transaction_amount"],
            "currency": payment_data["currency_id"]
        }
        
    except Exception as e:
        logger.error(f"Get MercadoPago status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payments/mercadopago/webhook")
async def mercadopago_webhook(request: Request):
    """Handle MercadoPago webhook notifications"""
    try:
        body = await request.json()
        logger.info(f"MercadoPago webhook received: {body}")
        
        notification_type = body.get("type")
        
        if notification_type == "payment":
            payment_id = body.get("data", {}).get("id")
            if payment_id:
                # Trigger status check
                await get_mercadopago_status(str(payment_id))
        
        return JSONResponse({"status": "success"}, status_code=200)
        
    except Exception as e:
        logger.error(f"MercadoPago webhook error: {e}")
        return JSONResponse({"status": "error"}, status_code=200)

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "INVITAME SR API",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "INVITAME SR API",
        "version": "1.0.0",
        "docs": "/docs"
    }
