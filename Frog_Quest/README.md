# Frog Quest

## The Plot
### I thought it would be fun to spin something up a bit silly with elements from old RPGs thrown in. Our protagonist's name is Frogtamus Prime. He may not look like much but he used to be a prince until he was cursed! Fortunately his old pal Wizzo the wizard is around to help guide him through his quest. In order to break this curse he must simply kiss a princess. Unfortunately she's being held hostage by a rougue cowboy, and he won't give her up easily.

## Copyright business:
### Images: 
In today's world I thought it may be a better idea to stick with non-copyrighted material(thanks Nintendo & Disney). One way of doing this was to find free images online that weren't tied to anything that is blatantly intellectual property and to use AI to alter the image when attacking or if the original just didn't have the right features...also for removing backgrounds.

### Sounds:
Beyond the "HappyWheels" victory music and some cat sounds, I recorded the dialogue in my office. It's a £20 headset so be gentle on my voice acting skills, I promise I still have a normal day job.

## Our Hero: ![frog](https://github.com/user-attachments/assets/3079ad62-090b-4c38-8aaa-e6e76082b446)
## Controls & Basics:
Fairly basic, really. For now press the LEFT or RIGHT key to hop in the corresponding direction. SPACE to attack! I would like to add another image to match the UP key so that our hero has a way to attack those pesky birds that we'll cover later. The animation is really just shifting and alternating through different images. In the future I would like to get somewhere between 5 and 8 per moving sprite and just increment through them appropriately. 

Press the "Q" key to quit.

You can also skip through dialogue events using the "D" key.

Our hero has a health bar at the top and it is currently set to 5, where 5 hits will kill him. This can be adjusted in the Player class...just look for the comment "health".

## Friends:
### "Wizzo"![wizard](https://github.com/user-attachments/assets/9bbd124c-a7e4-4bab-9595-0e3574d7e105)
Wizzo being magical can communicate telepathetically with our frog. It is only on the first meeting of the game that you'll actually see him. This is also the onloy instance of a textbox appearing. I had intended to extend this to internal monologue with Frogtomus, but time slipped away for now. He still speaks to the player after each event to guide him to where he needs to go.
### The "Boat Master":  ![ship_captain](https://github.com/user-attachments/assets/3fd8a8ee-f4eb-46e6-858d-f77dcaa6744a)
This was a particulary tricky gentleman for the shear fact that I really wanted a background story for him and getting the flags and logic right were frustrating. If you immediately go left from the start you'll trigger a dialogue from him where he'll request that you retrieve 3 bags of kibble for him. He gives a brief explanation that things aren't going so great for him because he's nowhere near an ocean :). Therefore, money is tight and he offers his services driving a covered wagon. Which is fun considering the cowboy plot.

## Enemies:
### "Birdy"![bird](https://github.com/user-attachments/assets/c0dd301e-e375-4004-be8a-d32251744512)
The birds are typically harmless, but they randomly drop rocks directly at your position that will damage your health so you need to hop out of the way. 

### "The Cats"![cat](https://github.com/user-attachments/assets/afe54af7-5ac9-4f22-b1c7-f0fa924a4fad)
There are 3 images in use. They represent an idle, angry, and attacking state depending on their proximately to the player. On collision they will hurt the player. I set their health to one each for testing, but this can be adjusted pretty quickly in the cat module & Cat class.

### "The Cowboy"![cowboy_1](https://github.com/user-attachments/assets/4edae416-112a-46c0-a353-18a76398eaea)
This dastardly fellow is your final boss! He's quite a bit tougher, and since there's no healing system in place you'll have to face him carrying only your remaining health. He's beefier but his movement is less random than the cat's that are basically dropped on top of you. Defeat him and that's it.


## Known issues
###
The cloud had a fun feature where it whould move depending on your direction and was set to match your scroll speed. So if you walked to left it would move more quickly but would be idle walking right as you were traveling really fast! Idle it was supposed to move on it's own. The latest push to integrate the cowboy & relevent background is likely the culprit but it should be a simple fix.

###
The boat master... A great deal of time was spent trying to accomodate the correct logic to offer two sets of dialogue so there are loads of flags and checks in place that has had side affects. Primarily he doesn't go away on his own before the fight with the cowboy so you'll have to skip the dialogue (update 6 May 2025, this should work now). I didn't place the wizard's third dialogue in the skip logic as it's sort of the queue that you're almost done.

###
cats... Their behavior is a bit too random to control at the moment. There is conflicting facotrs in regards to timing & logic for when the kibble_collected flag is tripped and the cats disappear. They also seem to spawn on top of each other more than I intended. Anyways to be safe I set the maximum number of cats that can spawn to six and the kibble_collected flag trips when "cats_defeated >= max_cats - 3"... so 3 bags. It would also be cool to create droppable bags that are collected on collision.

###
text boxes... I only have one at the moment, but would like to expand this. I The issue with the boat master ate up alot of time so this is really a matter of debugging why his doesn't work and trying to replicate it.
### The end: ![image](https://github.com/user-attachments/assets/0ab5b15d-8c35-4742-816c-2acada8e3da1)
Well, there should really be more to the story....at least a happy ending! I left a brief dialgue at the end, but I really wanted to create something along the lines of a totally non-copyrighted entity known as "Princess Orange". 
