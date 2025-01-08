from tenor import get_gif
import random

gifs = {
    "hug": [
        "https://media1.tenor.com/m/wUQH5CF2DJ4AAAAC/horimiya-hug-anime.gif",
        "https://media1.tenor.com/m/4OHcWvReiCgAAAAC/hugs.gif",
        "https://media1.tenor.com/m/8o4fWGwBY1EAAAAC/aharensan-aharen.gif"
    ],
    "punch": [
        "https://media1.tenor.com/m/p_mMicg1pgUAAAAC/anya-forger-damian-spy-x-family.gif",
        "https://media1.tenor.com/m/qDDsivB4UEkAAAAC/anime-fight.gif",
        "https://media1.tenor.com/m/54vXJe6Jj3kAAAAC/spy-family-spy-x-family.gif"
    ],
    "bite": [
        "https://media1.tenor.com/m/5mVQ3ffWUTgAAAAC/anime-bite.gif",
        "https://media1.tenor.com/m/n0DPyBDtZHgAAAAC/anime-bite.gif",
        "https://media1.tenor.com/m/0neaBmDilHsAAAAC/anime-bite.gif"
    ],
    "wave": [
        "https://media1.tenor.com/m/xsICn9T81LcAAAAC/roy-leops.gif",
        "https://media1.tenor.com/m/meiDmToBf4sAAAAC/anime-wave.gif",
        "https://media1.tenor.com/m/fraRGD3luZ4AAAAC/precure-precure-wave.gif"
    ],
    "kill": [
        "https://media1.tenor.com/m/cc1EzfBVr4oAAAAC/yandere-tagged.gif",
        "https://media1.tenor.com/m/NbBCakbfZnkAAAAC/die-kill.gif",
        "https://media1.tenor.com/m/SIrXZQWK9WAAAAAC/me-friends.gif"
    ],
    "lick": [
        "https://media1.tenor.com/m/hBwkISiqNI0AAAAC/shura-hiwa-lamer.gif",
        "https://media1.tenor.com/m/ps7jDcUG53MAAAAC/blue-archive-arona.gif",
        "https://media1.tenor.com/m/M8x5j8jGZhoAAAAC/lick.gif"
    ],
    "kiss": [
        "https://media1.tenor.com/m/3OW6j6x6Oh8AAAAC/cute-anime-his-and-her-circumstances.gif",
        "https://media1.tenor.com/m/1TDajWHZF_IAAAAC/berran%C4%B1n-opucugu.gif",
        "https://media1.tenor.com/m/xDCr6DNYcZEAAAAC/sealyx-frieren-beyond-journey%27s-end.gif"
    ],
    "spank": [
        "https://media1.tenor.com/m/Sp7yE5UzqFMAAAAC/spank-slap.gif",
        "https://media1.tenor.com/m/sdSmiixaAj0AAAAC/anime-anime-girl.gif",
        "https://media1.tenor.com/m/iz6t2EwKeYMAAAAC/rikka-takanashi-chunibyo.gif"
    ],
    "kick": [
        "https://media1.tenor.com/m/Lyqfq7_vJnsAAAAC/kick-funny.gif",
        "https://media1.tenor.com/m/k9QsoTYjJSUAAAAC/kick-anime.gif",
        "https://media1.tenor.com/m/XLrTcljAp3YAAAAC/roshidere-anime.gif"
    ],
    "pat": [
        "https://media1.tenor.com/m/kIh2QZ7MhBMAAAAd/tsumiki-anime.gif",
        "https://media1.tenor.com/m/pvF8xcytu1YAAAAd/pat.gif",
        "https://media1.tenor.com/m/E6fMkQRZBdIAAAAd/kanna-kamui-pat.gif"
    ],
    "poke": [
        "https://media1.tenor.com/m/3dOqO4vVlr8AAAAd/poke-anime.gif",
        "https://media1.tenor.com/m/0wPms8tS0eoAAAAd/boop-poke.gif",
        "https://media1.tenor.com/m/7iV_gBGrRAUAAAAd/boop-poke.gif",
    ],
    "bonk": [
        "https://media.tenor.com/bO1H2Zv_5doAAAAM/mai-mai-san.gif",
        "https://media.tenor.com/Gg4wSkuH6b4AAAAM/anime-manga.gif",
        "https://media.tenor.com/D6Ln3UPAdKcAAAAM/bonk-anime.gif",
    ],
    "wag": [
        "https://media.tenor.com/aqrVj-YBUucAAAAM/shino-wag.gif",
        "https://media.tenor.com/dkX3A1YEDSwAAAAM/shy-anime.gif",
        "https://media.tenor.com/41bzP_VeqnoAAAAj/please-shake.gif",
    ],
    "stare": [
        "https://media.tenor.com/SEEMSDLdDugAAAAM/anya-forger.gif",
        "https://media.tenor.com/f3ZQlg1--pUAAAAM/alya-sometimes-hides-her-feelings-in-russian-alya.gif",
        "https://media.tenor.com/YfqM8h3_6NEAAAAM/rin-anime.gif",
    ],
}


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

