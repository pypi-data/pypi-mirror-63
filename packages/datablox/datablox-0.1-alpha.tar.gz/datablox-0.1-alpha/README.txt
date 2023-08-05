# datablox

Testing distributed hashchains (or the unmentionable square shaped linked thingy,) __it has other uses aside from meme coins, I think__.

__disclaimer__: Datablox is just something I'm kicking around as a nice to have *and* a learning experience.  If you want to send me an email or pull request pointing out something that is blatantly obvious to even a competent programmer: please do, I could use the help.

TL;DR **don't read or use this code, it'll make you want to point at me and laugh**

## The premise.

A datablox instance is a linked list of immutable blocks stored on the filesystem.  Each individual block can store an arbitrary dictionary of data but can never be changed, instead a new block must be added.  