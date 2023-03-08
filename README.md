# CloudFormation to Terraform CLI

This is a really hacky, mostly OpenAI-generated prototype at a CLI for converting CloudFormation files to Terraform files. 

The CLI is called `cf2tf.py` and it has a `generate` subcommand. It takes two parameters, an input folder containing CloudFormation templates and an output folder where the generated Terraform files should be saved. It iterates over the files in the input folder, passes them into an OpenAI Davinci prompt to convert them to Terraform HCL, and saves the generated files in the output folder. After each file is generated, it runs `terraform validate` on the file to ensure it is valid. If it is not valid, an error message containing the validate output will be shown.

This has a pretty big limitation which is that max prompt size limits to fairly small cloudformation templates.

## Usage

To use this CLI, follow the steps below:

1. Clone the repository and navigate to the `cf2tf` directory.
2. Install the requirements with `pip install -r requirements.txt`
3. `export OPENAI_API_KEY=<redacted>`
4. Run the `cf2tf.py` script with the `generate` subcommand and the input and output folders as arguments:

```bash
python cf2tf.py generate <input_folder> <output_folder>
```
