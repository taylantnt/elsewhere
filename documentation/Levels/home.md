MONOLOGUE - after credits{
  "dialogue": [
	{
	  "speaker": "Player",
	  "text": "*Takes a deep breath, standing in front of the house.*"
	},
	{
	  "speaker": "Player",
	  "text": "Managed to catch the express and transfer at the right station. Not bad for my first time navigating solo.",
	  "condition": "boarded_shinkansen"
	},
	{
	  "speaker": "Player",
	  "text": "Man... that local train stopped at every single station. Took forever to get here.",
	  "condition": "!boarded_shinkansen"
	},
	{
	  "speaker": "Player",
	  "text": "It’s already pretty late. I hope I’m not waking anyone up...",
	  "condition": "!boarded_shinkansen"
	},
	{
	  "speaker": "Player",
	  "text": "Still can’t believe I’m actually here. My home—at least for the next year."
	},
	{
	  "speaker": "Player",
	  "text": "Alright… what was the proper greeting again? Konnichiwa? That works, right?"
	},
	{
	  "speaker": "Player",
	  "text": "Okay. Let’s do this."
	},
	{
	  "speaker": "Player",
	  "text": "*Reaches for the doorbell.*",
	  "action": "play_doorbell"
	},
	{
	  "speaker": "Player",
	  "text": "*Presses the button. A chime echoes from inside.*"
	},
	{
	  "speaker": "Mother",
	  "text": "There you are!"
	},
	{
	  "speaker": "Mother",
	  "text": "We were starting to worry you took the wrong train or got completely lost."
	},
	{
	  "speaker": "Mother",
	  "text": "I’m so glad you made it. Welcome!"
	},
	{
	  "speaker": "Mother",
	  "text": "Come on in—you must be exhausted.",
	  "action": "transition_to_home"
	}
  ]
}

Family Dialogue[
  {
	"speaker": "Miharu Nagai",
	"text": "Ah, you must be our guest! Welcome, welcome—I'm Miharu Nagai.",
	"portrait": "res://images/mother.png"
  },
  {
	"speaker": "Tetsuo Nagai",
	"text": "And I'm Tetsuo Nagai. So, you finally found our home. Good—Miharu told us you'd be arriving today.",
	"portrait": "res://images/father.png"
  },
  {
	"speaker": "Tetsuo Nagai",
	"text": "We keep things the proper way here—none of that new gadget nonsense. A good letter or a face-to-face talk works best.",
	"portrait": "res://images/father.png"
  },
  {
	"speaker": "Miharu Nagai",
	"text": "Tetsuo still uses the same flip phone from ten years ago. But don’t worry, I’m happy to help you with anything you need.",
	"portrait": "res://images/mother.png"
  },
  {
	"speaker": "Miharu Nagai",
	"text": "Hikari was the one who sent the emails you received. She’s resting now, but you’ll meet her in the morning.",
	"portrait": "res://images/mother.png"
  },
  {
	"speaker": "Tetsuo Nagai",
	"text": "This is our first time hosting someone from abroad. We’ll treat you like family here.",
	"portrait": "res://images/father.png"
  },
  {
	"speaker": "Tetsuo Nagai",
	"text": "Miharu, why don’t you take our guest to their room before the evening chill sets in?",
	"portrait": "res://images/father.png"
  },
  {
	"speaker": "Miharu Nagai",
	"text": "Of course. Please, follow me—your room is just upstairs.",
	"portrait": "res://images/mother.png"
  }
]

Mother Dialogue		{"text": "Well, this is not a lot but this will be your room for a year.", "speaker": "Miharu Nagai", "portrait": "res://images/mother.png"},
		{"text": "Miharu's room is next door so please try not to make a lot of noise. She is a light sleeper.", "speaker": "Miharu Nagai", "portrait": "res://images/mother.png"},
		{"text": "Oh, by the way, your clothes and belongings that you sent before coming here with shipping have already arrived yesterday.", "speaker": "Miharu Nagai", "portrait": "res://images/mother.png"},
		{"text": "Would you help your old host mother to bring it to your room?", "speaker": "Miharu Nagai", "portrait": "res://images/mother.png"}
	]
MONOLOGUE - Room first time	var player_monologue = [
		{"text": "Good thing I sent everything before. Thanks to that I was only managed to carry a small bag.", "speaker": "Player"},
		{"text": "I wouldn't be able to keep up with the train transfers if I had luggage.", "speaker": "Player"},
		{"text": "Anyways, I will unpack now.", "speaker": "Player"}
	]
MONOLOGUE - After unpacking	var final_dialogue = [
		{"text": "Whewww, I am tired with all this unpacking but finally it looks like a proper room now.", "speaker": "Player"},
		{"text": "But I am grateful that I even have a room honestly.", "speaker": "Player"},
		{"text": "I heard many foreign students share bunk beds in a small room so I am really grateful.", "speaker": "Player"},
		{"text": "Anyways, even though I slept in the train, all this unpacking made me sleepy again.", "speaker": "Player"},
		{"text": "Maybe I should sleep.", "speaker": "Player"}
	]