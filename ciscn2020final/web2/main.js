const express = require("express");
const path = require("path");
const hbs = require("hbs");
const bodyParser = require("body-parser");
const app = express();

app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.set("views", path.join(__dirname, "views/"));
app.engine("html", hbs.__express);
app.set("view engine", "html");

var flag = "flag{ *** CENSORED ***  }";
var careers = ["warrior", "high_priest", "shooter"]; //可选职业
var items = ["ZLYG", "BYZF", "XELD"]; //可选物品
var rounds = [1, 2, 3, 4, 5];
var player = {};
var monster = {};

function keepTwoDecimal(num) {
	return Math.round(num * 100) / 100;
}

function getPlayerAggressivity() {
	//生成攻击力
	function rand(begin, end) {
		return Math.floor(Math.random() * (end - begin)) + begin;
	}

	switch (player.career) {
		case "warrior":
			return rand(10, 30);
		case "high_priest":
			return rand(15, 25);
		case "shooter":
			return rand(19, 21);
		default:
			return 10;
	}
}

function getPlayerDamageValue() {
	//计算纯粹伤害
	if (player.buff) {
		return keepTwoDecimal(player.aggressivity + player.buff);
	} else return player.aggressivity;
}

function triggerPassiveSkill() {
	//触发被动技能
	switch (player.career) {
		case "warrior":
			player.buff = 5;
			return 1;
		case "high_priest":
			player.HP += 10;
			player.HP = keepTwoDecimal(player.HP);
			return 2;
		case "shooter":
			player.buff = 7;
			return 3;
		default:
			return 0;
	}
}

function monsterPassiveSkill() {
	if (monster.HP <= 80 && monster.num === 1) {
		monster.num = 0;
		monster.HP += 20;
		monster.HP = keepTwoDecimal(monster.HP);
		return true;
	} else return false;
}

function playerUseItem(round) {
	//ZLYG：治疗药膏，使用后回复10点生命值
	//BYZF：白银之锋，使用后的一次攻击将触发暴击并造成130%的伤害
	//XELD：邪恶镰刀，使用后将对方的一次攻击的攻击力变为80%
	if (round == player.round_to_use && player.num == 1) {
		player.num = 0;
		switch (player.item) {
			case "ZLYG":
				player.HP += 10;
				return 1;
			case "BYZF":
				player.buff = player.aggressivity * 0.3;
				player.buff = keepTwoDecimal(player.buff);
				return 2;
			case "XELD":
				monster.buff = monster.aggressivity * (1 - 0.8) * -1;
				monster.buff = keepTwoDecimal(monster.buff);
				return 3;
		}
	} else return 0;
}

function playerAttackMonster() {
	monster.HP -= getPlayerDamageValue();
	monster.HP = keepTwoDecimal(monster.HP);
}

function monsterAttackPlayer() {
	if (monster.buff) {
		player.HP -= monster.aggressivity + monster.buff;
		player.HP = keepTwoDecimal(player.HP);
		return keepTwoDecimal(monster.aggressivity + monster.buff);
	} else {
		player.HP -= monster.aggressivity;
		player.HP = keepTwoDecimal(player.HP);
		return monster.aggressivity;
	}
}

function initMonster() {
	monster = {
		HP: 100,
		skill: "suodi", //当血量<=80时触发缩地技能，遁入地下并迅速恢复20点生命值
		num: 1, //缩地技能剩余触发的次数
		name: "di_xue_ling_zhu", //地穴领主
		aggressivity: 40, // 攻击力
		master: "ciscn",
	};
}

function playerAndMonsterInfo() {
	let playerInfo = "\nPlayer\n",
		monsterInfo = "\nMonster\n";
	for (let i in player) {
		playerInfo += `${i} : ${player[i]}\n`;
	}
	for (let i in monster) {
		monsterInfo += `${i} : ${monster[i]}\n`;
	}
	return "<!-- " + playerInfo + "<br>" + monsterInfo + "-->";
}

function checkRound(i) {
	for (let r in rounds) {
		if (i == r) return true;
	}
	return false;
}

app.get("/", (req, res) => {
	res.render("home");
});

app.get("/source", function (req, res) {
	res.sendfile("./static/source.txt");
});

app.get("/start", (req, res) => {
	res.render("start");
});

