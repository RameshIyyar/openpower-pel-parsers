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
| List only critical system terminating PELs | peltool -t/--termination | NA | peltool.py -t/--termination | No | 
| Delete a PEL based on its ID | peltool -d/--delete "pelID" | NA | peltool.py -d/--delete "pelID" | No |
| Delete all PELs | peltool -D/--delete-all | NA | peltool.py -D/--delete-all | No |
| File containing SRC regular expressions to ignore | peltool -l -s/--scrub "src_scrub_file" | NA | peltool.py -l --scrub "src_scrub_file" | C++ tool users |
| Display PEL(s) in hexdump instead of JSON | peltool -x | NA | peltool.py -x/--hex | No |
| List or display archived PELs | peltool --archive | NA | peltool.py -A/--archive | No |
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

