This script is meant to deal with files that get uploaded somewhere. It sets up a couple folders one for the uploads and one for keeping copies safe. There is also a log that gets written to whenever something happens.

The path check part tries to stop anything tricky like going up folders. It reads the file content and figures out how many words are there. Then it makes a backup copy before doing anything else.

Logging happens after that. If the file turns out empty and the option is turned on it might get removed but only after the other steps. Errors get caught so the whole thing does not stop.

When running on everything in the folder it adds up the words across files. The main part just calls the batch function. Some of the error messages feel a bit basic but they get the job done most of the time.
Not sure if the logging is detailed enough for bigger use. 
