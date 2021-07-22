app.get("/fragment", (req, res) => {
  status = true;
  console.log("==> Admin was fragmented");
  let timer = setInterval(async () => {
    if (unlock) {
      res.send("fragment");
      clearInterval(timer);
    }
  }, 1);
});