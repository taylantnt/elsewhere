MONOLOGUE - black screen[
  {
	"speaker": "",
	"text": "Wow... that was a long flight."
  },
  {
	"speaker": "",
	"text": "I think that was the longest flight of my life."
  },
  {
	"speaker": "",
	"text": "But... I made it. I'm finally here."
  },
  {
	"speaker": "",
	"text": "Japan."
  },
  {
	"speaker": "",
	"text": "It doesn’t feel real yet. The signs, the announcements, the air—it’s all so different."
  },
  {
	"speaker": "",
	"text": "I came here as a foreign exchange student. A fresh start in a new country."
  },
  {
	"speaker": "",
	"text": "Host family, new school, new language, new life."
  },
  {
	"speaker": "",
	"text": "I should be more excited. But right now, everything feels a little... fuzzy."
  },
  {
	"speaker": "",
	"text": "I remember filling out the application. Sending the forms. Waiting for months."
  },
  {
	"speaker": "",
	"text": "I remember being thrilled when I got accepted. My friends said I was brave."
  },
  {
	"speaker": "",
	"text": "But... what exactly made me choose Japan?"
  },
  {
	"speaker": "",
	"text": "Was it the culture? The food? The language? Anime? No, that’s too easy."
  },
  {
	"speaker": "",
	"text": "I must’ve had a reason. I know I did."
  },
  {
	"speaker": "",
	"text": "But thinking back now... it’s like the memory is just out of reach."
  },
  {
	"speaker": "",
	"text": "Like trying to recall a dream after waking up."
  },
  {
	"speaker": "",
	"text": "Maybe it's just the jet lag. Or the nerves. Or being in a completely new place alone."
  },
  {
	"speaker": "",
	"text": "I should focus on what’s ahead."
  },
  {
	"speaker": "",
	"text": "A new home. A host family. A whole country waiting to be explored."
  },
  {
	"speaker": "",
	"text": "It’s strange... something about this place feels familiar and unfamiliar at the same time."
  },
  {
	"speaker": "",
	"text": "They say studying abroad changes you. Maybe it does."
  },
  {
	"speaker": "",
	"text": "Or maybe... it reminds you of who you really are."
  },
  {
	"speaker": "",
	"text": "Whatever this is, I’m here now. And I’m going to make the most of it."
  },
  {
	"speaker": "",
	"text": "Time to step into my new life..."
  }
]


MONOLOGUE - airport	internal_monologue_lines = [
		"Alright, I made it all the way here...",
		"But I have no idea where I'm going.",
		"Let me check my phone for the Maps app.",
		"...",
		"What? No reception?",
		"I guess I can't use my phone right now.",
		"Maybe I should ask someone around here for directions."
	]Airport Assistant[
  {
	"speaker": "Airport Assistant",
	"text": "パンフレットを確認してください。Check.. pamphlet... please.. またお越しください。 ",
	"portrait": "res://images/npc.png",
	"condition": "has_pamphlet"
  },
  { "speaker": "Player",
	"text": "I cannot read it at all! Maybe I can show this pamphlet to the other Airport Assistant",
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Airport Assistant",
	"text": "いらっしゃいませ～。ようこそ。",
	"portrait": "res://images/npc.png",
	"condition": "!talked_to_security || !talked_to_man1 || !talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "いらっしゃいませ～。ようこそ。",
	"portrait": "res://images/npc.png",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Player",
	"text": "Hi! Um… Can you help me?",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "えっ…えいご…すこしだけ…",
	"portrait": "res://images/npc.png",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "えいごのスタッフは…いまやすみ…",  
	"portrait": "res://images/npc.png",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "*muttering to herself*\nEnglish staff... break time now... しょうがないね。",
	"portrait": "res://images/npc.png",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Player",
	"text": "...Okay... Umm, I need to find this place.",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "アドレス？うーん… show... me?",
	"portrait": "res://images/npc.png",
	"choices": ["Show address on phone", "Nevermind"],
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Player",
	"text": "*Shows address on phone.*\nCan you tell me how to go here?",
	"branch": 0,
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "あー、これはね…でんしゃ？トレイン？",
	"portrait": "res://images/npc.png",
	"branch": 0,
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "うえのえき…から…えっと…ちょっとまってね。",
	"portrait": "res://images/npc.png",
	"branch": 0,
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "*Takes out a japanese map full of arrows and kanji.*",
	"portrait": "res://images/npc.png",
	"branch": 0,
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2",
	"action": "give_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Uh… this is... kind of amazing but also terrifying.",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Airport Assistant",
	"text": "No problem, Good Luck! がんばってください！",
	"portrait": "res://images/npc.png",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  },
  {
	"speaker": "Player",
	"text": "...Thanks. I'll try my best.",
	"condition": "talked_to_security && talked_to_man1 && talked_to_npc2"
  }
]

