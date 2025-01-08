from tenor import get_gif
import random
from predefined_gifs import gifs


# Action messages dictionary
messages = {
    "pat": [
        "{user} gave {user2} a gentle pat on the head. So cute!",
        "{user} patted {user2} on the back. Good job!",
        "{user} gave {user2} a warm pat. You're the best!",
        "{user} patted {user2} gently. So wholesome!",
        "{user} patted {user2} on the head.",
    ],
    "poke": [
        "{user} poked {user2}. Hey, wake up!",
        "{user} gave {user2} a little poke. What's up with you?",
        "{user} poked {user2} in the ribs. Gotcha!",
        "{user} poked {user2} playfully. Stop ignoring me!",
        "{user} gave {user2} a poke. Don't be shy!",
    ],
    "bonk": [
        "{user} bonked {user2} on the head. Ouch, that’s gotta hurt!",
        "{user} bonked {user2} lightly. Bad {user2}!",
        "{user} gave {user2} a good ol' bonk. Don’t mess with me!",
        "{user} bonked {user2} with a plushie. Soft but still funny!",
        "{user} bonked {user2} with a hammer. Okay, maybe a little too hard!",
    ],
    "wag": [
        "{user} wagged their tail at {user2}. Feeling happy today?",
        "{user} wagged their tail. Who’s a good {user2}?",
        "{user} wagged their tail. {user2} got lucky, huh?",
    ],
    "stare": [
        "{user} stared at {user2} intensely. You’re next!",
        "{user} gave {user2} a long, unwavering stare. Is there something on my face?",
        "{user} stared at {user2} with fiery eyes. You can feel the heat!",
        "{user} gave {user2} a penetrating stare. Trying to read your mind!",
        "{user} stared at {user2} without blinking. I’m not giving up!",
    ], ##
    "hug": [
        "{user} gave {user2} a warm hug! So wholesome!",
        "Aww, {user} hugged {user2}. That's so sweet!",
        "{user} spread some love and hugged {user2}.",
        "{user} hugged {user2} tightly. Someone's feeling loved!",
        "Hugs incoming! {user} hugged {user2}.",
        "{user} wrapped {user2} in a big hug. Warm fuzzies everywhere!",
        "{user} shared a wholesome hug with {user2}.",
        "Cuteness overload! {user} hugged {user2} softly.",
        "Hugs are the best! {user} gave {user2} a big hug.",
        "{user} used '/give {user2} hugs 1'!"
    ],
    "punch": [
        "BAM! {user} landed a solid punch on {user2}. Ouch!",
        "{user} unleashed a flurry of punches on {user2}.",
        "{user} just punched {user2}. That’s gotta hurt!",
        "{user} smashed {user2} with a devastating punch.",
        "POW! {user} showed no mercy and punched {user2} hard!",
        "A sneak attack! {user} punched {user2} in a fit of rage.",
        "{user} threw a mean right hook at {user2}. Lights out!",
        "It’s a knockout! {user} punched {user2} to oblivion.",
        "Watch out! {user} just punched {user2}. The crowd gasps!",
        "Boxing champ alert! {user} delivered a deadly punch to {user2}.",
        "AND HIS NAME IS... {user}! {user}-1 {user2}-0"
    ],
    "bite": [
        "Uh oh! {user} bit {user2}. Is this a zombie apocalypse?",
        "{user} showed their teeth and bit {user2}. Nom nom!",
        "{user} got hungry and took a bite out of {user2}.",
        "{user} sank their teeth into {user2}. Ferocious!",
        "Yikes! {user} bit {user2} hard. Someone call a medic!",
        "{user} decided to munch on {user2}. Ouch!",
        "{user} bit {user2} like a wild animal. Someone’s hangry!",
        "CHOMP! {user} bit {user2}. Better watch those fingers!",
        "Run for your life! {user} bit {user2}. No mercy!",
        "Cannibal vibes? {user} bit {user2}. Someone’s feeling savage!",
        "I think {user} mistook {user2} for a wafer."
    ],
    "wave": [
        "{user} waved enthusiastically at {user2}. Hi there!",
        "Friendly vibes! {user} waved at {user2} with a big smile.",
        "{user} waved at {user2}. Are they besties now?",
        "Wave incoming! {user} waved at {user2} with style.",
        "{user} sent a cheerful wave towards {user2}. Cute!",
        "Hiya! {user} waved at {user2}. They look so happy!",
        "The crowd goes wild! {user} waved at {user2} like royalty.",
        "{user} waved dramatically at {user2}. A true showstopper!",
        "{user} waved so hard, their hand almost fell off! {user2} noticed.",
        "Friendly greetings! {user} waved at {user2} from across the room.",
    ],
    "kill": [
        "Fatality! {user} executed {user2} in cold blood.",
        "Game over! {user} eliminated {user2}. Rest in pieces.",
        "{user} used kill! It was ultra-effective! {user2} has died.",
        "Watch out! {user} assassinated {user2}. Brutal!",
        "{user} killed {user2}. No respawn button here.",
        "Lights out! {user} annihilated {user2} with precision.",
        "{user} ended {user2}’s journey with a swift kill.",
        "Ruthless! {user} took down {user2}. No survivors.",
        "The end is nigh! {user} killed {user2} mercilessly.",
        "{user} obliterated {user2}. Absolute carnage!",
    ],
    "lick": [
        "Eww! {user} just licked {user2}. That’s unexpected.",
        "{user} licked {user2} like an ice cream cone. Yikes!",
        "{user} showed affection by licking {user2}. Weird flex!",
        "What was that? {user} licked {user2} out of nowhere.",
        "{user} licked {user2} gently. A bit awkward, right?",
        "Lick attack! {user} licked {user2}. Why tho?",
        "{user} gave {user2} a slobbery lick. Eww but cute?",
        "Friendly but weird! {user} licked {user2}.",
        "{user} stuck out their tongue and licked {user2}. Bold move!",
        "Someone’s feeling playful! {user} licked {user2} out of nowhere.",
    ],
    "kiss": [
        "{user} used KISS! It was super effective! {user2} has been flattered.",
        "{user} kissed {user2} on the cheek. How sweet!",
        "Aww, {user} planted a soft kiss on {user2}. Romantic!",
        "{user} kissed {user2}. Is that love in the air?",
        "Smooch alert! {user} kissed {user2} with affection.",
        "A tender moment! {user} kissed {user2}. So cute!",
        "Lovebirds? {user} kissed {user2}. Adorable!",
        "{user} leaned in and kissed {user2}. A perfect moment.",
        "Romantic vibes! {user} kissed {user2} under the stars.",
        "{user} kissed {user2}. The crowd ships them!",
        "Swoon-worthy! {user} kissed {user2} with elegance.",
    ],
    "spank": [
        "WHAP! {user} spanked {user2}. Someone’s in trouble!",
        "{user} gave {user2} a playful spank. Naughty!",
        "{user} spanked {user2}. That’s gotta sting!",
        "Spank incoming! {user} delivered a sharp hit to {user2}.",
        "{user} gave {user2} a well-aimed spank. Yikes!",
        "Ouch! {user} spanked {user2}. Someone call HR!",
        "{user} spanked {user2} for no apparent reason. Chaos!",
        "The sound echoed! {user} spanked {user2}. Everyone heard it.",
        "SPANK ALERT! {user} hit {user2} with style.",
        "{user} didn’t hold back and spanked {user2}. Whoops!",
    ],
    "kick": [
        "WHAM! {user} kicked {user2} into next week.",
        "A flying kick! {user} launched at {user2}. Epic!",
        "{user} kicked {user2}. That’s gotta leave a mark!",
        "Watch out! {user} delivered a powerful kick to {user2}.",
        "{user} didn’t hold back and kicked {user2}. Brutal!",
        "Kick combo! {user} unleashed fury on {user2}.",
        "{user} kicked {user2} with incredible force. Impressive!",
        "Boom! {user} kicked {user2}. Someone call a referee!",
        "A perfectly executed kick! {user} hit {user2} squarely.",
        "{user} went all out and kicked {user2}. Ouch!",
    ],
}

# Function to get random text and gif from predefined gifs
def defined_action_message(action):
    action = action.lower()
    if action not in messages or action not in gifs:
        raise ValueError("Unknown action.")
    text = random.choice(messages[action])
    gif = random.choice(gifs[action])
    return text, gif


# Function to get random text and gif from tenor api
def action_message(action):
    action = action.lower()
    if action not in messages or action not in gifs:
        raise ValueError("Unknown action.")
    text = random.choice(messages[action])
    gif = get_gif(['anime', action])
    return text, gif

