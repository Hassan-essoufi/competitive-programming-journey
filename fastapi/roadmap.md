graph TD

A[Python Basics] --> B[HTTP Fundamentals]
B --> C[FastAPI Basics]

C --> D[Path Operations]
C --> E[Query Parameters]
C --> F[Request Body]

D --> G[Pydantic Models]
E --> G
F --> G

G --> H[Validation & Serialization]

H --> I[Response Models]
H --> J[Status Codes]

I --> K[Dependency Injection]

K --> L[Database Integration]

L --> M[SQLAlchemy / ORM]
L --> N[Async Databases]

M --> O[Authentication]
N --> O

O --> P[Security OAuth2 JWT]

P --> Q[Background Tasks]
P --> R[WebSockets]

Q --> S[Testing]
R --> S

S --> T[Deployment]

T --> U[Docker]
T --> V[Nginx]
T --> W[CI/CD]