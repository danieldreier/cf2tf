"""
This module provides a CLI for converting Cloudformation files to Terraform files.

The CLI is called cf2tf.py and it has a "generate" subcommand. It takes two parameters, an input folder containing Cloudformation templates and an output folder where the generated Terraform files should be saved. It iterates over the files in the input folder, passes them into an OpenAI davinci prompt to convert them to Terraform HCL, and saves the generated files in the output folder.

It iterates over the files in the input folder, passes them into an OpenAI davinci prompt to convert them to Terraform HCL, and saves the generated files in the output folder.

After each file is generated, it runs Terraform validate on the file to ensure it is valid. If it is not valid, an error message containing the validate output will be shown.
"""


import click
import os
import logging
import subprocess
import openai


log = logging.getLogger(__name__)



@click.option('--debug', is_flag=True, help='Enables debug logging')
@click.group()
def cli(debug):
    """
    CLI for converting Cloudformation files to Terraform files
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    log.debug('Starting CLI')
    pass

@cli.command()
def help_command():
    """
    Shows help for the CLI.
    """
    click.echo(cli.get_help(click.Context(cli)))
    pass


@cli.command()
@click.argument('input_folder', type=click.Path(exists=True))
@click.argument('output_folder', type=click.Path(exists=True))
def generate(input_folder, output_folder):
    """
    Generates Terraform files from Cloudformation templates.
    """
    log.debug('Generating Terraform files from Cloudformation templates')
    validate_input_folder(input_folder)
    validate_output_folder(output_folder)
    generate_terraform_hcl_from_cloudformation_files(input_folder, output_folder)


    log.debug('Generating Terraform HCL from Cloudformation files')
def generate_terraform_hcl_from_cloudformation_files(input_folder, output_folder):
    """
    Generates Terraform HCL from Cloudformation files.
    """
    for filename in os.listdir(input_folder):
        generate_terraform_hcl_from_cloudformation_file(input_folder, output_folder, filename)
        print("Generated Terraform file: " + filename)

def generate_terraform_hcl_from_cloudformation_file(input_folder, output_folder, filename):
    """
    Generates Terraform HCL from a Cloudformation file and saves it to a file.
    """
    cloudformation_file_path = os.path.join(input_folder, filename)
    log.debug('Generating Terraform HCL from Cloudformation file: %s', cloudformation_file_path)
    terraform_hcl = generate_terraform_hcl_from_cloudformation_file_path(cloudformation_file_path)

    validate_terraform_hcl(terraform_hcl)
    save_terraform_hcl_to_file(terraform_hcl, os.path.join(output_folder, filename + '.tf'))

def save_terraform_hcl_to_file(terraform_hcl: str, terraform_file_path: str):
    log.debug('Writing generated Terraform HCL to file: %s', terraform_file_path)
    """
    Saves the generated Terraform HCL to a file.
    """
    with open(terraform_file_path, 'w') as terraform_file:
        terraform_file.write(terraform_hcl)

def validate_input_folder(input_folder):
    """
    Validates that the input folder exists and is a directory.
    """
    if not os.path.isdir(input_folder):
        log.error('Input folder does not exist or is not a directory: %s', input_folder)

def validate_output_folder(output_folder):
    """
    Validates that the output folder exists and is a directory.
    """
    log.debug('Validating output folder')
    if not os.path.isdir(output_folder):
        log.error('Output folder does not exist or is not a directory: %s', output_folder)
        raise click.BadParameter('Output folder does not exist or is not a directory: %s', output_folder)

def generate_terraform_hcl_from_cloudformation_file_path(cloudformation_file_path: str) -> str:
    """
    Generates Terraform HCL from a Cloudformation file path.
    """
    with open(cloudformation_file_path, 'r') as cloudformation_file:

        cloudformation_file_contents = cloudformation_file.read()

    prompt = "translate the following cloudformation to valid Terraform code with equivalent functionality. Let's think step by step. \n\n\n" + cloudformation_file_contents
    log.debug('prompt: %s', prompt)
    log.debug('Generating Terraform HCL from Cloudformation file: %s', cloudformation_file_path)

    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=3345,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
    )

    log.debug('completion: %s', completion.choices[0].text)
    if len(completion.choices[0].text) < 5:
        log.error('Generated Terraform HCL is too short: %s', completion.choices[0].text)
        raise click.BadParameter('Generated Terraform HCL is too short')

    return completion.choices[0].text

def validate_terraform_hcl(terraform_hcl: str):
    """
    Validates the generated Terraform HCL.
    """
    log.debug('Validating generated Terraform HCL')
    terraform_hcl = terraform_hcl.encode()
    terraform_validate_output = subprocess.check_output(['terraform', 'validate'], input=terraform_hcl, stderr=subprocess.STDOUT)
    log.debug('Terraform validate output: %s', terraform_validate_output)
    if terraform_validate_output != b'\x1b[32m\x1b[1mSuccess!\x1b[0m The configuration is valid.\n\x1b[0m\n':
        log.error('Generated Terraform HCL is not valid: %s', terraform_validate_output)
        raise click.BadParameter('Generated Terraform HCL is not valid')

if __name__ == '__main__':
    cli()
