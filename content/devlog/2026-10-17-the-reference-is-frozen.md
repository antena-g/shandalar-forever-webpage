title: The reference is frozen
date: 2026-10-17
summary: The recovered 1997 game is accepted as version 1.0, and becomes the yardstick for everything that follows.
---
Before writing a new Shandalar, we needed a Shandalar we could trust. The
recovered original game now runs as an accepted **1.0 build** under
Windows/Wine, and from here on it is frozen: it is the reference that the
native rewrite gets compared against.

The last stretch of work on it was about safety and rules:

- **Campaign saves** now stage all three original save files and keep a
  recovery journal until the save is fully written. A failed write keeps your
  old save, and an interrupted one finishes the next time the game starts.
- **Card behaviour** got a long audit of targeting and ability code. Kismet,
  Fireball (split and single-target), Ley Druid's land untap and Brainwash were
  replayed live.
- The source build passes **274 tests** and ten Rust ABI checks.

The 1.0 build stays exactly as it is. New work happens somewhere else.
