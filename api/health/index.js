module.exports = async function (context, req) {
  context.res = {
    status: 200,
    json: {
      status: "ok",
      service: "maya-core",
      timestamp: new Date().toISOString()
    }
  };
};