Veteran Assistant[
  {
	"speaker": "Veteran Assistant",
	"text": "Oh dear, are you a bit lost?",
	"portrait": "res://images/assistant2.png",
	"condition": "!has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "If you find a pamphlet lying around,\nI can try to translate it for you!",
	"portrait": "res://images/assistant2.png",
	"condition": "!has_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Pamphlet? \nI'll go look for one.",
	"condition": "!has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Oh dear, are you a bit lost?",
	"portrait": "res://images/assistant2.png",
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Let me have a look at that pamphlet.\nThese things are more puzzle than guide, huh?",
	"portrait": "res://images/assistant2.png",
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Yes, totally.\nI can't make sense of it.",
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Okay then.\nYou're headed to 中野3丁目, right?",
	"portrait": "res://images/assistant2.png",
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Yeah, that's the place.",
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "You’ve got two ways to get there.\nTrain is cheaper, but a bit tricky.\nTaxi’s simple, but pricey.\nWant details?",
	"portrait": "res://images/assistant2.png",
	"choices": ["Tell me about the train", "No, I'm good. Thanks!"],
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Tell me about the train.",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Alright, here's the deal.\nFirst, buy a ticket before going in.\nYou can’t enter the platform without it.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Then wait for the express train.\nNot the local one!\nUnless you enjoy long rides and sore feet.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Follow the signs for the Keisei Line.\nIt'll get you there in about 45 minutes.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Want me to explain the taxi option too,\nor are you ready to go?",
	"portrait": "res://images/assistant2.png",
	"choices": ["Tell me about the taxi", "No, I'm good. Thanks!"],
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Tell me about the taxi.",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Just head outside and find the taxi stand.\nThere’s usually a line, so be patient.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "It might cost around ¥18,000,\nmaybe more if traffic’s bad.\nBut it’s the easiest route.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Just show the driver your pamphlet.\nThey’ll handle the rest.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Glad to help!\nEnjoy your trip, and welcome to Japan!",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet",
	"end": true
  },
  {
	"speaker": "Player",
	"text": "No, I'm good. Thanks!",
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Glad to help!\nEnjoy your trip, and welcome to Japan!",
	"portrait": "res://images/assistant2.png",
	"branch": 1,
	"condition": "has_pamphlet",
	"end": true
  },
  {
	"speaker": "Player",
	"text": "Tell me about the taxi.",
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Just head outside and find the taxi stand.\nThere’s usually a line, so be patient.",
	"portrait": "res://images/assistant2.png",
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "It might cost around ¥18,000,\nmaybe more if traffic’s bad.\nBut it’s the easiest route.",
	"portrait": "res://images/assistant2.png",
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Just show the driver your pamphlet.\nThey’ll handle the rest.",
	"portrait": "res://images/assistant2.png",
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Want me to explain the train option too,\nor are you ready to go?",
	"portrait": "res://images/assistant2.png",
	"choices": ["Tell me about the train", "No, I'm good. Thanks!"],
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Player",
	"text": "Tell me about the train.",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Alright, here's the deal.\nFirst, buy a ticket before going in.\nYou can’t enter the platform without it.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Then wait for the express train.\nNot the local one!\nUnless you enjoy long rides and sore feet.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Follow the signs for the Keisei Line.\nIt'll get you there in about 45 minutes.",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Glad to help!\nEnjoy your trip, and welcome to Japan!",
	"portrait": "res://images/assistant2.png",
	"branch": 0,
	"condition": "has_pamphlet",
	"end": true
  },
  {
	"speaker": "Player",
	"text": "No, I'm good. Thanks!",
	"branch": 1,
	"condition": "has_pamphlet"
  },
  {
	"speaker": "Veteran Assistant",
	"text": "Glad to help!\nEnjoy your trip, and welcome to Japan!",
	"portrait": "res://images/assistant2.png",
	"branch": 1,
	"condition": "has_pamphlet",
	"end": true
  }
]

