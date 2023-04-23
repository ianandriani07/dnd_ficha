from character_def import Features

# Artificer

MAGICAL_TINKERING = Features('Magical Tinkering', {1: """You've learned how to invest a spark of magic into mundane objects. To use this ability, you must have thieves' tools or artisan's tools in hand. You then touch a Tiny nonmagical object as an action and give it one of the following magical properties of your choice:

• The object sheds bright light in a 5-foot radius and dim light for an additional 5 feet.
• Whenever tapped by a creature, the object emits a recorded message that can be heard up to 10 feet away. You utter the message when you bestow this property on the object, and the recording can be no more than 6 seconds long.
• The object continuously emits your choice of an odor or a nonverbal sound (wind, waves, chirping, or the like). The chosen phenomenon is perceivable up to 10 feet away.
• A static visual effect appears on one of the object's surfaces. This effect can be a picture, up to 25 words of text, lines and shapes, or a mixture of these elements, as you like.

The chosen property lasts indefinitely. As an action, you can touch the object and end the property early.
You can bestow magic on multiple objects, touching one object each time you use this feature, though a single object can only bear one property at a time. The maximum number of objects you can affect with this feature at one time is equal to your Intelligence modifier (minimum of one object). If you try to exceed your maximum, the oldest property immediately ends, and then the new property applies."""})

# Barbarian

RAGE = Features('Rage', {1: """In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action.

While raging, you gain the following benefits if you aren't wearing heavy armor:

• You have advantage on Strength checks and Strength saving throws.
• When you make a melee weapon attack using Strength, you gain a bonus to the damage roll that increases as you gain levels as a barbarian, as shown in the Rage Damage column of the Barbarian table.
• You have resistance to bludgeoning, piercing, and slashing damage.

If you are able to cast spells, you can't cast them or concentrate on them while raging.

Your rage lasts for 1 minute. It ends early if you are knocked unconscious or if your turn ends and you haven't attacked a hostile creature since your last turn or taken damage since then. You can also end your rage on your turn as a bonus action.

Once you have raged the number of times shown for your barbarian level in the Rages column of the Barbarian table, you must finish a long rest before you can rage again."""})

DANGER_SENSE = Features('Danger Sense', {
                        2: """You gain an uncanny sense of when things nearby aren't as they should be, giving you an edge when you dodge away from danger. You have advantage on Dexterity saving throws against effects that you can see, such as traps and spells. To gain this benefit, you can't be blinded, deafened, or incapacitated."""})

RECKLESS_ATTACK = Features('Reckless Attack', {
                           2: """You can throw aside all concern for defense to attack with fierce desperation. When you make your first attack on your turn, you can decide to attack recklessly. Doing so gives you advantage on melee weapon attack rolls using Strength during this turn, but attack rolls against you have advantage until your next turn."""})

EXTRA_ATTACK = Features('Extra Attack', {
                        5: "You can attack twice, instead of once, whenever you take the Attack action on your turn."})

FAST_MOVEMENT = Features('Fast Movement', {
                         5: "Your speed increases by 10 feet while you aren't wearing heavy armor."})

FERAL_INSTINCT = Features('Feral Instinct', {7: """Your instincts are so honed that you have advantage on initiative rolls.

Additionally, if you are surprised at the beginning of combat and aren't incapacitated, you can act normally on your first turn, but only if you enter your rage before doing anything else on that turn."""})

BRUTAL_CRITICAL = Features('Brutal Critical', {9: "You can roll one additional weapon damage die when determining the extra damage for a critical hit with a melee attack.",
                           13: "You can roll three additional weapon damage die when determining the extra damage for a critical hit with a melee attack.", 17: "You can roll one additional weapon damage die when determining the extra damage for a critical hit with a melee attack."})

RELENTLESS_RAGE = Features('Relentless Rage', {11: """Your rage can keep you fighting despite grievous wounds. If you drop to 0 hit points while you're raging and don't die outright, you can make a DC 10 Constitution saving throw. If you succeed, you drop to 1 hit point instead.

Each time you use this feature after the first, the DC increases by 5. When you finish a short or long rest, the DC resets to 10."""})

