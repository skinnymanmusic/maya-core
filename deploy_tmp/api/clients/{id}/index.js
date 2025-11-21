const { getCurrentUser } = require('../../shared/auth');
const { getClient, updateClient, deleteClient } = require('../../shared/clients');

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

    const clientId = context.bindingData.id;

    if (req.method === 'GET') {
      const client = await getClient(user.tenant_id, clientId);
      context.res = {
        status: 200,
        body: client
      };
    } else if (req.method === 'PUT') {
      const client = await updateClient(user.tenant_id, clientId, req.body);
      context.res = {
        status: 200,
        body: client
      };
    } else if (req.method === 'DELETE') {
      await deleteClient(user.tenant_id, clientId);
      context.res = {
        status: 204
      };
    }
  } catch (error) {
    context.res = {
      status: 500,
      body: { error: error.message }
    };
  }
};

