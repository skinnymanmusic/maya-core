const { verifyJWT, processGmailWebhook } = require('../../shared/gmail');

module.exports = async function (context, req) {
  try {
    // Verify JWT token from Google Pub/Sub
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token || !await verifyJWT(token)) {
      context.res = {
        status: 401,
        body: { error: "Invalid JWT token" }
      };
      return;
    }

    // Process webhook
    await processGmailWebhook(req.body);

    context.res = {
      status: 200,
      body: { status: "processed" }
    };
  } catch (error) {
    context.res = {
      status: 500,
      body: { error: error.message }
    };
  }
};

