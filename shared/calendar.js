/**
 * Shared calendar utilities
 */

const { getDb } = require('./database');

async function listEvents(tenantId, { start_date, end_date, limit, offset }) {
  const db = await getDb();
  let query = 'SELECT * FROM calendar_events WHERE tenant_id = $1';
  const params = [tenantId];
  let paramIndex = 2;

  if (start_date) {
    query += ` AND start_time >= $${paramIndex}`;
    params.push(start_date);
    paramIndex++;
  }

  if (end_date) {
    query += ` AND end_time <= $${paramIndex}`;
    params.push(end_date);
    paramIndex++;
  }

  query += ` ORDER BY start_time DESC LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`;
  params.push(limit, offset);

  const result = await db.query(query, params);
  return result.rows;
}

async function createEvent(tenantId, eventData) {
  const db = await getDb();
  const result = await db.query(
    `INSERT INTO calendar_events (tenant_id, title, start_time, end_time, location, description, client_id)
     VALUES ($1, $2, $3, $4, $5, $6, $7)
     RETURNING *`,
    [
      tenantId,
      eventData.title,
      eventData.start_time,
      eventData.end_time,
      eventData.location,
      eventData.description,
      eventData.client_id
    ]
  );
  return result.rows[0];
}

async function autoBlockForConfirmedGig(tenantId, blockData) {
  // Auto-block logic - create calendar event with red color
  const db = await getDb();
  const result = await db.query(
    `INSERT INTO calendar_events (tenant_id, title, start_time, end_time, location, description, client_id, color_id)
     VALUES ($1, $2, $3, $4, $5, $6, $7, 4)
     RETURNING *`,
    [
      tenantId,
      `SME Booking — ${blockData.client_name}`,
      blockData.event_date,
      new Date(new Date(blockData.event_date).getTime() + blockData.duration_hours * 60 * 60 * 1000).toISOString(),
      blockData.location || blockData.venue,
      blockData.context || 'Auto-blocked from email acceptance',
      blockData.client_id
    ]
  );
  return result.rows[0];
}

module.exports = {
  listEvents,
  createEvent,
  autoBlockForConfirmedGig
};