PERSISTENT_RAGE = Features('Persistent Rage', {
                           15: "Your rage is so fierce that it ends early only if you fall unconscious or if you choose to end it."})

INDOMITABLE_MIGHT = Features('Indomitable Might', {
                             18: "If your total for a Strength check is less than your Strength score, you can use that score in place of the total."})

# Bard

BARDIC_INSPIRATION = Features('Bardic Inspiration', {1: """You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d6.

Once within the next 10 minutes, the creature can roll the die and add the number rolled to one ability check, attack roll, or saving throw it makes. The creature can wait until after it rolls the d20 before deciding to use the Bardic Inspiration die, but must decide before the DM says whether the roll succeeds or fails. Once the Bardic Inspiration die is rolled, it is lost. A creature can have only one Bardic Inspiration die at a time.

You can use this feature a number of times equal to your Charisma modifier (a minimum of once). You regain any expended uses when you finish a long rest.""", 5:  """You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d8.

Once within the next 10 minutes, the creature can roll the die and add the number rolled to one ability check, attack roll, or saving throw it makes. The creature can wait until after it rolls the d20 before deciding to use the Bardic Inspiration die, but must decide before the DM says whether the roll succeeds or fails. Once the Bardic Inspiration die is rolled, it is lost. A creature can have only one Bardic Inspiration die at a time.

You can use this feature a number of times equal to your Charisma modifier (a minimum of once). You regain any expended uses when you finish a long rest.""", 10: """You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d10.

Once within the next 10 minutes, the creature can roll the die and add the number rolled to one ability check, attack roll, or saving throw it makes. The creature can wait until after it rolls the d20 before deciding to use the Bardic Inspiration die, but must decide before the DM says whether the roll succeeds or fails. Once the Bardic Inspiration die is rolled, it is lost. A creature can have only one Bardic Inspiration die at a time.

You can use this feature a number of times equal to your Charisma modifier (a minimum of once). You regain any expended uses when you finish a long rest.""", 15: """You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d12.

Once within the next 10 minutes, the creature can roll the die and add the number rolled to one ability check, attack roll, or saving throw it makes. The creature can wait until after it rolls the d20 before deciding to use the Bardic Inspiration die, but must decide before the DM says whether the roll succeeds or fails. Once the Bardic Inspiration die is rolled, it is lost. A creature can have only one Bardic Inspiration die at a time.

You can use this feature a number of times equal to your Charisma modifier (a minimum of once). You regain any expended uses when you finish a long rest."""})

JACK_OF_ALL_TRADES = Features('Jack of All Trades', {
                              2: """You can add half your proficiency bonus, rounded down, to any ability check you make that doesn't already include your proficiency bonus."""})

SONG_OF_REST = Features('Song of Rest', {2: "You can use soothing music or oration to help revitalize your wounded allies during a short rest. If you or any friendly creatures who can hear your performance regain hit points at the end of the short rest by spending one or more Hit Dice, each of those creatures regains an extra 1d6 hit points.", 9: "Beginning at 2nd level, you can use soothing music or oration to help revitalize your wounded allies during a short rest. If you or any friendly creatures who can hear your performance regain hit points at the end of the short rest by spending one or more Hit Dice, each of those creatures regains an extra 1d8 hit points.",
                        13: "Beginning at 2nd level, you can use soothing music or oration to help revitalize your wounded allies during a short rest. If you or any friendly creatures who can hear your performance regain hit points at the end of the short rest by spending one or more Hit Dice, each of those creatures regains an extra 1d10 hit points.", 17: "Beginning at 2nd level, you can use soothing music or oration to help revitalize your wounded allies during a short rest. If you or any friendly creatures who can hear your performance regain hit points at the end of the short rest by spending one or more Hit Dice, each of those creatures regains an extra 1d12 hit points."})

