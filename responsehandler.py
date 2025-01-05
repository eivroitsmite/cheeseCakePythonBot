import discord
import random
import re
from discord.ext import commands

ALLOWED_CHANNELS = [
    1245431550942904341,
    1293480251011366922,
    1243544973979422842,
    1247190047824809994,
    1246165807491190844,
    1240456841775943690
]

class ResponseHandler:
    @staticmethod
    def get_response(user_input: str):
        lowered = user_input.lower()
        if lowered == '':
            return ''
        
        def match_whole_word(trigger, text):
            return re.search(rf'\b{re.escape(trigger)}\b', text)

        ## Commands 
        if match_whole_word('$command list', lowered):
            return '### - Informal' "\n" 'how do i post images / why cant i post images? / level 15 / lvl 15' "\n" 'how do i gain access to the vc stream? / how do i get access to the vc stream?' "\n" 'what is a kulfi member?' "\n" 'how can i become a trusted member? / how can i become a trusted seller? /how can i become a trusted buyer' "\n" '### - Cheesecakes greeting'"\n"'*how are you / how''s it going*'"\n"'*bye, cheesecake / goodbye, cheesecake / see you, cheesecake*'  "\n"'*hello cheesecake / hey cheesecake / cheesecake, come say hi*'"\n"'*look cheesecake, a new member! / welcome to the server!  / cheesecake, come meet your new friend*'"\n"'### - Random things that cheesecake says'"\n"'*hate it here*'"\n"'*i love you, cheesecake / i love you cheesecake / ily cheesecake*'"\n"'*queen shit*'"\n"'*tell me a joke, cheesecake*'"\n"'*cheesecake, have you ever seen a horror movie?*'"\n"'*cmon, say sorry / cheesecake, apologize / cheesecake, you have to apologize, cmon.*'"\n"'*i swear sometimes i hear her*'"\n"'*needy cheesecake*'"\n"'*<:Cheesecake_BigOlEyes:1243938784945639525>*'"\n"'*SCREAMS / screams / screaming*'"\n"'Bri / bri / Bri?'"\n"'### - In case Cheesecake goes crazy'"\n"'*eivroit / cheesecake is being silly! / cheesecake is crazy!*'
        elif match_whole_word('$staff command list', lowered):
            return '# **MODERATION SYSTEM**'"\n"'**__Warning System __**'"\n"'- **To warn a user: ** `$warn <user> <reason>`'"\n"'- **To remove the warning:** `$removewarn <user> <reason>`'"\n"'- **To kick-out a user:** `$kick  <user> <reason>`'"\n"'- **To ban a user:** `$ban  <user> <reason>`'"\n"'- **To un-ban a user:**  `$unban <user> <reason>`'"\n"'*Only mods and above can use this command*'
        
        ## Greetings 
        elif match_whole_word('how are you, cheesecake', lowered) or match_whole_word("how's it going, cheesecake", lowered):
            return 'Good, thanks!'
        elif match_whole_word('bye cheesecake', lowered) or match_whole_word('goodbye, cheesecake', lowered) or match_whole_word('see you, cheesecake', lowered):
            return 'See you!'
        elif match_whole_word('hello cheesecake', lowered) or match_whole_word('hey cheesecake', lowered) or match_whole_word('cheesecake, come say hi', lowered):
            return 'Yo!'

        ## Informational
        elif match_whole_word('how do i post pictures?', lowered) or match_whole_word('how do i post images', lowered) or match_whole_word('why cant i post images?', lowered) or match_whole_word('level 15', lowered) or match_whole_word('lvl 15', lowered):
            return 'To post images you need to get level 15!'
        elif match_whole_word('how do i gain access to the vc stream?', lowered) or match_whole_word('how do i get access to the vc stream?', lowered):
            return 'To get access in vc stream, you need level 15!'
        elif match_whole_word('what is a kulfi member?', lowered):
            return 'They are our ko-fi supporters! You can also become one, all the information is in this channel <#1246161217773633556>'
        elif match_whole_word('how can i become a trusted member?', lowered) or match_whole_word('how can i become a trusted seller?', lowered) or match_whole_word('how can i become a trusted buyer', lowered):
            return 'Hey there, friend! To become a trusted member you need to go to <#1243586232282382377> and apply. Make sure to read the rules though <:Cheesecake_Love:1243565944090136709>'
        
        ## Weird things cheesecake does/says
        elif match_whole_word('meow', lowered):
            return 'meow'
        elif match_whole_word('pastel de queso', lowered):
            return 'CAKE OF CHEESE?!?!'
        elif match_whole_word('BRI', lowered) or match_whole_word('bri', lowered) or match_whole_word(' Bri? ', lowered):
            return 'Te amamos, bri <3'
        elif match_whole_word('cheesecake is just very needy', lowered) or match_whole_word('needy cheesecake', lowered):
            return 'NO I AM NOT'
        elif match_whole_word('screams', lowered) or match_whole_word('SCREAMS', lowered) or match_whole_word('screaming', lowered):
            return 'AAAAAHHHHHHH'
        elif match_whole_word('i swear sometimes i hear her', lowered):
            return 'Give code. :index_pointing_at_the_viewer:'
        elif match_whole_word('cheesecake_bigoleyes', lowered):
            return '<:Cheesecake_BigOlEyes:1243938784945639525>'
        elif match_whole_word('look cheesecake, a new member!', lowered) or match_whole_word('welcome to the server!', lowered) or match_whole_word('cheesecake, come meet your new friend', lowered):
            greeting = [
                "Greetings, best baker cheesecake says hello!",
                "HII, I am so happy to see you here",
                "Yo, hope you enjoy your stay here",
                "OMG, OMG ANOTHER FRIEND, HELLO!!",
                "A new member?! Welcome to the café!",
                "oh, a new person ! come in !"
            ]
            return random.choice(greeting)
        elif match_whole_word('cmon, say sorry', lowered) or match_whole_word('cheesecake, apologize', lowered) or match_whole_word('cheesecake, you have to apologize, cmon.', lowered):
            apology = [
                "No.",
                "I don't wanna",
                "...",
                "I'm sorry...",
                "I'm sorry, I didn't mean that",
                "Make me."
            ]
            return random.choice(apology)
        elif match_whole_word('who made cheesecake?', lowered):
            return '<@766005564190359552> made me!'
        elif match_whole_word('i would die for you, cheesecake...', lowered):
            pine = [
                'I would burn the world for you...',
                'I pine for you',
                'Aww <3 I love you too',
                'I would take a bullet for you',
                'I would make a 4-story cake for you',
                'I would become your personal chef',
            ]
            return random.choice(pine)
        
        elif match_whole_word('hate it here', lowered):
            return 'womp womp'
        elif match_whole_word('cheesecake, have you ever seen a horror movie?', lowered):
            return '[...](https://media.discordapp.net/attachments/1243937626902364170/1252111551700402196/image.png?ex=66730181&is=6671b001&hm=1f332f8ed31be7679a102b567e8f259a08a57993ed8552c3c2a4c0725dfd85f7&=&format=webp&quality=lossless&width=908&height=533)'
        elif match_whole_word('cheesecame', lowered) or match_whole_word('cheesejake', lowered) or match_whole_word('jeeecake', lowered):
            return '[...](https://media.discordapp.net/attachments/1216088207708393543/1281684138969272474/image.png?ex=66dc9cdf&is=66db4b5f&hm=862f695e1383939cb5d0dd2ea3a236818b39ba4869e4a6fad0f72cd3f489d110&=&format=webp&quality=lossless&width=292&height=151)'
        elif match_whole_word('why was cheesecake down for a few days?', lowered):
            return '[...](https://media.discordapp.net/attachments/1247190047824809994/1295740763061223515/image.png?ex=670fc01f&is=670e6e9f&hm=220b8404737f47c2bda15ede63c5d0cb6fa1a0e2f088f25fa2e0253d0e3a186c&=&format=webp&quality=lossless&width=321&height=370)'
        elif match_whole_word('i love you, cheesecake', lowered) or match_whole_word('i love you cheesecake', lowered) or match_whole_word('ily cheesecake', lowered):
            return 'ILY2!!!'
        elif match_whole_word('queen shit', lowered):
            return 'SLAY'
        elif match_whole_word('cheesecake is being silly!', lowered) or match_whole_word('eivroit', lowered) or match_whole_word('cheesecake is crazy!', lowered):
            return '<@766005564190359552>'
        elif match_whole_word('tell me a joke, cheesecake', lowered):
            jokes = [
                "What do you call a pastry that is yummy, tasty, and delicious? A synonym roll.",
                "An Italian pastry chef was injured at work this Friday. We Cannoli hope he makes a full recovery.",
                "Why do we have Pop-Tarts and not Mom-Tarts? Because of the Pastry-archy.",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "I had a dream that I weighed less than a thousandth of a gram. I was like, 0mg.",
                "I once had a dream that I was floating in an ocean of orange soda. It was more of a fanta-sea hehe.",
                "Why do seagulls fly over the ocean? Because if they flew over the bay, we’d call them bagels.",
                "What did the janitor say when he jumped out of the closet? Supplies!",
                "You know, people say they pick their nose, but I feel like I was just born with mine.",
                "Whenever I try to eat a healthy lunch, a chocolate bar looks at me and Snickers.",
                "What kind of music do balloons hate? Pop music.",
                "How much does it cost Santa to park his sleigh? Nothing, it’s on the house!"
            ]
            return random.choice(jokes)