app.post("/start", (req, res) => {
	if (req.body && typeof req.body == "object") {
		player = {
			name: "ciscn",
			career: "warrior",
			item: "BYZF",
			round_to_use: 1, //round_to_use表示在哪一轮使用物品
		};

		let tempPlayer = req.body;

		for (let i in tempPlayer) {
			if (player[i]) {
				if (
					(i == "career" && !careers.includes(tempPlayer[i])) ||
					(i == "item" && !items.includes(tempPlayer[i])) ||
					(i == "round_to_use" && !checkRound(tempPlayer[i])) ||
					tempPlayer[i] === ""
				) {
					continue;
				}
				player[i] = tempPlayer[i];
			}
		}
		player.num = 1; //player剩余可`使用物品`的次数
		player.HP = 100; //HP为血量
		player.aggressivity = getPlayerAggressivity();

		initMonster();
		res.redirect("/battle");
	} else {
		res.redirect("/");
	}
});

app.get("/battle", (req, res) => {
	if (player.HP !== 100) {
		res.status(403).end("Forbidden");
		return;
	}

	let battleLog = [];
	let round = 1;
	do {
		battleLog.push(
			`<font color="red" size="5px">Round <B>${round}</B> fight!</font>`
		);

		player.aggressivity = getPlayerAggressivity();
		battleLog.push(
			`${playerAndMonsterInfo()}玩家<B>${
				player.name
			}</B>攻击力为<B>${getPlayerDamageValue()}</B>!`
		);

		switch (playerUseItem(round)) {
			case 0:
				break;
			case 1:
				battleLog.push(
					`玩家<B>${player.name}</B>使用了物品<B>治疗药膏</B>! 玩家生命值+10！`
				);
				break;
			case 2:
				battleLog.push(
					`玩家<B>${player.name}</B>使用了物品<B>白银之锋</B>! 即将造成130%暴击！`
				);
				break;
			case 3:
				battleLog.push(
					`玩家<B>${player.name}</B>使用了物品<B>邪恶镰刀</B>! <B>地穴领主</B>的攻击力变为了80%！`
				);
				break;
		}

		if (round === 1) {
			switch (triggerPassiveSkill()) {
				case 1:
					battleLog.push(
						`玩家<B>${player.name}</B>触发了<B>战神领主</B>的被动技能<B>旋风飞斧</B>! 下次攻击的攻击力+5！`
					);
					break;
				case 2:
					battleLog.push(
						`玩家<B>${player.name}</B>触发了<B>奥术祭司</B>的被动技能<B>巫毒恢复</B>! 玩家<B>${player.name}</B>的生命值+10！`
					);
					break;
				case 3:
					battleLog.push(
						`玩家<B>${player.name}</B>触发了<B>暗夜游侠</B>的被动技能<B>百步穿杨</B>! 下次攻击的攻击力+7！`
					);
			}
		}

		playerAttackMonster();
		battleLog.push(
			`玩家<B>${
				player.name
			}</B>攻击了<B>地穴领主</B>并造成<B>${getPlayerDamageValue()}</B>点伤害! <B>地穴领主</B>剩余血量为<B>${
				monster.HP
			}</B>`
		);

		if (monster.HP <= 0) {
			battleLog.push(" ");
			break;
		}

		if (monsterPassiveSkill()) {
			battleLog.push(
				`<B>地穴领主</B>触发了被动技能<B>缩地</B>！生命值回复20点！回复后生命值为<B>${monster.HP}</B>`
			);
		}

		battleLog.push(
			`<B>地穴领主</B>攻击了玩家<B>${
				player.name
			}</B>并造成<B>${monsterAttackPlayer()}</B>点伤害! 玩家<B>${
				player.name
			}</B>剩余血量为<B>${player.HP}</B>`
		);

		monster.aggressivity = 40;
		monster.buff = 0;
		player.buff = 0;
		round++;
		battleLog.push(" ");
	} while (player.HP > 0 && monster.HP > 0);

	if (player.HP > monster.HP) {
		battleLog.push(
			"Congratulation,恭喜你胜aaabbb利了！这是给你的奖励：" + flag
		);
	} else {
		battleLog.push("很遗憾，你被打败了，但是不要灰心，再接再厉");
	}
	player = monster = {};
	res.render("result", { result: battleLog.join("<br />\n") });
});

app.listen(80);
