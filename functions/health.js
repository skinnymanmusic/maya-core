const { app } = require('@azure/functions');

/**
 * V4 programming model health check
 * Route: GET /api/health
 */
app.http('health', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'health',
  handler: async (request, context) => {
    context.log('Health check called');

    return {
      status: 200,
      jsonBody: {
        status: 'ok',
        service: 'maya-core',
        runtime: 'node-v4',
        timestamp: new Date().toISOString(),
      },
    };
  },
});
