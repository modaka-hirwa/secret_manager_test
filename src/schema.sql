CREATE TABLE IF NOT EXISTS secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,                  -- Unique name/identifier for the secret
    type TEXT NOT NULL,                         -- Type of the secret (e.g., password, API key)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the secret was created
    last_accessed_at TIMESTAMP,                 -- Timestamp for the last time the secret was accessed
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for the last update to the secret
    owner TEXT,                                 -- The owner of the secret (user or service)
    storage_location TEXT,                      -- Where the secret is stored (local, S3, etc.)
    environment TEXT CHECK(environment IN ('dev', 'staging', 'prod')), -- The environment the secret belongs to
    expiration_date TIMESTAMP,                  -- When the secret expires (if applicable)
    rotation_frequency INTEGER,                 -- Rotation frequency in days
    compliance_tags TEXT,                       -- Compliance labels (e.g., GDPR, PCI-DSS)
    associated_service TEXT,                    -- Service or application using the secret
    is_encrypted BOOLEAN DEFAULT 1             -- Indicates if the secret is encrypted
);
