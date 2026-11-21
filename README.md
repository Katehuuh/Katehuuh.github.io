# Shelf Life: web build

The files of an Unreal Engine 5.9 browser build (WebGPU, Lumen). This branch holds only the build; the page that
plays it is `demos/[GAME]-Shelf-Life.html` on `main`, which reads these files.

The game is made of packs from Fab and the Unreal Engine Marketplace, cooked into the containers here. They stay
under their Fab or Marketplace licences and belong to their makers: this build is here to be played, not to be taken
apart or reused.

<details>
<summary><b>The game in short (design document)</b></summary>

A browser game on Unreal Engine 5.9 (WebAssembly, WebGPU, Lumen): 44 mini games in 44 worlds, built from about
330 Fab packs, many of them claimed while they were free.

### The idea

Everything ever claimed on Fab and never opened sits boxed on an endless shelf: 1k crates, one for every title,
each with its own picture. Every crate is a world caught mid-scene, and you are the one thing on the shelf that
woke up. One figure keeps turning up in other crates, a mechanic: she is the "she" of several scenes below. The
Reaper waits on the bottom shelf.

### A fall

- You fall from crate to crate. A fall is six worlds, and a seventh if it has gone far enough up or down.
- Each world gives you a few seconds and one thing to do. Do it and the shelf files you one shelf up, towards the
  light. Do nothing, or fail, and you drop a shelf, where the worlds are darker.
- No world comes twice in a fall, and every world has a verb of its own.
- Three endings. A fall that has gone far enough up ends at the way out, Meadow Gate: step through and you are
  UNBOXED. One that has gone far enough down ends on the bottom shelf, in The Orb: fall there and you are DELETED.
  Anything else puts you back in your box, RE-SHELVED.
- The ending draws your fall as a path, world by world. `E` on the shelf opens ALL WORLDS: any world, whenever you
  are on the shelf.

### A world

- A level of a Fab pack as its maker built it, with the lighting adjusted where the browser needs it. The game adds
  a cast, one thing that is about to go wrong, and one verb.
- Fifteen to forty seconds. What to do is on the screen, with its keys, before it is needed.
- Two ends, both staged: the dark end is an event of the scene, not a "game over" card.
- The keys never change: `W` `A` `S` `D` move, the mouse looks, `SPACE` or a click does the world's one thing,
  `E` uses.

### The worlds

| Shelf | World | You | The scene |
|---|---|---|---|
| Bright | Bread Run | catch | The baker's cart has lost a wheel at the top of the lane, and the morning's loaves are bouncing down towards the mill stream. |
| Bright | Downhill | ride | The pram has rolled off the terrace where the family is having a barbecue, and it is gathering speed down the lanes towards the harbour. |
| Bright | Festival Street | disguise | The festival band marches up to the shrine, and only marchers in its uniform get through the gate. She is waiting on the other side. |
| Bright | Fjord | fly | A small jet with a dead engine is coming in low over the lake: the only flat place is the water off the fishing hut, where Gadget stands watching. |
| Bright | Harbour Lights | light | Fog is rolling in, a boat is still out, and the lamps of the lighthouse island are dark. |
| Bright | Market Day | lead | A wolf cub is lost among the market stalls, and the dog-catcher's van is on its way. |
| Bright | Night Fire | bark | A pan has caught fire in the kitchen and the family asleep upstairs has not woken. You are their dog. |
| Bright | Paper Round | throw | Six in the morning on Assetsville's main street: the bike will not stop, and every doorstep is waiting for its paper. |
| Bright | Sky Mail | grind | The windmill holds the islets up. One letter has to reach the tower before it stops. |
| Bright | The Garden | photograph | A fox has come over the wall for the last koi in the pond. Nobody else is watching. |
| Bright | The Keep | ring | A frost giant drives his horde over the bridge at the open gate. The watch sleeps. Ring the bell. |
| Bright | White Steps | balance | The wedding is at the top of the island, the cake is at the bottom, and between them are the white lanes of the hill, a wind off the sea and a goat. |
| Middle | Bazaar | climb | Kallari has the mechanic's toolbox and is laughing down from the roof. Climb up before she slips into the crowd. |
| Middle | Card Table | play a card | Morigesh deals you one hand across her table. Beat two of her three pieces and she opens the way on. Lose, and she keeps your heroes. |
| Middle | Crane | drop | A van full of stolen crates is threading the container yard for the gate, and you are in the crane cab with a container on the hook. |
| Middle | Desert City | fit | She is fixing the city gate. It has no power, and something is coming down the pass. |
| Middle | Fire Ship | push off | A galleon is burning against the town pier and the tide is turning. Shove her off before the fire takes the quay. |
| Middle | Hold-Up | tackle | A guard is wrestling a robber for his gun on the marble floor, and the crew is coming in off the street. |
| Middle | Last Orders | squeeze | A woman in the aisle is choking, and every face in the restaurant is turned to the gig down the avenue. |
| Middle | Last Train | follow | Closing time. The last train is at the island platform, and the man who just ran past you knows the way to it. |
| Middle | Outpost | snipe | Steel holds the outpost's breach against a walking gun, a hive beast has the squad pinned across the clearing, and you are on the ridge with one round. |
| Middle | Paladin's Stand | dash | A paladin is losing to a stone golem in the ruined village. Ten seconds to decide if it is your fight. |
| Middle | Rope Bridge | cut | You took the idol. Its guardian is awake, and the only way on is the rope bridge. |
| Middle | Salt Flats | ram | A truck with nobody at the wheel is heading for the edge of the flats. |
| Middle | Test Chamber | redirect | The android in the capsule is drowning. One laser crosses the trench the wrong way: bend it into the receiver. |
| Middle | The Alchemist | brew | The alchemist has turned to stone at his own bench with the cure half made. The recipe is painted on the wall behind him, and the cauldron is coming to the boil. |
| Middle | The Arena | duel | The crowd wants a fight, and the gorilla is already in the ring. |
| Middle | The Canal | row | A funeral gondola has slipped its mooring on the tide, candles lit and nobody aboard. Row after it before it reaches the lagoon. |
| Middle | The Gala | swap | Someone has poisoned her glass. The toast is raised when the aria next door ends. |
| Middle | The House | inspect | A music box is winding down in the twins' room. Find the one that plays and wind it, or the house forgets you. |
| Dark | Airlock | drift | The station has lost its air. Your crewmate is drifting toward the open airlock, and so are you. |
| Dark | Blackout | kill the lights | A chrome hunter comes down into the wet plaza, seeing only by the neon. Phase hides by the breaker board, and so do you. |
| Dark | Dragon Cave | sneak | Grux wants the gold beyond the bridge and has sent the smallest goblin across it. The dragon on the hoard is not quite asleep. |
| Dark | Dwarven Deep | mine | A stone golem is crossing the great bridge towards the last lit hall. Terra stands at the last joint, where the keystone holds the span it walks on. |
| Dark | Graveyard Shift | cast | The crypt is opening and the knights inside are getting up. |
| Dark | Quarantine | turn | She is older here. She is holding the shutter shut, alone, and something is coming up the tunnel. |
| Dark | Scarecrow Road | watch | The courtyard was empty when you came through the gate. They only move when nobody is looking. |
| Dark | The Deep | wade | The dive hall is flooding and something very large is at the glass. The medic is holding the last hatch for you. |
| Dark | The Deep End | notice | The hall repeats. If anything in it has changed, turn back; if nothing has, go on. |
| Dark | The Lock | pick | The jailer's torch is coming back along the corridor. She is chained in the cell beyond this door, and you have a bent nail. |
| Dark | The Mansion | hide | Something elegant is walking the halls, looking for you. The wardrobe is behind you. |
| Dark | Thin Ice | crawl | A pickup has gone through the ice road on the frozen bay. The driver is on its roof as it settles, and a whiteout is walking across the lake toward the hole. |
| The way out | Meadow Gate | step through | The way out is open at the far end of the meadow, and she is waiting by it. It is closing. |
| The bottom | The Orb | survive | The bottom shelf. The Reaper keeps what was never opened, and he has come for you. |