NPC - Timid Man[
  {
	"speaker": "Timid Man",
	"text": "話しかけないでくれ！"
  },
  {
	"speaker": "Timid Man",
	"text": "忙しくて雑談してる暇はないんだ。"
  },
  {
	"speaker": "Timid Man",
	"text": "どいてくれ、今は大事な用事がある。"
  },
  {
	"speaker": "Player",
	"text": "(What...? I have no idea what he just said.)"
  },
  {
	"speaker": "Player",
	"text": "(I guess he doesn't want to talk...)",
	"action": "set_talked_to_man1"
  }
]

NPC - Cheerful Woman[
  {
	"speaker": "Cheerful Woman",
	"text": "こんにちは！初めてお会いしますね！"
  },
  {
	"speaker": "Cheerful Woman",
	"text": "日本へようこそ！楽しい滞在になりますように！"
  },
  {
	"speaker": "Cheerful Woman",
	"text": "もし道に迷ったら、遠慮なく聞いてくださいね！"
  },
  {
	"speaker": "Player",
	"text": "(Uhh… she said something about… sushi?)"
  },
  {
	"speaker": "Player",
	"text": "(Or maybe she thinks I look like someone she knows?)"
  },
  {
	"speaker": "Player",
	"text": "(Well, she's smiling, so I'll just smile back and nod.)",
	"action": "set_talked_to_npc2"
  }
]


NPC - Security Guard	dialogue_lines = [
	{"text": "ちょっと、下がってください。", "speaker": "Security"},
	{"text": "(Huh? I'm just trying to ask something...)", "speaker": "Player"},
	{"text": "業務中です。話しかけないでください。", "speaker": "Security", "action": "set_talked_to_security"},
	{"text": "(Did I do something wrong? I just showed my smartphone to him...)", "speaker": "Player"},
	{"text": "……", "speaker": "Security"},
	{"text": "(He didn’t even *look* at it... Is this guy part robot or something?)", "speaker": "Player"},
	{"text": "(Okay... maybe I should ask someone who isn't radiating pure stress.)", "speaker": "Player"}
]
NPC - Security Guard 2	dialogue_lines = [
	{"text": "荷物の検査をお願いします。", "speaker": "Security2"},
	{"text": "(Luggage inspection? But I don't have any luggage...)", "speaker": "Player"},
	{"text": "手荷物はどちらですか？", "speaker": "Security2"},
	{"text": "(I... I don't understand what he's asking for...)", "speaker": "Player"},
	{"text": "……手荷物がないのですか？", "speaker": "Security2", "action": "set_talked_to_security2"},
	{"text": "(Oh, I guess he can't help me either...)", "speaker": "Player"},
	{"text": "(Maybe I can ask others for directions.)", "speaker": "Player"}
]
ITEM - Information Boardsvar board1_messages := [
	"Please check your flight departure time carefully. Gates close 30 minutes before departure.",
	"All passengers must present valid identification and boarding passes at security checkpoints.",
	"Baggage restrictions apply. Check with your airline for specific weight and size limits.",
	"Flight delays may occur due to weather conditions. Monitor departure boards for updates.",
	"Duty-free shopping is available after security. Remember liquid restrictions for carry-on items.",
	"Emergency exits are located throughout the terminal. Familiarize yourself with the nearest exit.",
	"Free WiFi is available throughout the airport. Connect to 'Airport_Guest' network."
]
ITEM - Plantsvar plant_dialogues := [
	"Oh what a great plant!",
	"Oh another plant!",
	"These plants are quite nice...",
	"I don't have time to look at plants all day.",
	"Why am I looking at plants?",
	"Maybe I will get a plant when I get my own place, wonder if my host family would allow that?",
	"Same as the last one.",
	"Really? Another plant?",
	"PLANTSSS!",
	"PLAAAAAAAAANTTTTSSSS!!!"
]

