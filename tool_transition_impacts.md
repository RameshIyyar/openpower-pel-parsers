# Tool transition impacts

| Operation  | C++ peltool | Old Python peltool | New Python peltool | Who impactes |
| -----------|:-----------:|--------------------|:------------------:|:------------------:|
| Display a PEL using its Raw PEL file | peltool --file "file" | peltool.py -f/--file "file" | Same | No |
| Display a PEL based on its ID | peltool -i/--id "pel_id" | NA | peltool.py -i/--id "pel_id" | No |
| Display a PEL based on its BMC Event ID | peltool --bmc-id "bmc_event_id" | NA | peltool.py --bmc-id "bmc_event_id" | No | 
| Display all PELs | peltool -a | NA | peltool.py -a/--all-pels | No |
| List PELs | peltool -l | NA | peltool.py -l/--list | No |
| Show number of PELs | peltool -n | NA | peltool.py -n/--show-pel-count | No |
| Reverse order of output | peltool -lr | NA | peltool.py -l -r/--reverse | No |
| Include hidden PELs | peltool -lh | NA | peltool.py -l -H/--hidden | C++ tool users |
| Include informational PELs | peltool -l -f/--info | NA | peltool -l -S 'informational' | C++ tool users |
| List only critical system terminating PELs | peltool -l -t/--termination | NA | peltool.py -lO -t/--termination | C++ tool users | 
| Delete a PEL based on its ID | peltool -d/--delete "pelID" | NA | peltool.py -d/--delete "pelID" | No |
| Delete all PELs | peltool -D/--delete-all | NA | peltool.py -D/--delete-all | No |
| File containing SRC regular expressions to ignore | peltool -l -s/--scrub "src_scrub_file" | NA | peltool.py -l --scrub "src_scrub_file" | C++ tool users |
| Display PEL(s) in hexdump instead of JSON | peltool -x | NA | peltool.py -x/--hex | No |
| List or display archived PELs (Only in BMC env, use -p for non-BMC env) | peltool --archive | NA | peltool.py -A/--archive | No |
| Only parse serviceable (not info/recovered) PELs | NA | peltool.py -s/--serviceable | Same | No, is it needed? It is default operation for -l/-a/-n |
| Only parse non-serviceable (info/recovered) PELs | NA | peltool.py -n/--non-serviceable | peltool.py -N/--non-serviceable | Python tool users |
| Skip loading plugins | NA | peltool.py -p/--no-plugins | peltool.py -P/--skip-parser-plugins | No, dev only options |
| Process all files in a directory and save as filename.json | NA | peltool.py -d/--directory "input_directory" -o/--output-dir "output_directory" | peltool.py -j/--json -p/--path "input_directory" -o/--output-dir "output_directory" | Python tool users |
| Directory to write output files when processing a directory | NA | peltool.py -o/--output-dir "output_directory" | Same | No |
| Used with -d, only look for files with this extension (e.g. ".pel") | NA | peltool.py -e/--extension | Same | No |
| Delete original file after parsing | NA | peltool.py -x/--delete | peltoolpy -c/--clean | Python tool users |
| Specify path to PELs (non-BMC enviroment only) | NA | NA | peltool.py -p/--path "pels_path" | No
| Get PELs based on the given severities along with servicable logs | NA | NA | peltool.py -S "severity1,severity2,..." | No |
| Get PELs based on the given severities | NA | NA | peltool.py -l -O/--only -S "severity1,..." | No |


### Which tool users need to compromise??

#### Python tool users

Some users will install the Python peltool themselves by cloning the openpower-pel-parsers repo, so we need to compromise them.

**Note:** We should not alter any of the existing Python peltool options (`-n`, `-d`, `-x`, and `--delete`).

#### C++ tool users

The C++ peltool is always included with the BMC image, and users run peltool from the BMC console. Therefore, we could create a shell script named peltool to translate the old options into the new ones, ensuring there is no impact on the users. This approach is feasible with zero impact.

#### How do we translate the old options into the new options?

Let's create a shell script named `peltool` with below mapping and package into BMC image so that C++ peltool users won't need to modify their code.

```

if "-n" then
   # show pels counts, will it be used with other option "-lhn"???
   use "-N"
if "-lh" or "-l -h" then
   # Include hidden PELs along with Serviceable logs
   use "-lH"
if "-lf" or or "-l -f" or "-l --info" then
   # Include information PELs along with Servicable logs
   use "-l -S 'informational'"
if "-lt" or "-l -t " or "-l --termination" then
   # List only system termination PELs
   use "-lOt"
if "-d" or "--delete" then
   # Delete the given PEL id
   use "-c"
if "-D or "--delete-all" then
   use "-C"
if "-ls" or "-l -s" or "-l --scrub"
   # Ignore matched SRCs which was given in the input file
   use "-l --scrub"
if "-x" then
   # Print the PELs in hex format
   use "-X"

# All other options need to pass as it to the Python peltool.
# Note, all options combination need to work as like C++ peltool
```

