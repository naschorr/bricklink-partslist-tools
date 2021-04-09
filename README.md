# bricklink-tools
A collection of CLI tools for manipulating and exporting Bricklink parts lists

## Supported Operations
### `missing-parts`
Searches through a PartList of potentially unowned parts, and attempts to see if you've already got those parts available in the owned parts lists. Think of it like a right excluding join in SQL land. This is especially handy when you've made changes to an existing model and want to easily figure out exactly which parts are new.

#### CLI Conditions
- The `--missing-parts` flag is present
- One or more `--owned-parts-list-path` options pointing to your part list .csv file
- One `--unowned-parts-list-path` option pointing to the part list .csv file
- The `--save-path` option specifying where you want to save the output .csv file to
- The `--save-format` option specifying what flavor of output you'd like.

### `merge`
Merges the given owned and unowned PartsLists together, returning a single one containing all of the parts contained in each individual PartsList.

#### CLI Conditions
- The `--merge` flag is present
- Zero or more `--owned-parts-list-path` options pointing to your part list .csv file
- Zero or more `--unowned-parts-list-path` options pointing to your part list .csv file
    
    __Note:__ you need at least one valid owned or unowned parts list path (and ideally two or more) for the merge to complete successfully.

- The `--save-path` option specifying where you want to save the output .csv file to
- The `--save-format` option specifying what flavor of output you'd like.

## Commands
- `--missing-parts` - A flag to choose to perform a check for missing parts, wherein a single unowned-parts-list is compared to one or more owned-parts-lists to find missing pieces. See the `missing-parts` section above for more details.
- `--merge` - A flag to choose to merge all provided `owned-parts-list-path` and `unowned-parts-list-path` parts lists together into a singular list of parts.
- `--owned-parts-list-path`, `-o` - A path to a Bricklink parts list .csv file representing parts that you own. Can be used multiple times.
- `--unowned-parts-list-path`, `-u` - A path to a Bricklink parts list .csv file representing parts that you do not own. Can be used multiple times.
- `--save-path`, `-s` - The path to export manipulated parts list data to
- `--save-format`, `-f` - The format to export manipulated parts list data in, acceptable values include `csv` or `simple-csv`. Note that the `csv` option will output a .csv file with the same headers that were fed into it, while a `simple-csv` will output a simplified version with only the "part", "color", and "quantity" headers and values. The simpler version is suitable for uploading into a Rebrickable parts list, for example.
