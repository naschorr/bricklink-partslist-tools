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

### `intersection`
Performs an intersection on all provided PartsLists, regardless of them being owned or unowned. It then returns a single PartsList containing only the parts shared between all of the input PartsLists.

#### CLI Conditions
- The `--intersection` flag is present
- Zero or more `--owned-parts-list-path` options pointing to your part list .csv file
- Zero or more `--unowned-parts-list-path` options pointing to your part list .csv file
    
    __Note:__ you need at least one valid owned and/or unowned parts list path (and ideally two or more) for the intersection to complete successfully.

- The `--save-path` option specifying where you want to save the output .csv file to
- The `--save-format` option specifying what flavor of output you'd like.

## Commands
- `--missing-parts` - A flag to choose to perform a check for missing parts, wherein a single unowned-parts-list is compared to one or more owned-parts-lists to find missing pieces. See the `missing-parts` section above for more details.
- `--merge` - A flag to choose to merge all provided `owned-parts-list-path` and `unowned-parts-list-path` parts lists together into a singular list of parts.
- `--owned-parts-list-path`, `-o` - A path to a Bricklink parts list .csv file representing parts that you own. This option can be used multiple times.
- `--unowned-parts-list-path`, `-u` - A path to a Bricklink parts list .csv file representing parts that you do not own. This option can be used multiple times.
- `--any-color`, `-a` - Defines a certain color in the PartsList to be changed over to the `any` color recognized by Bricklink and Rebrickable, which in turn selects the cheapest parts in any available color. For a list of all current colors, see [Rebrickable's color guide](https://rebrickable.com/colors/). Specifically, see the text in the "Bricklink" column, between the single quotes. Note that this mapping happens after all other commands have completed, so the output PartsList will have the specified colors mapped to the `any` color. This option can be used multiple times, for multiple colors that need to be mapped to the `any` color.
- `--save-path`, `-s` - The path to export manipulated parts list data to
- `--save-format`, `-f` - The format to export manipulated parts list data in, acceptable values include:
    - `csv`
    - `simple-csv`
    
    Note that the `csv` option will output a .csv file with the Bricklink parts list headers that were fed into it, while a `simple-csv` will output a simplified version with only the "part", "color", and "quantity" headers and values. The simpler version is suitable for uploading into a Rebrickable parts list, for example. Please note that if you do intend to import into Rebrickable, that you must set the "External Source" option to be "BrickLink", instead of the default "Rebrickable (no conversion)" option.