#### Fix current new Python peltool options, meaning less but no other alternative.

- `-N` => `-n` // non-serviceable logs
- `-n` => `-N` // PELs count
- `-d` => `-c` // Delete a PEL, Delete -> Clear
- `--delete` => `--clear` // Delete a PEL, Delete -> Clear
- `-D` => `-C` // Delete all PELs, Delete All -> Clear All
- `--delete-all` => `--clear-all` // Delete all PELs, Delete All -> Clear All
- `-c` => `-x` // Clean a processed PELs file
- `--clean` => `--delete` // Clean a processed PELs file
- `-j` -> `-d` // Write PELs (which are available in the given directory) into JSON format
- `--json` -> `--directory` // Write PELs (which are available in the given directory) into JSON format

**Note:** We don't need to change `--skip-parser-plugins` to `--no-plugins` since it's a development-only option. This is the only option we are renaming in the new Python tool.

# Final peltool option mapping 

| Operation  | C++ peltool | Old Python peltool | New Python peltool | Who impactes | Conflicts |
| -----------|:-----------:|--------------------|:------------------:|:------------------:|:------------------:|
| Display a PEL using its Raw PEL file | peltool --file "file" | peltool.py -f/--file "file" | Same | No | - |
| Display a PEL based on its ID | peltool -i/--id "pel_id" | NA | peltool.py -i/--id "pel_id" | No | - |
| Display a PEL based on its BMC Event ID | peltool --bmc-id "bmc_event_id" | NA | peltool.py --bmc-id "bmc_event_id" | No |  - |
| Display all PELs | peltool -a | NA | peltool.py -a/--all-pels | No | - |
| List PELs | peltool -l | NA | peltool.py -l/--list | No | - |
| Show number of PELs | peltool -n | NA | peltool.py -N/--show-pel-count | C++ tool users | with "non-serviceable" log option "-n" |
| Reverse order of output | peltool -lr | NA | peltool.py -l -r/--reverse | No | - |
| Include hidden PELs | peltool -lh | NA | peltool.py -l -H/--hidden | C++ tool users | with tool usage option "-h" |
| Include informational PELs | peltool -l -f/--info | NA | peltool -l -S 'informational' | C++ tool users | with parse PEL file option "-f" | 
| List only critical system terminating PELs | peltool -l -t/--termination | NA | peltool.py -lO -t/--termination | C++ tool users | with tool behaviour i.e "only termination PELs" |
| Delete a PEL based on its ID | peltool -d/--delete "pelID" | NA | peltool.py -c/--clear "pelID" | C++ tool users | with get JSON format data option "-d" and delete parsed file option "--delete" |
| Delete all PELs | peltool -D/--delete-all | NA | peltool.py -C/--clear-all | C++ tool users | No, but align with single delete option "-c/--clear"
| File containing SRC regular expressions to ignore | peltool -l -s/--scrub "src_scrub_file" | NA | peltool.py -l --scrub "src_scrub_file" | C++ tool users | with serviceable log option "-s" |
| Display PEL(s) in hexdump instead of JSON | peltool -x | NA | peltool.py -X/--hex | C++ tool users | with delete parsed file option "-x" |
| List or display archived PELs (Only in BMC env, use -p for non-BMC env) | peltool --archive | NA | peltool.py -A/--archive | No |  - |
| Only parse serviceable (not info/recovered) PELs | NA | peltool.py -s/--serviceable | Same | No |  - |
| Only parse non-serviceable (info/recovered) PELs | NA | peltool.py  -n/--non-serviceable | peltool.py -n/--non-serviceable | No |  - |
| Skip loading plugins | NA | peltool.py -p/--no-plugins | peltool.py -P/--skip-parser-plugins | No, dev only options |  - |
| Process all files in a directory and save as filename.json | NA | peltool.py -d/--directory "input_directory" -o/--output-dir "output_directory" | Same | No |  - |
| Directory to write output files when processing a directory | NA | peltool.py -o/--output-dir "output_directory" | Same | No |  - |
| Used with -d, only look for files with this extension (e.g. ".pel") | NA | peltool.py -e/--extension | Same | No |  - |
| Delete original file after parsing | NA | peltool.py -x/--delete | Same | No | - |
| Specify path to PELs (non-BMC enviroment only) | NA | NA | peltool.py -p/--path "pels_path" | No | - |
| Get PELs based on the given severities along with servicable logs | NA | NA | peltool.py -S "severity1,severity2,..." | No |  - |
| Get PELs based on the given severities | NA | NA | peltool.py -l -O/--only -S "severity1,..." | No |  - |
| Get PELs based on the given PLID (Platform Log ID) | NA | NA | peltool.py --plid "platform log id" | No | - |
