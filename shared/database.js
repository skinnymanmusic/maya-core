/**
 * Shared database connection for Azure Functions
 */

const { Pool } = require('pg');

let pool = null;

function getDb() {
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.DATABASE_SSL === 'true' ? { rejectUnauthorized: false } : false
    });
  }
  return pool;
}

module.exports = { getDb };

