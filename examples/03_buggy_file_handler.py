Utility script to read, back up, and delete uploaded files. It sets up two folders, uploads and backups, then defines functions to handle the work.

One reads a file by building the path and opening it. Another copies it to the backup folder and prints a note. The delete function removes the file and logs it.

The log writer opens activity.log in append mode and adds the message. The main process reads the file, counts words by splitting on spaces, backs it up, and logs the filename and count. If the count is zero, it deletes the file.

It then lists all files in the upload folder, processes each one, and keeps a running total. At the end, it prints the grand total of words. The script runs when started directly.
