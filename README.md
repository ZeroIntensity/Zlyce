# Last updated: 1/19/21

## New Features
- Upgraded `snipe` command to only snipe messages from that channel.
- Added a snow falling background to [zlyce.xyz](https://zlyce.xyz).

## Credits
### Dependencies
- [discord.py](https://pypi.org/project/discord.py/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [flask](https://pypi.org/project/flask/)

### Developer

- [twitter.com/ZintensityDev](https://twitter.com/ZintensityDev)
- [youtube.com/ZeroIntensity](https://youtube.com/ZeroIntensity)
- [zintensity.net](https://zintensity.net)

## Commands
### Implemented Commands

- `help`
- `kick`
- `ban`
- `member`
- `server`
- `ping`
- `prefix`
- `info`
- `snipe`
- `random`
- `warn`
- `warnings`
- `unwarn`

### Command Usage Table

`[]` Is an optional argument.

`<>` Is not an optional argument.

`zlyce/` is the default prefix for the bot, so it will be used here. You can change the prefix using the following command: `zlyce/prefix <new prefix>` 

|Command Name|Aliases|Usage|
|----|-----|-------|
|Ban|`None`|`zlyce/ban <@member>`|
|Kick|`None`|`zlyce/kick <@member>`|
|Member|`user`|`zlyce/member [@member]`|
|Server|`guild`|`zlyce/server`|
|Info|`information`,`stats`|`zlyce/info`|
|Ping|`api`,`latency`|`zlyce/ping`|
|Prefix|`setprefix`|`zlyce/prefix <new prefix>`|
|Help|`None`|`zlyce/help [category/command]`|
|Snipe|`None`|`zlyce/snipe`|
|Random|`None`|`zlyce/random <text/number>`|
|Warn|`Infraction`|`zlyce/warn <@member> [reason]`|
|Unwarn|`Uninfraction`|`zlyce/unwarn <@member> <warn number>`|
|Warnings|`Infractions`,`Warns`|`zlyce/warns [@member]`|

## Notes
### Version Notes
Current Version: `development`

|MM/DD/YY|Version|Notes|
|----|-----|-------|
|1/19/21|`development`|Changed `snipe` command to only snipe messages from the current channel, and added a snow falling bg to [zlyce.xyz](https://zlyce.xyz).|

### Known Bugs

* [ ] `unwarn` command does not work.
* [ ] `warnings` works, but breaks after using the `unwarn` command. 
* [ ] [zlyce.xyz](https://zlyce.xyz) does not work for mobile users.


### Planned Features
**There are still more features to be planned**

- `mute` command.
- `lock` command.
- Upgraded `info` command.
- Add `support` page on [zlyce.xyz](https://zlyce.xyz).
- Add changelogs to [zlyce.xyz](https://zlyce.xyz).
- Add the `Command Usage Table` to [zlyce.xyz](https://zlyce.xyz).
- Add leveling system.
- Add econonmy system.