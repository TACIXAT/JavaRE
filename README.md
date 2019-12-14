Java RE tools fucking suck! No one updates them! Maybe there is a good decompiler but there is nothing around it to make it useful. Some RE applications will have variable renaming, some will have search, some will support unicode, some will have cross references, but none have it all and most haven't been updated in years!

Rather than being another project that strings together a bunch of no-longer-developed decompilers, this one aims to just look at the bytecode. Like if I can read x86 tf am I not trying to read some JVM?

Initial goal will be Java 7, since that's what I'm looking at rn. After that we'll target all the LTS releases (8, 11, ...?). Should be relatively easy to pull out instruction specifications from the online Java pages (see gen.py somewhere in this repo). About 60% instructions are a single byte or whatever, so we should only have to think about 50 of them. I'd wager the worse of my two dogs that most those 50 are automatble too.

# Goal

Initally cloning WASMFile for Java class files. Once I can parse and disassemble the goal is to make a nice RE framework. Let's see what I can get done in a weekend!

## Target Features

* Handle single class
* Handle JAR file
* Variable renaming
  - Keep a sqlite db with mapings
* Find definition
  - Use JAR paths
  - Index where we need to
* Cross references / uses
  - I guess we need to index for this
  - Maybe some hack can be done with the constant pools
* Commenting
  - Store in db with insn offset
* ASCII / TUI control flow graphs (prob the hardest part)
  - Gotta look up CFG layout algorithms / ask binary ninja folks
* Tracking stack values (future)
  - We'll have how each instruction affects the stack
  - Shouldn't be too hard to have a .model(stack: List)
  - Biggest q rn is what do we put on it for unknowns?
  - Z3 variables would be dope
  - I'll have a better idea of this as I look at JVM more
  - Thinking about this more, this is a pretty important feature
