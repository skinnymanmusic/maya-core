const { getCurrentUser } = require('../../shared/auth');

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

    context.res = {
      status: 200,
      body: {
        id: user.id,
        email: user.email,
        tenant_id: user.tenant_id,
        role: user.role,
        active: user.active
      }
    };
  } catch (error) {
    context.res = {
      status: 401,
      body: { error: error.message }
    };
  }
};

