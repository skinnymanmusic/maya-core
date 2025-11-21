/**
 * Shared agent utilities
 */

const { getDb } = require('./database');

async function listAgents(tenantId) {
  const db = await getDb();
  const result = await db.query(
    `SELECT ap.*, a.name as agent_name, a.category
     FROM tenant_agent_profiles ap
     JOIN agents a ON ap.agent_key = a.key
     WHERE ap.tenant_id = $1
     ORDER BY a.name`,
    [tenantId]
  );
  return result.rows;
}

async function createAgent(tenantId, agentData) {
  const db = await getDb();
  const result = await db.query(
    `INSERT INTO tenant_agent_profiles (tenant_id, agent_key, system_prompt, is_active)
     VALUES ($1, $2, $3, $4)
     RETURNING *`,
    [tenantId, agentData.agent_key, agentData.system_prompt || '', agentData.is_active !== false]
  );
  return result.rows[0];
}

module.exports = {
  listAgents,
  createAgent
};

