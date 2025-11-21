const { getCurrentUser } = require('../../shared/auth');
const { listClients, createClient, getClient, updateClient, deleteClient } = require('../../shared/clients');

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

    if (req.method === 'GET' && !clientId) {
      // List clients
      const { limit = 50, offset = 0 } = req.query;
      const result = await listClients(user.tenant_id, { limit, offset });
      
      context.res = {
        status: 200,
        body: result
      };
    } else if (req.method === 'GET' && clientId) {
      // Get single client
      const client = await getClient(user.tenant_id, clientId);
      
      context.res = {
        status: 200,
        body: client
      };
    } else if (req.method === 'POST') {
      // Create client
      const client = await createClient(user.tenant_id, req.body);
      
      context.res = {
        status: 201,
        body: client
      };
    } else if (req.method === 'PUT' && clientId) {
      // Update client
      const client = await updateClient(user.tenant_id, clientId, req.body);
      
      context.res = {
        status: 200,
        body: client
      };
    } else if (req.method === 'DELETE' && clientId) {
      // Delete client
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

