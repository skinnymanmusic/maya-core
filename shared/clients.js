/**
 * Shared client utilities
 */

const { getDb } = require('./database');
const crypto = require('crypto');

function hashEmail(email) {
  return crypto.createHash('sha256').update(email.toLowerCase().trim()).digest('hex');
}

async function listClients(tenantId, { limit, offset }) {
  const db = await getDb();
  const result = await db.query(
    `SELECT id, name, email_hash, last_contact_at, created_at 
     FROM clients 
     WHERE tenant_id = $1 
     ORDER BY last_contact_at DESC NULLS LAST
     LIMIT $2 OFFSET $3`,
    [tenantId, limit, offset]
  );

  const countResult = await db.query(
    'SELECT COUNT(*) as total FROM clients WHERE tenant_id = $1',
    [tenantId]
  );

  return {
    items: result.rows,
    total: parseInt(countResult.rows[0].total),
    limit,
    offset
  };
}

async function getClient(tenantId, clientId) {
  const db = await getDb();
  const result = await db.query(
    'SELECT * FROM clients WHERE id = $1 AND tenant_id = $2',
    [clientId, tenantId]
  );
  return result.rows[0] || null;
}

async function createClient(tenantId, clientData) {
  const db = await getDb();
  const emailHash = clientData.email ? hashEmail(clientData.email) : null;
  
  const result = await db.query(
    `INSERT INTO clients (tenant_id, name, email, email_hash, phone, company)
     VALUES ($1, $2, $3, $4, $5, $6)
     RETURNING id, name, email_hash, created_at`,
    [
      tenantId,
      clientData.name,
      clientData.email, // Would be encrypted in real implementation
      emailHash,
      clientData.phone,
      clientData.company
    ]
  );
  return result.rows[0];
}

async function updateClient(tenantId, clientId, clientData) {
  const db = await getDb();
  const updates = [];
  const values = [];
  let paramIndex = 1;

  if (clientData.name) {
    updates.push(`name = $${paramIndex++}`);
    values.push(clientData.name);
  }
  if (clientData.phone) {
    updates.push(`phone = $${paramIndex++}`);
    values.push(clientData.phone);
  }
  if (clientData.company) {
    updates.push(`company = $${paramIndex++}`);
    values.push(clientData.company);
  }

  if (updates.length === 0) {
    return await getClient(tenantId, clientId);
  }

  values.push(clientId, tenantId);
  const result = await db.query(
    `UPDATE clients 
     SET ${updates.join(', ')}, updated_at = NOW()
     WHERE id = $${paramIndex} AND tenant_id = $${paramIndex + 1}
     RETURNING *`,
    values
  );
  return result.rows[0];
}

async function deleteClient(tenantId, clientId) {
  const db = await getDb();
  await db.query(
    'DELETE FROM clients WHERE id = $1 AND tenant_id = $2',
    [clientId, tenantId]
  );
}

module.exports = {
  listClients,
  getClient,
  createClient,
  updateClient,
  deleteClient
};

