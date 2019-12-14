# Goal

Initally cloning WASMFile for Java class files. Once I can parse and disassemble the goal is to make a nice RE framework.

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
