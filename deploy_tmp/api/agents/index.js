const { getCurrentUser } = require('../../shared/auth');
const { listAgents, createAgent } = require('../../shared/agents');

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
      const agents = await listAgents(user.tenant_id);
      context.res = {
        status: 200,
        body: { agents }
      };
    } else if (req.method === 'POST') {
      const agent = await createAgent(user.tenant_id, req.body);
      context.res = {
        status: 201,
        body: { agent }
      };
    }
  } catch (error) {
    context.res = {
      status: 500,
      body: { error: error.message }
    };
  }
};

