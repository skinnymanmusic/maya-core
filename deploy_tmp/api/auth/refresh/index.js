const { validateRefreshToken, createTokenPair, getUserById } = require('../../shared/auth');

module.exports = async function (context, req) {
  try {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      context.res = {
        status: 400,
        body: { error: "Refresh token required" }
      };
      return;
    }

    const payload = await validateRefreshToken(refresh_token);
    const user = await getUserById(payload.sub);
    
    if (!user || !user.is_active) {
      context.res = {
        status: 401,
        body: { error: "Invalid or inactive user" }
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
      status: 401,
      body: { error: error.message }
    };
  }
};