FONT_OF_INSPIRATION = Features('Font of Inspiration', {
                               5: "You regain all of your expended uses of Bardic Inspiration when you finish a short or long rest."})

COUNTERCHARM = Features('Countercharm', {6: "You gain the ability to use musical notes or words of power to disrupt mind-influencing effects. As an action, you can start a performance that lasts until the end of your next turn. During that time, you and any friendly creatures within 30 feet of you have advantage on saving throws against being frightened or charmed. A creature must be able to hear you to gain this benefit. The performance ends early if you are incapacitated or silenced or if you voluntarily end it (no action required)."})

SUPERIOR_INSPIRATION = Features('Superior Inspiration', {
                                20: "When you roll initiative and have no uses of Bardic Inspiration left, you regain one use."})

# Paladin

CHANNEL_DIVINITY = Features('Channel Divinity', {2: """You gain the ability to channel divine energy directly from your deity, using that energy to fuel magical effects. You start with two such effects: Turn Undead and an effect determined by your domain. Some domains grant you additional effects as you advance in levels, as noted in the domain description.

When you use your Channel Divinity, you choose which effect to create. You must then finish a short or long rest to use your Channel Divinity again.

Some Channel Divinity effects require saving throws. When you use such an effect from this class, the DC equals your cleric spell save DC. You can only use it once.""", 6: """You gain the ability to channel divine energy directly from your deity, using that energy to fuel magical effects. You start with two such effects: Turn Undead and an effect determined by your domain. Some domains grant you additional effects as you advance in levels, as noted in the domain description.

When you use your Channel Divinity, you choose which effect to create. You must then finish a short or long rest to use your Channel Divinity again.

Some Channel Divinity effects require saving throws. When you use such an effect from this class, the DC equals your cleric spell save DC. You can only use it twice.""", 18: """You gain the ability to channel divine energy directly from your deity, using that energy to fuel magical effects. You start with two such effects: Turn Undead and an effect determined by your domain. Some domains grant you additional effects as you advance in levels, as noted in the domain description.

When you use your Channel Divinity, you choose which effect to create. You must then finish a short or long rest to use your Channel Divinity again.

Some Channel Divinity effects require saving throws. When you use such an effect from this class, the DC equals your cleric spell save DC. You can only use it three times."""})

CHANNEL_DIVINITY_TURN_UNDEAD = Features('Channel Divinity: Turn Undead', {2: """As an action, you present your holy symbol and speak a prayer censuring the undead. Each undead that can see or hear you within 30 feet of you must make a Wisdom saving throw. If the creature fails its saving throw, it is turned for 1 minute or until it takes any damage.

A turned creature must spend its turns trying to move as far away from you as it can, and it can't willingly move to a space within 30 feet of you. It also can't take reactions. For its action, it can use only the Dash action or try to escape from an effect that prevents it from moving. If there's nowhere to move, the creature can use the Dodge action."""})

DESTROY_UNDEAD = Features('Destroy Undead', {
                          5: "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below a certain threshold, as shown in the Cleric table above."})

DIVINE_INTERVENTION = Features('Divine Intervention', {10: """you can call on your deity to intervene on your behalf when your need is great.

Imploring your deity's aid requires you to use your action. Describe the assistance you seek, and roll percentile dice. If you roll a number equal to or lower than your cleric level, your deity intervenes. The DM chooses the nature of the intervention; the effect of any cleric spell or cleric domain spell would be appropriate. If your deity intervenes, you can't use this feature again for 7 days. Otherwise, you can use it again after you finish a long rest.""", 20: """You can call on your deity to intervene on your behalf when your need is great.

Imploring your deity's aid requires you to use your action. Describe the assistance you seek. The DM chooses the nature of the intervention; the effect of any cleric spell or cleric domain spell would be appropriate. When your deity intervenes, you can't use this feature again for 7 days. Otherwise, you can use it again after you finish a long rest."""})
