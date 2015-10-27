# EasyPlayer
### What is EasyPlayer?
`EasyPlayer` is a custom package for Source.Python, designed to make it easier for plugin developers to interfere with the player entities.
The main feature is `EasyPlayer`'s management of what I call "player effects", like burn and freeze, so that you can safely use them without having to worry about someone else changing them in their own plugins.

Imagine the following scenario *without* `EasyPlayer`: You apply a freeze to a player using `player.move_type = MoveType.NONE`. Meanwhile, someone else (an other developer) has their own plugin freeze everyone for 2 seconds whenever they're shot. We now have two plugins interacting with `player.move_type`, and it might cause the following:

 1. Player X gets shot and thus gets his `move_type` set to `MoveType.NONE` by the acts of the other developer's plugin.
 2. A second later, your plugin applies your freeze due to whatever reason (so this does nothing, he's already set to `MoveType.NONE`).
 3. An other second later (2 seconds since player X was shot) the other developer's plugin removes his freeze using `player.move_type = MoveType.WALK`.
 4. Your freeze, which was supposed to last more than a second, was also removed because of this.

If everyone were to use `EasyPlayer`, this wouldn't happen as it controls the way these player effects are applied and removed. `EasyPlayer` makes sure a player doesn't unfreeze until every freeze applied on him has ended.

### How to use EasyPlayer?
Currently you can call any of the following player effect functions on the player:

    player.burn()
    player.freeze()
    player.noclip()
    player.fly()
    player.godmode()

You can pass in a duration as an optional argument to make the effect temporary (instead of permanent): `player.noclip(3)` gives a noclip for three seconds.

All of these effects return a `_PlayerEffect` instance. To remove an infinite effect, or an effect with a duration that hasn't ended yet, store the returned `_PlayerEffect` instance and call `.cancel()` on it:

    freeze = player.freeze(10)
    # 5 seconds later:
    freeze.cancel()

Keep in mind that none of these function calls interfere with each other, so calling `.cancel()` might not unfreeze the player completely; it simply removes the freeze you've applied, but the player might still be frozen by someone else.

### Anything else EasyPlayer does?
You can subclass `EasyPlayer` as you please, and it shouldn't interfere with any of the mechanisms (unless you override some of the methods, obviously). You can create your own player effects to your subclass using the `@PlayerEffect` decorator. See examples from the bottom of `easyplayer.py`.
`EasyPlayer` also resets gravity on every round (because Source engine chose not to reset gravity although it resets all the other properties) and implements `from_userid(userid)` classmethod to get an instance directly from an userid.
There's even a built-in restriction system in `EasyPlayer`! You can use it by accessing player's `restrictions` set to restrict him from using certain weapons. Here's an example:

    from easyplayer import EasyPlayer
    from filters.weapons import WeaponClassIter
    from events import Event
 
    @Event
    def player_spawn(game_event):
        player = EasyPlayer.from_userid(game_event.get_int('userid'))
 
        # Allow only scout and knife
        player.restrictions = set(WeaponClassIter(return_types='classname')) - {'weapon_knife', 'weapon_scout'}
 
        # Actually, allow awp too
        player.restrictions.remove('weapon_awp')

### Final words
Keep in mind that `EasyPlayer` is still in beta, and might contain some bugs.
If you have any suggestions for improvements, or possibly new player effects you'd like to see, leave an issue (or a pull request) to this repository and I'll answer asap.
