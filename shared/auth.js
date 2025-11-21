/**
 * Shared authentication utilities for Azure Functions
 */

const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { getDb } = require('./database');

const JWT_SECRET = process.env.JWT_SECRET_KEY || process.env.JWT_SECRET;
const JWT_ALGO = 'HS256';
const ACCESS_TOKEN_EXPIRE_MINUTES = 30;
const REFRESH_TOKEN_EXPIRE_DAYS = 7;

/**
 * Authenticate user with email and password
 */
async function authenticateUser(email, password) {
  const db = await getDb();
  const result = await db.query(
    'SELECT id, email, password_hash, tenant_id, role, active FROM users WHERE email = $1',
    [email]
  );

  if (result.rows.length === 0) {
    return null;
  }

  const user = result.rows[0];
  const isValid = await bcrypt.compare(password, user.password_hash);

  if (!isValid) {
    return null;
  }

  return {
    id: user.id,
    email: user.email,
    tenant_id: user.tenant_id,
    role: user.role,
    active: user.active
  };
}

/**
 * Get user by ID
 */
async function getUserById(userId) {
  const db = await getDb();
  const result = await db.query(
    'SELECT id, email, tenant_id, role, active FROM users WHERE id = $1',
    [userId]
  );

  return result.rows[0] || null;
}

/**
 * Create JWT token pair
 */
function createTokenPair(user) {
  const now = Math.floor(Date.now() / 1000);

  const accessPayload = {
    sub: user.id,
    tenant_id: user.tenant_id,
    role: user.role,
    scope: 'access',
    iat: now,
    exp: now + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
  };

  const refreshPayload = {
    sub: user.id,
    tenant_id: user.tenant_id,
    role: user.role,
    scope: 'refresh',
    iat: now,
    exp: now + (REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)
  };

  return {
    access_token: jwt.sign(accessPayload, JWT_SECRET, { algorithm: JWT_ALGO }),
    refresh_token: jwt.sign(refreshPayload, JWT_SECRET, { algorithm: JWT_ALGO }),
    token_type: 'bearer'
  };
}

/**
 * Validate refresh token
 */
async function validateRefreshToken(token) {
  try {
    const payload = jwt.verify(token, JWT_SECRET, { algorithms: [JWT_ALGO] });
    
    if (payload.scope !== 'refresh') {
      throw new Error('Invalid token scope');
    }

    return payload;
  } catch (error) {
    throw new Error('Invalid refresh token');
  }
}

/**
 * Get current user from request
 */
async function getCurrentUser(req) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return null;
  }

  try {
    const payload = jwt.verify(token, JWT_SECRET, { algorithms: [JWT_ALGO] });
    
    if (payload.scope !== 'access') {
      return null;
    }

    const user = await getUserById(payload.sub);
    return user;
  } catch (error) {
    return null;
  }
}

module.exports = {
  authenticateUser,
  getUserById,
  createTokenPair,
  validateRefreshToken,
  getCurrentUser
};

