/**
 * Shared Gmail webhook utilities
 */

const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');
const { getDb } = require('./database');

const GMAIL_WEBHOOK_URL = process.env.GMAIL_WEBHOOK_URL;
const GMAIL_PUBSUB_SERVICE_ACCOUNT = process.env.GMAIL_PUBSUB_SERVICE_ACCOUNT;

const client = jwksClient({
  jwksUri: 'https://www.googleapis.com/oauth2/v3/certs'
});

function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key.publicKey || key.rsaPublicKey;
    callback(null, signingKey);
  });
}

/**
 * Verify Google JWT token
 */
async function verifyJWT(token) {
  return new Promise((resolve, reject) => {
    jwt.verify(
      token,
      getKey,
      {
        audience: GMAIL_WEBHOOK_URL,
        issuer: ['https://accounts.google.com', 'accounts.google.com'],
        algorithms: ['RS256']
      },
      (err, decoded) => {
        if (err) {
          resolve(false);
        } else if (decoded.sub !== GMAIL_PUBSUB_SERVICE_ACCOUNT) {
          resolve(false);
        } else {
          resolve(true);
        }
      }
    );
  });
}

/**
 * Process Gmail webhook
 */
async function processGmailWebhook(message) {
  // Implementation would call backend service or process directly
  // This is a placeholder
  const db = await getDb();
  // Process webhook logic here
}

module.exports = {
  verifyJWT,
  processGmailWebhook
};

