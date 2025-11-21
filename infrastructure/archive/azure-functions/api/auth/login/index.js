const { authenticateUser, createTokenPair } = require('../../shared/auth');

module.exports = async function (context, req) {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      context.res = {
        status: 400,
        body: { error: "Email and password required" }
      };
      return;
    }

    const user = await authenticateUser(email, password);
    
    if (!user) {
      context.res = {
        status: 401,
        body: { error: "Invalid credentials" }
      };
      return;
    }

    const tokens = createTokenPair(user);

    context.res = {
      status: 200,
      body: tokens
    };
  } catch (error) {
    context.res = {
      status: 500,
      body: { error: error.message }
    };
  }
};

