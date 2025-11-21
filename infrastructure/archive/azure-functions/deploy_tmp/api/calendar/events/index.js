const { getCurrentUser } = require('../../shared/auth');
const { listEvents, createEvent } = require('../../shared/calendar');

module.exports = async function (context, req) {
  try {
    const user = await getCurrentUser(req);
    
    if (!user) {
      context.res = {
        status: 401,
        body: { error: "Unauthorized" }
      };
      return;
    }

    if (req.method === 'GET') {
      const { start_date, end_date, limit = 100, offset = 0 } = req.query;
      const events = await listEvents(user.tenant_id, { start_date, end_date, limit, offset });
      
      context.res = {
        status: 200,
        body: {
          status: "success",
          count: events.length,
          events
        }
      };
    } else if (req.method === 'POST') {
      const event = await createEvent(user.tenant_id, req.body);
      
      context.res = {
        status: 201,
        body: {
          status: "success",
          event_id: event.id,
          ...event
        }
      };
    }
  } catch (error) {
    context.res = {
      status: 500,
      body: { error: error.message }
    };
  }
};

