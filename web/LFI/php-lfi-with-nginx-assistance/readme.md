# Nginx + PHP-FPM environment

LFI(LocalFileIncludion) + RCE(RemoteCodeExecution)

get cpus and pid_max

This method takes advantage of the specification that if a php page running in a Nginx + PHP-FPM environment 
sends an HTTP request body with more than a certain amount of data (default 16K or more in a 64-bit environment), 
the data will be written to a temporary file.
By sending an HTTP request that contains code of the size that would cause writing to the temporary file and 
at the same time reads the temporary file using the LFI vulnerability, it is possible to execute arbitrary code.

The temporary file is stored under /var/lib/nginx/body/, 
and it is difficult to identify the name of the file, but it is possible to identify it by referring to it via procfs, 
by doing a brute force search in the range [process ID of the Nginx worker process] x [file descriptor]. 
The file descriptors are listed in /procfs. 
Note that PHP does not allow direct inclusion of /proc/[PID]/fd/[FD], 
so /proc/self/fd/[PID]/... /... /... /[PID]/fd/[FD] is also used as a reference technique via /[PID]/fd/[FD].

