# ARCHITECTURE_OVERVIEW.md  
## MayAssistant Architecture Overview (v1.2)

Last Updated: 2025-01-27

---

# 1. SYSTEM PURPOSE

MayAssistant automates:
- booking  
- reminders  
- payments  
- follow-ups  
- event planning  
- venue intelligence  
- client communication  

Designed for:
- Beauty pros  
- Barbers  
- Stylists  
- DJs  
- AV technicians  
- Other appointment-based pros  

---

# 2. HIGH-LEVEL ARCHITECTURE

### CLIENT LAYER
- Next.js 14 (web)
- Mobile PWA  
- SMS  
- Email  

### API LAYER
- FastAPI application  
- REST endpoints  
- Auth with JWT  
- Workspace isolation  

### APPLICATION LAYER
- Booking engine  
- Payment service  
- SMS service  
- Email processing v3  
- Calendar sync  
- Reminder engine  
- Intelligence modules (8)  
- Guardian Framework  

### MICRO-SERVICES
- Nova → pric
