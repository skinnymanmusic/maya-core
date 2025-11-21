const { getCurrentUser } = require('../../shared/auth');
const { autoBlockForConfirmedGig } = require('../../shared/calendar');

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

    const event = await autoBlockForConfirmedGig(user.tenant_id, req.body);

    context.res = {
      status: 201,
      body: {
        status: "success",
        event_id: event.id,
        message: "Calendar block created",
        ...event
      }
    };
  } catch (error) {
    context.res = {
      status: 500,
      body: { error: error.message }
    };
  }
};

