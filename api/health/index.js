module.exports = async function (context, req) {
  context.res = {
    status: 200,
    body: {
      status: "ok",
      service: "maya-core",
      timestamp: new Date().toISOString()
    }
  };
};
