title: First steps in Shandalar
date: 2026-10-21
summary: The native client can walk the overworld, open the map, and visit its first village, Hornwell Mill.
---
**Shandalar Forever** is the native rewrite: a standalone Rust game built
on the [Fyrox](https://fyrox.rs/) engine. The rules and campaign state live
in a core with no engine code inside, so they can be tested without opening a
window. Fyrox handles drawing, input and the world.

What works today:

- Creating a character and starting a campaign.
- Walking the overworld with the arrow keys or the mouse, using the original
  direction tables, terrain speed and sprite frames.
- The **F2 map**, which only shows the land you have actually explored.
- A first **village visit**. Walk up to Hornwell Mill, step inside, and leave
  again to the same spot on the map.
- A short **duel fixture** with original card art.

Every step is checked against the frozen 1.0 game. The Hornwell Mill visit,
for example, opens at the same distance from the village as in the original,
and the same walk was played in the Linux client and in the browser build.

Next up are town services, encounters, full duels and saving.
