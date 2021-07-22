const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const Koa = require("koa");
const Router = require("koa-router");
const koaBody = require("koa-body");
const send = require("koa-send");

const app = new Koa();
const router = new Router();
const SECRET = "?";

app.use(
	koaBody({
		multipart: true,
		formidable: {
			maxFileSize: 2000 * 1024 * 1024,
		},
	})
);

router.post("/uploadfile", async (ctx, next) => {
	// console.log(ctx.request.body.files);
	const file = ctx.request.body.files.file;
	const reader = fs.createReadStream(file.path);
	let fileId = crypto
		.createHash("md5")
		.update(file.name + Date.now() + SECRET)
		.digest("hex");
	let filePath = path.join(__dirname, "upload/") + fileId;
	const upStream = fs.createWriteStream(filePath);
	reader.pipe(upStream);
	return (ctx.body = "Upload success ~, your fileId is here：" + fileId);
});

router.get("/downloadfile/:fileId", async (ctx, next) => {
	let fileId = ctx.params.fileId;
	ctx.attachment(fileId);
	try {
		await send(ctx, fileId, { root: __dirname + "/upload" });
	} catch (e) {
		return (ctx.body = "SCTF{no_such_file_~}");
	}
});

router.get("/", async (ctx, next) => {
	ctx.response.type = "html";
	ctx.response.body = fs.createReadStream("index.html");
});

app.use(router.routes());
app.listen(3333, () => {
	console.log("This server is running at port: 3333");
});