### Made of

- 1k Fab and Unreal Engine Marketplace titles. Every one is a crate on the shelf with its own picture, and the
  crate lights up once a world has shown the title.
- About 330 of them appear in a world: as its level, a character, a prop, an effect, an animation or a sound.
- The others are a crate and nothing more: plugins and editor tools that cannot run in a browser, titles that could
  not be downloaded, and titles whose world is planned and not built.

### How it is built

- Unreal Engine 5.9, web platform, unmodified. The desktop renderer in a browser tab: deferred shading, and Lumen
  global illumination where it holds up there (28 of the 44 worlds; open landscapes are lit by sun and sky alone).
  No Nanite in a browser (such meshes draw their fallback) and 4 GB of memory.
- C++ only. One class and one data file per world, and one director that stages a world, runs it, draws the screen
  and carries the fall from level to level.
- Every world has two scripted players, one that touches nothing and one that plays it. Both were run to their end
  in every world, natively and in Chrome.
- Design, code, staging and tests are the work of an AI model, Claude Fable 5.2, directing other model instances
  (one built each world from a brief, a second one judged it and fixed it), for a person who set the constraints
  and judged each version.

### How it reaches the browser

- The cooked game is 49 GB; with the world packs this branch holds about 67 GB, in files of at most 95 MiB. The
  page is under a megabyte on `main` and reads these files across origins from `raw.githubusercontent.com`, pinned
  to one commit.
- The engine reads a world a quarter of a megabyte at a time from about fifty of those files. A service worker in
  front of the engine's own answers those reads from "world packs" instead: for every world, the bytes it was
  recorded reading, in the order of need, as a few whole files (66 to 830 MB a world, half of them under 380 MB).
- The engine's log tells the page which world the game is opening. The page fetches that world's pack and shows what
  is being unpacked while the game itself cannot draw. A world fetched once stays in the browser (up to 8 GB).
- As a world begins, the game decides where the fall goes from it, for each of its two ends, and writes it to its
  log, where the page reads it: both worlds are fetched while the current one is played.

### Measured

| What | Value |
|---|---|
| Worlds | 44, each played to both of its ends by scripted players, natively and in Chrome |
| Frame rate | 35 to 57 frames a second in whole falls at the highest quality (a top-end desktop graphics card, 1920 x 1080) |
| Memory | at most 2.2 GB of the 4 GB a browser tab gives the engine |
| Page to shelf | 6 to 8 s |
| From the game's choice of a world to play, first visit | 6 to 20 s for most worlds on one fast connection: the level opens in 1 to 9 s, the rest is the card shown between worlds while shaders compile. The heaviest worlds can take half a minute |
| Requests to the file host in a fall | about 85 (about 1,000 before the world packs) |

### Known limits

- A desktop computer with a dedicated graphics card and Chrome (tested) or Edge. No phones.
- Packs authored for Nanite show coarser meshes than their makers intended.
- Sound levels between worlds were balanced by numbers and not by ear.
- The files are served from this branch: the first visit to a world waits for its download.

### Licences

The packs stay under their Fab or Unreal Engine Marketplace licences and belong to their makers. The cooked build is
here to be played, not to be taken apart or reused.

</details>
